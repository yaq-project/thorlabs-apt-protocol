import struct
import functools
from typing import Dict, Any

id_to_func = {}
HEADER_SIZE = 6


def parser(msgid):
    def wrapper(func):
        @functools.wraps(func)
        def inner(data: bytes) -> Dict[str, Any]:
            msgid_read, _, dest, source = struct.unpack_from("<HHBB", data)
            dest = dest & ~0x80
            assert msgid == msgid_read
            ret = {"msg": func.__name__, "msgid": msgid, "dest": dest, "source": source}
            ret.update(func(data))
            return ret

        if msgid in id_to_func:
            raise ValueError(f"Duplicate msgid: {hex(msgid)}")
        id_to_func[msgid] = inner
        return inner

    return wrapper


def _parse_dcstatus(data: bytes) -> Dict[str, Any]:
    chan_ident, position, velocity, _, status_bits = struct.unpack_from(
        "<HlHHL", data, HEADER_SIZE
    )
    ret = {
        "chan_ident": chan_ident,
        "position": position,
        "velocity": velocity,
    }
    ret.update(_parse_status_bits(status_bits))
    return ret


def _parse_status(data: bytes) -> Dict[str, Any]:
    chan_ident, position, enc_count, status_bits = struct.unpack_from(
        "<HllL", data, HEADER_SIZE
    )
    ret = {
        "chan_ident": chan_ident,
        "position": position,
        "enc_count": enc_count,
    }
    ret.update(_parse_status_bits(status_bits))
    return ret


def _parse_status_bits(status_bits: int) -> Dict[str, Any]:
    # Bitfield
    # Tracking and interlock are the same bit?
    return {
        "forward_limit_switch": bool(status_bits & 0x1),
        "reverse_limit_switch": bool(status_bits & 0x2),
        "moving_forward": bool(status_bits & 0x10),
        "moving_reverse": bool(status_bits & 0x20),
        "jogging_forward": bool(status_bits & 0x40),
        "jogging_reverse": bool(status_bits & 0x80),
        "motor_connected": bool(status_bits & 0x100),
        "homing": bool(status_bits & 0x200),
        "homed": bool(status_bits & 0x400),
        "tracking": bool(status_bits & 0x1000),
        "interlock": bool(status_bits & 0x1000),
        "settled": bool(status_bits & 0x2000),
        "motion_error": bool(status_bits & 0x4000),
        "motor_current_limit_reached": bool(status_bits & 0x1000000),
        "channel_enabled": bool(status_bits & 0x80000000),
    }


@parser(0x0212)
def mod_get_chanenablestate(data: bytes) -> Dict[str, Any]:
    return {"chan_ident": data[2], "enabled": data[3] == 0x01}


@parser(0x0002)
def hw_disconnect(data: bytes) -> Dict[str, Any]:
    return {}


@parser(0x0080)
def hw_response(data: bytes) -> Dict[str, Any]:
    return {}


@parser(0x0081)
def hw_richresponse(data: bytes) -> Dict[str, Any]:
    msg_ident, code, notes = struct.unpack_from("<HH64c", data, HEADER_SIZE)
    return {"msg_ident": msg_ident, "code": code, "notes": notes}


@parser(0x0006)
def hw_get_info(data: bytes) -> Dict[str, Any]:
    (
        serial_number,
        model_number,
        type_,
        *firmware_version,
        _,
        _,
        hw_version,
        mod_state,
        nchs,
    ) = struct.unpack_from("<l8sH4B60sHHH", data, HEADER_SIZE)
    return {
        "serial_number": serial_number,
        "model_number": model_number,
        "type": type_,
        "firmware_version": firmware_version[::-1],
        "hw_version": hw_version,
        "mod_state": mod_state,
        "nchs": nchs,
    }


@parser(0x0061)
def rack_get_bayused(data: bytes) -> Dict[str, Any]:
    return {"bay_ident": data[2], "occupied": data[3] == 0x01}


@parser(0x0066)
def hub_get_bayused(data: bytes) -> Dict[str, Any]:
    bay_ident = data[2]
    if bay_ident == 0xFF:
        bay_ident = -1
    return {"bay_ident": bay_ident}


@parser(0x0226)
def rack_get_statusbits(data: bytes) -> Dict[str, Any]:
    # Bitfield
    status_bits, = struct.unpack_from("<L", data, HEADER_SIZE)
    return {
        "dig_outs": [
            bool(status_bits & 0x1),
            bool(status_bits & 0x2),
            bool(status_bits & 0x3),
            bool(status_bits & 0x4),
        ]
    }


@parser(0x0230)
def rack_get_digoutputs(data: bytes) -> Dict[str, Any]:
    # Bitfield
    return {
        "dig_outs": [
            bool(data[2] & 0x1),
            bool(data[2] & 0x2),
            bool(data[2] & 0x3),
            bool(data[2] & 0x4),
        ]
    }


@parser(0x0215)
def mod_get_digoutputs(data: bytes) -> Dict[str, Any]:
    # This differs from 0x0225 and 0x0230, as the number of outputs is not known
    # Bitfield
    return {"bits": data[2]}


@parser(0x0252)
def hw_get_kcubemmilock(data: bytes) -> Dict[str, Any]:
    return {"locked": data[3] == 0x01}


@parser(0x0412)
def mot_get_poscounter(data: bytes) -> Dict[str, Any]:
    chan_ident, position = struct.unpack_from("<Hl", data, HEADER_SIZE)
    return {"chan_ident": chan_ident, "position": position}


@parser(0x040B)
def mot_get_enccounter(data: bytes) -> Dict[str, Any]:
    chan_ident, encoder_count = struct.unpack_from("<Hl", data, HEADER_SIZE)
    return {"chan_ident": chan_ident, "encoder_count": encoder_count}


@parser(0x0415)
def mot_get_velparams(data: bytes) -> Dict[str, Any]:
    chan_ident, min_velocity, acceleration, max_velocity = struct.unpack_from(
        "<H3l", data, HEADER_SIZE
    )
    return {
        "chan_ident": chan_ident,
        "min_velocity": min_velocity,
        "acceleration": acceleration,
        "max_velocity": max_velocity,
    }


@parser(0x0418)
def mot_get_jogparams(data: bytes) -> Dict[str, Any]:
    (
        chan_ident,
        jog_mode,
        step_size,
        min_velocity,
        acceleration,
        max_velocity,
        stop_mode,
    ) = struct.unpack_from("<HH4lH", data, HEADER_SIZE)
    return {
        "chan_ident": chan_ident,
        "jog_mode": jog_mode,
        "step_size": step_size,
        "min_velocity": min_velocity,
        "acceleration": acceleration,
        "max_velocity": max_velocity,
        "stop_mode": stop_mode,
    }


@parser(0x042C)
def mot_get_adcinputs(data: bytes) -> Dict[str, Any]:
    adc_input1, adc_input2 = struct.unpack_from("<HH", data, HEADER_SIZE)
    return {
        "adc_input1": adc_input1 * 5 / 2 ** 15,
        "adc_input2": adc_input2 * 5 / 2 ** 15,
    }


@parser(0x0428)
def mot_get_powerparams(data: bytes) -> Dict[str, Any]:
    chan_ident, rest_factor, move_factor = struct.unpack_from("<3H", data, HEADER_SIZE)
    return {
        "chan_ident": chan_ident,
        "rest_factor": rest_factor,
        "move_factor": move_factor,
    }


@parser(0x043C)
def mot_genmoveparams(data: bytes) -> Dict[str, Any]:
    chan_ident, backlash_distance = struct.unpack_from("<Hl", data, HEADER_SIZE)
    return {"chan_ident": chan_ident, "backlash_distance": backlash_distance}


@parser(0x0447)
def mot_get_moverelparams(data: bytes) -> Dict[str, Any]:
    chan_ident, relative_distance = struct.unpack_from("<Hl", data, HEADER_SIZE)
    return {"chan_ident": chan_ident, "relative_distance": relative_distance}


@parser(0x0452)
def mot_get_moveabsparams(data: bytes) -> Dict[str, Any]:
    chan_ident, absolute_position = struct.unpack_from("<Hl", data, HEADER_SIZE)
    return {"chan_ident": chan_ident, "absolute_position": absolute_position}


@parser(0x0442)
def mot_get_homeparams(data: bytes) -> Dict[str, Any]:
    (
        chan_ident,
        home_dir,
        limit_switch,
        home_velocity,
        offset_distance,
    ) = struct.unpack_from("<3Hll", data, HEADER_SIZE)
    return {
        "chan_ident": chan_ident,
        "home_dir": home_dir,
        "limit_switch": limit_switch,
        "home_velocity": home_velocity,
        "offset_distance": offset_distance,
    }


@parser(0x0425)
def mot_get_limswitchparams(data: bytes) -> Dict[str, Any]:
    (
        chan_ident,
        cw_hardlimit,
        ccw_hardlimit,
        cw_softlimit,
        ccw_softlimit,
        soft_limit_mode,
    ) = struct.unpack_from("<3HLLH", data, HEADER_SIZE)
    return {
        "chan_ident": chan_ident,
        "cw_hardlimit": cw_hardlimit,
        "ccw_hardlimit": ccw_hardlimit,
        "cw_softlimit": cw_softlimit,
        "ccw_softlimit": ccw_softlimit,
        "soft_limit_mode": soft_limit_mode,
    }


@parser(0x0444)
def mot_move_homed(data: bytes) -> Dict[str, Any]:
    return {"chan_ident": data[2]}


@parser(0x0464)
def mot_move_completed(data: bytes) -> Dict[str, Any]:
    return _parse_dcstatus(data)


@parser(0x0466)
def mot_move_stopped(data: bytes) -> Dict[str, Any]:
    return _parse_dcstatus(data)


@parser(0x04F6)
def mot_get_bowindex(data: bytes) -> Dict[str, Any]:
    chan_ident, bow_index = struct.unpack_from("<HH", data, HEADER_SIZE)
    return {"chan_ident": chan_ident, "bow_index": bow_index}


@parser(0x04A2)
def mot_get_dcpidparams(data: bytes) -> Dict[str, Any]:
    (
        chan_ident,
        proportional,
        integral,
        differential,
        integral_limits,
        filter_control,
    ) = struct.unpack_from("<H4LH", data, HEADER_SIZE)
    return {"chan_ident": data[2], "enabled": data[3] == 0x01}


@parser(0x04B5)
def mot_get_avmodes(data: bytes) -> Dict[str, Any]:
    chan_ident, mode_bits = struct.unpack_from("<HH", data, HEADER_SIZE)
    # Bitfield
    return {"chan_ident": chan_ident, "mode_bits": mode_bits}


@parser(0x04B2)
def mot_get_potparams(data: bytes) -> Dict[str, Any]:
    chan_ident, zero_wnd, vel1, wnd1, vel2, wnd2, vel3, wnd3, vel4 = struct.unpack_from(
        "<HHlHlHlHl", data, HEADER_SIZE
    )
    return {
        "chan_ident": chan_ident,
        "zero_wnd": zero_wnd,
        "vel1": vel1,
        "wnd1": wnd1,
        "vel2": vel2,
        "wnd2": wnd2,
        "vel3": vel3,
        "wnd3": wnd3,
        "vel4": vel4,
    }


@parser(0x04B8)
def mot_get_buttonparams(data: bytes) -> Dict[str, Any]:
    chan_ident, mode, position1, position2, time_out1, time_out2 = struct.unpack_from(
        "<HHllHH", data, HEADER_SIZE
    )
    return {
        "chan_ident": chan_ident,
        "mode": mode,
        "position1": position1,
        "position2": position2,
        "time_out1": time_out1,
        "time_out2": time_out2,
    }


@parser(0x0491)
def mot_get_dcstatusupdate(data: bytes) -> Dict[str, Any]:
    return _parse_dcstatus(data)


@parser(0x04D9)
def mot_get_positionloopparams(data: bytes) -> Dict[str, Any]:
    (
        chan_ident,
        kp_pos,
        integral,
        i_lim_pos,
        differential,
        kd_time_pos,
        kout_pos,
        kaff_pos,
        pos_err_lim,
        _,
        _,
    ) = struct.unpack_from("<3HL5HL2H", data, HEADER_SIZE)
    return {
        "chan_ident": chan_ident,
        "kp_pos": kp_pos,
        "integral": integral,
        "i_lim_pos": i_lim_pos,
        "differential": differential,
        "kd_time_pos": kd_time_pos,
        "kout_pos": kout_pos,
        "kaff_pos": kaff_pos,
        "pos_err_lim": pos_err_lim,
    }


@parser(0x04DC)
def mot_get_motoroutputparams(data: bytes) -> Dict[str, Any]:
    (
        chan_ident,
        cont_current_lim,
        energy_lim,
        motor_lim,
        motor_bias,
        _,
        _,
    ) = struct.unpack_from("<7H", data, HEADER_SIZE)
    return {
        "chan_ident": chan_ident,
        "cont_current_lim": cont_current_lim,
        "energy_lim": energy_lim,
        "motor_lim": motor_lim,
        "motor_bias": motor_bias,
    }


@parser(0x04E2)
def mot_get_tracksettleparams(data: bytes) -> Dict[str, Any]:
    chan_ident, time, settle_window, track_window, _, _ = struct.unpack_from(
        "<6H", data, HEADER_SIZE
    )
    return {
        "chan_ident": chan_ident,
        "time": time,
        "settle_window": settle_window,
        "track_window": track_window,
    }


@parser(0x04E5)
def mot_get_profilemodeparams(data: bytes) -> Dict[str, Any]:
    chan_ident, mode, jerk, _, _ = struct.unpack_from("<HHLHH", data, HEADER_SIZE)
    return {
        "chan_ident": chan_ident,
        "mode": mode,
        "jerk": jerk,
    }


@parser(0x04E8)
def mot_get_joystickparams(data: bytes) -> Dict[str, Any]:
    (
        chan_ident,
        gear_high_max_vel,
        gear_low_accn,
        gear_high_accn,
        dir_sense,
    ) = struct.unpack_from("<H4LH", data, HEADER_SIZE)
    return {
        "chan_ident": chan_ident,
        "gear_high_max_vel": gear_high_max_vel,
        "gear_low_accn": gear_low_accn,
        "gear_high_accn": gear_high_accn,
        "dir_sense": dir_sense,
    }


@parser(0x04D6)
def mot_get_currentloopoarams(data: bytes) -> Dict[str, Any]:
    (
        chan_ident,
        phase,
        kp_current,
        ki_current,
        i_lim_current,
        i_dead_band,
        kff,
        _,
        _,
    ) = struct.unpack_from("<9H", data, HEADER_SIZE)
    return {
        "chan_ident": chan_ident,
        "phase": phase,
        "kp_current": kp_current,
        "ki_current": ki_current,
        "i_lim_current": i_lim_current,
        "i_dead_band": i_dead_band,
        "kff": kff,
    }


@parser(0x04EB)
def mot_get_settledcurrentloopparams(data: bytes) -> Dict[str, Any]:
    (
        chan_ident,
        phase,
        kp_settled,
        ki_settled,
        i_lim_settled,
        i_dead_band_settled,
        kff_settled,
        _,
        _,
    ) = struct.unpack_from("<9H", data, HEADER_SIZE)
    return {
        "chan_ident": chan_ident,
        "phase": phase,
        "kp_settled": kp_settled,
        "ki_settled": ki_settled,
        "i_lim_settled": i_lim_settled,
        "i_dead_band_settled": i_dead_band_settled,
        "kff_settled": kff_settled,
    }


@parser(0x04F2)
def mot_get_stageaxisparams(data: bytes) -> Dict[str, Any]:
    (
        chan_ident,
        stage_id,
        axis_id,
        part_no_axis,
        serial_num,
        counts_per_unit,
        min_pos,
        max_pos,
        max_accn,
        max_dec,
        max_vel,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = struct.unpack_from("<HHH16sLL5l4H4L", data, HEADER_SIZE)
    return {
        "chan_ident": chan_ident,
        "stage_id": stage_id,
        "axis_id": axis_id,
        "part_no_axis": part_no_axis,
        "serial_num": serial_num,
        "counts_per_unit": counts_per_unit,
        "min_pos": min_pos,
        "max_pos": max_pos,
        "max_accn": max_accn,
        "max_dec": max_dec,
        "max_vel": max_vel,
    }


@parser(0x0481)
def mot_get_statusupdate(data: bytes) -> Dict[str, Any]:
    return _parse_status(data)


@parser(0x042A)
def mot_get_statusbits(data: bytes) -> Dict[str, Any]:
    chan_ident, status_bits = struct.unpack_from("<HL", data, HEADER_SIZE)
    ret = {
        "chan_ident": chan_ident,
    }
    ret.update(_parse_status_bits(status_bits))
    # Bitfield
    return ret


@parser(0x0502)
def mot_get_trigger(data: bytes) -> Dict[str, Any]:
    return {
        "chan_ident": data[2],
        "mode": data[3],
    }


@parser(0x0522)
def mot_get_kcubemmiparams(data: bytes) -> Dict[str, Any]:
    (
        chan_ident,
        mode,
        max_vel,
        accn,
        dir_sense,
        pre_set_pos1,
        pre_set_pos2,
        disp_brightness,
        disp_timeout,
        disp_dim_level,
    ) = struct.unpack_from("<HHllHll3H", data, HEADER_SIZE)
    return {
        "chan_ident": chan_ident,
        "mode": mode,
        "max_vel": max_vel,
        "accn": accn,
        "dir_sense": dir_sense,
        "pre_set_pos1": pre_set_pos1,
        "pre_set_pos2": pre_set_pos2,
        "disp_brightness": disp_brightness,
        "disp_timeout": disp_timeout,
        "disp_dim_level": disp_dim_level,
    }


@parser(0x0525)
def mot_get_kcubetrigconfig(data: bytes) -> Dict[str, Any]:
    (
        chan_ident,
        trig1_mode,
        trig1_polarity,
        trig2_mode,
        trig2_polarity,
    ) = struct.unpack_from("<5H", data, HEADER_SIZE)
    return {
        "chan_ident": chan_ident,
        "trig1_mode": trig1_mode,
        "trig1_polarity": trig1_polarity,
        "trig2_mode": trig2_mode,
        "trig2_polarity": trig2_polarity,
    }


@parser(0x0528)
def mot_get_kcubeposttrigparams(data: bytes) -> Dict[str, Any]:
    (
        chan_ident,
        start_pos_fwd,
        interval_fwd,
        num_pulses_fwd,
        start_pos_rev,
        interval_rev,
        num_pulses_rev,
        pulse_width,
        num_cycles,
    ) = struct.unpack_from("<H8l", data, HEADER_SIZE)
    return {
        "chan_ident": chan_ident,
        "start_pos_fwd": start_pos_fwd,
        "interval_fwd": interval_fwd,
        "num_pulses_fwd": num_pulses_fwd,
        "start_pos_rev": start_pos_rev,
        "interval_rev": interval_rev,
        "num_pulses_rev": num_pulses_rev,
        "pulse_width": pulse_width,
        "num_cycles": num_cycles,
    }


@parser(0x052B)
def mot_get_kcubestloopparams(data: bytes) -> Dict[str, Any]:
    (
        chan_ident,
        loop_mode,
        prop,
        int,
        diff,
        pid_clip,
        pid_tol,
        encoder_const,
    ) = struct.unpack_from("<HH5lL", data, HEADER_SIZE)
    return {
        "chan_ident": chan_ident,
        "loop_mode": loop_mode,
        "prop": prop,
        "int": int,
        "diff": diff,
        "pid_clip": pid_clip,
        "pid_tol": pid_tol,
        "encoder_const": encoder_const,
    }


@parser(0x0512)
def mot_get_mmf_operparams(data: bytes) -> Dict[str, Any]:
    (
        chan_ident,
        i_tranit_time,
        i_transit_time_adc,
        oper_mode1,
        sig_mode1,
        pulse_width1,
        oper_mode2,
        sig_mode2,
        pulse_width2,
        _,
        _,
    ) = struct.unpack_from("<HllHHlHHllL", data, HEADER_SIZE)
    return {
        "chan_ident": chan_ident,
        "i_tranit_time": i_tranit_time,
        "i_transit_time_adc": i_transit_time_adc,
        "oper_mode1": oper_mode1,
        "sig_mode1": sig_mode1,
        "pulse_width1": pulse_width1,
        "oper_mode2": oper_mode2,
        "sig_mode2": sig_mode2,
        "pulse_width2": pulse_width2,
    }


@parser(0x04C2)
def mot_get_sol_operatingmode(data: bytes) -> Dict[str, Any]:
    return {"chan_ident": data[2], "mode": data[3]}


@parser(0x04C5)
def mot_get_sol_cycleparams(data: bytes) -> Dict[str, Any]:
    chan_ident, off_time, num_cycles = struct.unpack_from("<H3l", data, HEADER_SIZE)
    return {
        "chan_ident": chan_ident,
        "off_time": off_time,
        "num_cycles": num_cycles,
    }


@parser(0x04C8)
def mot_get_sol_interlockmode(data: bytes) -> Dict[str, Any]:
    return {"chan_ident": data[2], "mode": data[3] == 0x01}


@parser(0x04CD)
def mot_get_sol_state(data: bytes) -> Dict[str, Any]:
    return {"chan_ident": data[2], "state": data[3] == 0x01}
