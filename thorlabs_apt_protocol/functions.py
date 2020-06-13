from typing import Optional, Sequence
import struct


def _pack(
    msgid: int,
    dest: int,
    source: int,
    *,
    param1: int = 0,
    param2: int = 0,
    data: Optional[bytes] = None
):
    if data is not None:
        assert param1 == param2 == 0
        return struct.pack("<HHBB", msgid, len(data), dest | 0x80, source) + data
    else:
        return struct.pack("<H2b2B", msgid, param1, param2, dest, source)


def mod_identify(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0223, dest, source, param1=chan_ident)


def mod_set_chanenablestate(
    dest: int, source: int, chan_ident: int, enable_state: int
) -> bytes:
    return _pack(0x0210, dest, source, param1=chan_ident, param2=enable_state)


def mod_req_chanenablestate(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0211, dest, source, param1=chan_ident)


def hw_disconnect(dest: int, source: int) -> bytes:
    return _pack(0x0002, dest, source)


def hw_start_updatemsgs(dest: int, source: int) -> bytes:
    return _pack(0x0011, dest, source)


def hw_stop_updatemsgs(dest: int, source: int) -> bytes:
    return _pack(0x0012, dest, source)


def hw_req_info(dest: int, source: int) -> bytes:
    return _pack(0x0005, dest, source)


def rack_req_bayused(dest: int, source: int, bay_ident: int) -> bytes:
    return _pack(0x0060, dest, source, param1=bay_ident)


def hub_req_bayused(dest: int, source: int) -> bytes:
    return _pack(0x0065, dest, source)


def rack_req_statusbits(dest: int, source: int) -> bytes:
    # I suspect there is an error in the docs, and status_bits should be omitted
    # This reflects what I think it _should_ be
    # - KFS 2020-06-05
    return _pack(0x0226, dest, source)


def rack_set_digoutputs(dest: int, source: int, dig_outs: Sequence[bool]) -> bytes:
    dig_out_param = 0
    bit = 1
    for i in dig_outs:
        if i:
            dig_out_param |= bit
        bit <<= 1
    return _pack(0x0228, dest, source, param1=dig_out_param)


def rack_get_digoutputs(dest: int, source: int) -> bytes:
    return _pack(0x0229, dest, source)


def mod_set_digoutputs(dest: int, source: int, chan_ident: int, dig_outs: Sequence[bool]) -> bytes:
    dig_out_param = 0
    bit = 1
    for i in dig_outs:
        if i:
            dig_out_param |= bit
        bit <<= 1
    return _pack(0x0213, dest, source, param1=dig_out_param)


def mod_req_digoutputs(dest: int, source: int) -> bytes:
    # I suspect there is an error in the docs, and bits should be omitted
    # This reflects what I think it _should_ be
    # - KFS 2020-06-05
    return _pack(0x0214, dest, source)


def hw_set_kcubemmilock(dest: int, source: int, mmi_lock: int) -> bytes:
    return _pack(0x0250, dest, source, param2=mmi_lock)


def hw_req_kcubemmilock(dest: int, source: int) -> bytes:
    # I suspect there is an error in the docs, and bits should be omitted
    # This reflects what I think it _should_ be
    # - KFS 2020-06-05
    return _pack(0x0251, dest, source)


def restorefactorysettings(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0686, dest, source, param1=chan_ident)


def hw_yes_flash_programming(dest: int, source: int) -> bytes:
    return _pack(0x0017, dest, source)


def hw_no_flash_programming(dest: int, source: int) -> bytes:
    return _pack(0x0018, dest, source)


def mot_set_poscounter(dest: int, source: int, chan_ident: int, position: int) -> bytes:
    data = struct.pack("<Hl", chan_ident, position)
    return _pack(0x0410, dest, source, data=data)


def mot_req_poscounter(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0411, dest, source, param1=chan_ident)


def mot_set_enccounter(dest: int, source: int, chan_ident: int, encoder_count) -> bytes:
    data = struct.pack("<Hl", chan_ident, encoder_count)
    return _pack(0x0409, dest, source, data=data)


def mot_req_enccounter(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x040A, dest, source, param1=chan_ident)


def mot_set_velparams(
    dest: int,
    source: int,
    chan_ident: int,
    min_velocity: int,
    acceleration: int,
    max_velocity: int,
) -> bytes:
    data = struct.pack("<H3l", chan_ident, min_velocity, acceleration, max_velocity)
    return _pack(0x0413, dest, source, data=data)


def mot_req_velparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0414, dest, source, param1=chan_ident)


def mot_set_jogparams(
    dest: int,
    source: int,
    chan_ident: int,
    jog_mode: int,
    step_size: int,
    min_velocity: int,
    acceleration: int,
    max_velocity: int,
    stop_mode: int,
) -> bytes:
    data = struct.pack(
        "<HH4lH",
        chan_ident,
        jog_mode,
        step_size,
        min_velocity,
        acceleration,
        max_velocity,
        stop_mode,
    )
    return _pack(0x0416, dest, source, param1=chan_ident)


def mot_req_jogparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0417, dest, source, param1=chan_ident)


def mot_req_adcinputs(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x042B, dest, source, param1=chan_ident)


def mot_set_powerparams(
    dest: int, source: int, chan_ident: int, rest_factor: int, move_factor: int
) -> bytes:
    data = struct.pack("<3H", chan_ident, rest_factor, move_factor)
    return _pack(0x0426, dest, source, data=data)


def mot_req_powerparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0427, dest, source, param1=chan_ident)


def mot_set_genmoveparams(
    dest: int, source: int, chan_ident: int, backlash_distance: int
) -> bytes:
    data = struct.pack("<Hl", chan_ident, backlash_distance)
    return _pack(0x043A, dest, source, data=data)


def mot_req_genmoveparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x043B, dest, source, param1=chan_ident)


def mot_set_moverelparams(
    dest: int, source: int, chan_ident: int, relative_distance: int
) -> bytes:
    data = struct.pack("<Hl", chan_ident, relative_distance)
    return _pack(0x0445, dest, source, data=data)


def mot_req_moverelparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0446, dest, source, param1=chan_ident)


def mot_set_moveabsparams(
    dest: int, source: int, chan_ident: int, absolute_position: int
) -> bytes:
    data = struct.pack("<Hl", chan_ident, absolute_position)
    return _pack(0x0450, dest, source, data=data)


def mot_req_moveabsparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0451, dest, source, param1=chan_ident)


def mot_set_homeparams(
    dest: int,
    source: int,
    chan_ident: int,
    home_dir: int,
    limit_switch: int,
    home_velocity: int,
    offset_distance: int,
) -> bytes:
    data = struct.pack(
        "<3Hll", chan_ident, home_dir, limit_switch, home_velocity, offset_distance
    )
    return _pack(0x0440, dest, source, param1=chan_ident)


def mot_req_homeparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0441, dest, source, param1=chan_ident)


def mot_set_limswitchparams(
    dest: int,
    source: int,
    chan_ident: int,
    cw_hardlimit: int,
    ccw_hardlimit: int,
    cw_softlimit: int,
    ccw_softlimit: int,
    sort_limit_mode: int,
) -> bytes:
    data = struct.pack(
        "<3HLLH",
        chan_ident,
        cw_hardlimit,
        ccw_hardlimit,
        cw_softlimit,
        ccw_softlimit,
        sort_limit_mode,
    )
    return _pack(0x0423, dest, source, data=data)


def mot_req_limswitchparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0424, dest, source, param1=chan_ident)


def mot_move_home(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0443, dest, source, param1=chan_ident)


def mot_move_relative(
    dest: int, source: int, chan_ident: int, distance: Optional[int] = None
):
    msgid = 0x0448
    if distance is None:
        return _pack(msgid, dest, source, param1=chan_ident)
    else:
        data = struct.pack("<Hl", chan_ident, distance)
        return _pack(msgid, dest, source, data=data)


def mot_move_absolute(
    dest: int, source: int, chan_ident: int, position: Optional[int] = None
):
    msgid = 0x0453
    if position is None:
        return _pack(msgid, dest, source, param1=chan_ident)
    else:
        data = struct.pack("<Hl", chan_ident, position)
        return _pack(msgid, dest, source, data=data)


def mot_move_jog(dest: int, source: int, chan_ident: int, direction) -> bytes:
    return _pack(0x046A, dest, source, param1=chan_ident, param2=direction)


def mot_move_velocity(dest: int, source: int, chan_ident: int, direction) -> bytes:
    return _pack(0x0457, dest, source, param1=chan_ident, param2=direction)


def mot_move_stop(dest: int, source: int, chan_ident: int, stop_mode: int) -> bytes:
    return _pack(0x0465, dest, source, param1=chan_ident, param2=stop_mode)


def mot_set_bowindex(dest: int, source: int, chan_ident: int, bow_index: int) -> bytes:
    data = struct.pack("<HH", chan_ident, bow_index)
    return _pack(0x04F4, dest, source, param1=chan_ident)


def mot_req_bowindex(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x04F5, dest, source, param1=chan_ident)


def mot_set_dcpidparams(
    dest: int,
    source: int,
    chan_ident: int,
    proportional: Optional[int] = None,
    integral: Optional[int] = None,
    differential: Optional[int] = None,
    integral_limit: Optional[int] = None,
) -> bytes:
    filter_control = 0
    if proportional is not None:
        filter_control |= 1
    else:
        proportional = 0
    if integral is not None:
        filter_control |= 2
    else:
        integral = 0
    if differential is not None:
        filter_control |= 4
    else:
        differential = 0
    if integral_limit is not None:
        filter_control |= 8
    else:
        integral_limit = 0
    data = struct.pack(
        "<H4LH",
        chan_ident,
        proportional,
        integral,
        differential,
        integral_limit,
        filter_control,
    )
    return _pack(0x04A0, dest, source, data=data)


def mot_req_dcpidparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x04A1, dest, source, param1=chan_ident)


def mot_set_avmodes(dest: int, source: int, chan_ident: int, mode_bits: int) -> bytes:
    data = struct.pack("<HH", chan_ident, mode_bits)
    return _pack(0x04B3, dest, source, data=data)


def mot_req_avmodes(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x04B4, dest, source, param1=chan_ident)


def mot_set_potparams(
    dest: int,
    source: int,
    chan_ident: int,
    zero_wnd: int,
    vel1: int,
    wnd1: int,
    vel2: int,
    wnd2: int,
    vel3: int,
    wnd3: int,
    vel4: int,
) -> bytes:
    data = struct.pack(
        "<HHlHlHlHl", chan_ident, zero_wnd, vel1, wnd1, vel2, wnd2, vel3, wnd3, vel4
    )
    return _pack(0x04B0, dest, source, data=data)


def mot_req_potparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x04B1, dest, source, param1=chan_ident)


def mot_set_buttonparams(
    dest: int,
    source: int,
    chan_ident: int,
    mode: int,
    position1: int,
    position2: int,
    time_out1: int,
    time_out2: int,
) -> bytes:
    data = struct.pack(
        "<HHllHH", chan_ident, mode, position1, position2, time_out1, time_out2
    )
    return _pack(0x04B6, dest, source, data=data)


def mot_req_buttonparams(
    dest: int, source: int, chan_ident: int, msgid_param: int
) -> bytes:
    data = struct.pack("<HH", chan_ident, msgid_param)
    return _pack(0x04B9, dest, source, data=data)


def mot_set_eepromparams(
    dest: int, source: int, chan_ident: int, msgid_param: int
) -> bytes:
    data = struct.pack("<HH", chan_ident, msgid_param)
    return _pack(0x04B9, dest, source, data=data)


def mot_set_positionloopparams(
    dest: int,
    source: int,
    chan_ident: int,
    kp_pos: int,
    integral: int,
    i_lim_pos: int,
    differential: int,
    kd_time_pos: int,
    kout_pos: int,
    kaff_pos: int,
    pos_err_lim: int,
) -> bytes:
    data = struct.pack(
        "<3HL5HL2H",
        chan_ident,
        kp_pos,
        integral,
        i_lim_pos,
        differential,
        kd_time_pos,
        kout_pos,
        kaff_pos,
        pos_err_lim,
        0,
        0,
    )
    return _pack(0x04D7, dest, source, data=data)


def mot_req_positionloopparams(dest: int, source: int, chan_ident: int):
    return _pack(0x04D8, dest, source, param1=chan_ident)


def mot_set_motoroutputparams(
    dest: int,
    source: int,
    chan_ident: int,
    cont_current_lim: int,
    energy_lim: int,
    motor_lim: int,
    motor_bias: int,
) -> bytes:
    data = struct.pack(
        "<7H", chan_ident, cont_current_lim, energy_lim, motor_lim, motor_bias, 0, 0
    )
    return _pack(0x04DA, dest, source, data=data)


def mot_req_motoroutputparams(dest: int, source: int, chan_ident: int):
    return _pack(0x04DB, dest, source, param1=chan_ident)


def mot_set_tracksettleparams(
    dest: int,
    source: int,
    chan_ident: int,
    time: int,
    settle_window: int,
    track_window: int,
) -> bytes:
    data = struct.pack("<6H", chan_ident, time, settle_window, track_window, 0, 0)
    return _pack(0x04E0, dest, source, data=data)


def mot_req_tracksettleparams(dest: int, source: int, chan_ident: int):
    return _pack(0x04E1, dest, source, param1=chan_ident)


def mot_set_profilemodeparams(
    dest: int, source: int, chan_ident: int, mode: int, jerk: int
) -> bytes:
    data = struct.pack("<HHLHH", chan_ident, mode, jerk, 0, 0)
    return _pack(0x04E3, dest, source, data=data)


def mot_req_profilemodeparams(dest: int, source: int, chan_ident: int):
    return _pack(0x04E4, dest, source, param1=chan_ident)


def mot_set_joystickparams(
    dest: int,
    source: int,
    chan_ident: int,
    gear_high_max_vel: int,
    gear_low_accn: int,
    gear_high_accn: int,
    dir_sense: int,
) -> bytes:
    data = struct.pack(
        "<H4LH", chan_ident, gear_high_max_vel, gear_low_accn, gear_high_accn, dir_sense
    )
    return _pack(0x04E6, dest, source, data=data)


def mot_req_joystickparams(dest: int, source: int, chan_ident: int):
    return _pack(0x04E7, dest, source, param1=chan_ident)


def mot_set_currentloopoarams(
    dest: int,
    source: int,
    chan_ident: int,
    phase: int,
    kp_current: int,
    ki_current: int,
    i_lim_current: int,
    i_dead_band: int,
    kff: int,
) -> bytes:
    data = struct.pack(
        "<9H",
        chan_ident,
        phase,
        kp_current,
        ki_current,
        i_lim_current,
        i_dead_band,
        kff,
        0,
        0,
    )
    return _pack(0x04D4, dest, source, data=data)


def mot_req_currentloopoarams(dest: int, source: int, chan_ident: int):
    return _pack(0x04D5, dest, source, param1=chan_ident)


def mot_set_settledcurrentloopparams(
    dest: int,
    source: int,
    chan_ident: int,
    phase: int,
    kp_settled: int,
    ki_settled: int,
    i_lim_settled: int,
    i_dead_band_settled: int,
    kff_settled: int,
) -> bytes:
    data = struct.pack(
        "<9H",
        chan_ident,
        phase,
        kp_settled,
        ki_settled,
        i_lim_settled,
        i_dead_band_settled,
        kff_settled,
        0,
        0,
    )
    return _pack(0x04E9, dest, source, data=data)


def mot_req_settledcurrentloopparams(dest: int, source: int, chan_ident: int):
    return _pack(0x04EA, dest, source, param1=chan_ident)


def mot_set_stageaxisparams(
    dest: int,
    source: int,
    chan_ident: int,
    stage_id: int,
    axis_id: int,
    part_no_axis: int,
    serial_num: int,
    counts_per_unit: int,
    min_pos: int,
    max_pos: int,
    max_accn: int,
    max_dec: int,
    max_vel: int,
) -> bytes:
    data = struct.pack(
        "<HHH16sLL5l4H4L",
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
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    return _pack(0x04F0, dest, source, data=data)


def mot_req_stageaxisparams(dest: int, source: int, chan_ident: int):
    return _pack(0x04F1, dest, source, param1=chan_ident)


def mot_set_tssactuatortype(dest: int, source: int, actuator_ident: int):
    return _pack(0x04FE, dest, source, param1=actuator_ident)


def mot_ack_dcstatusupdate(dest: int, source: int) -> bytes:
    return _pack(0x0492, dest, source)


def mot_req_statusupdate(dest: int, source: int, chan_ident: int):
    return _pack(0x0480, dest, source, param1=chan_ident)


def mot_suspend_endofmovemsges(dest: int, source: int):
    return _pack(0x046B, dest, source)


def mot_resume_endofmovemsges(dest: int, source: int):
    return _pack(0x046C, dest, source)


def mot_set_trigger(dest: int, source: int, chan_ident: int, mode: int) -> bytes:
    # Bitfield
    return _pack(0x0500, dest, source, param1=chan_ident, param2=mode)


def mot_req_trigger(dest: int, source: int, chan_ident: int):
    return _pack(0x0501, dest, source, param1=chan_ident)


def mot_set_kcubemmiparams(
    dest: int,
    source: int,
    chan_ident: int,
    mode: int,
    max_vel: int,
    accn: int,
    dir_sense: int,
    pre_set_pos1: int,
    pre_set_pos2: int,
    disp_brightness: int,
    disp_timeout: int,
    disp_dim_level: int,
) -> bytes:
    data = struct.pack(
        "<HHllHll3H",
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
    )
    return _pack(0x0520, dest, source, data=data)


def mot_req_kcubemmiparams(dest: int, source: int, chan_ident: int):
    return _pack(0x0521, dest, source, param1=chan_ident)


def mot_set_kcubetrigioconfig(
    dest: int,
    source: int,
    chan_ident: int,
    trig1_mode: int,
    trig1_polarity: int,
    trig2_mode: int,
    trig2_polarity: int,
) -> bytes:
    data = struct.pack(
        "<6H", chan_ident, trig1_mode, trig1_polarity, trig2_mode, trig2_polarity, 0
    )
    return _pack(0x0523, dest, source, data=data)


def mot_req_kcubetrigconfig(dest: int, source: int, chan_ident: int):
    return _pack(0x0524, dest, source, param1=chan_ident)


def mot_set_kcubeposttrigparams(
    dest: int,
    source: int,
    chan_ident: int,
    start_pos_fwd: int,
    interval_fwd: int,
    num_pulses_fwd: int,
    start_pos_rev: int,
    interval_rev: int,
    num_pulses_rev: int,
    pulse_width: int,
    num_cycles: int,
) -> bytes:
    data = struct.pack(
        "<H8l",
        chan_ident,
        start_pos_fwd,
        interval_fwd,
        num_pulses_fwd,
        start_pos_rev,
        interval_rev,
        num_pulses_rev,
        pulse_width,
        num_cycles,
    )
    return _pack(0x0526, dest, source, data=data)


def mot_req_kcubeposttrigparams(dest: int, source: int, chan_ident: int):
    return _pack(0x0527, dest, source, param1=chan_ident)


def mot_set_kcubestloopparams(
    dest: int,
    source: int,
    chan_ident: int,
    loop_mode: int,
    prop: int,
    int: int,
    diff: int,
    pid_clip: int,
    pid_tol: int,
    encoder_const: int,
) -> bytes:
    data = struct.pack(
        "<HH5lL",
        chan_ident,
        loop_mode,
        prop,
        int,
        diff,
        pid_clip,
        pid_tol,
        encoder_const,
    )
    return _pack(0x0529, dest, source, data=data)


def mot_req_kcubestloopparams(dest: int, source: int, chan_ident: int):
    return _pack(0x052A, dest, source, param1=chan_ident)


def mot_set_mmf_operparams(
    dest: int,
    source: int,
    chan_ident: int,
    i_tranit_time: int,
    i_transit_time_adc: int,
    oper_mode1: int,
    sig_mode1: int,
    pulse_width1: int,
    oper_mode2: int,
    sig_mode2: int,
    pulse_width2: int,
) -> bytes:
    data = struct.pack(
        "<HllHHlHHllL",
        chan_ident,
        i_tranit_time,
        i_transit_time_adc,
        oper_mode1,
        sig_mode1,
        pulse_width1,
        oper_mode2,
        sig_mode2,
        pulse_width2,
        0,
        0,
    )
    return _pack(0x0510, dest, source, data=data)


def mot_req_mmf_operparams(dest: int, source: int, chan_ident: int):
    return _pack(0x0511, dest, source, param1=chan_ident)


def mot_set_sol_operatingmode(
    dest: int, source: int, chan_ident: int, mode: int
) -> bytes:

    return _pack(0x04C0, dest, source, param1=chan_ident, param2=mode)


def mot_req_sol_operatingmode(dest: int, source: int, chan_ident: int) -> bytes:

    return _pack(0x04C1, dest, source, param1=chan_ident)


def mot_set_sol_cycleparams(
    dest: int, source: int, chan_ident: int, off_time: int, num_cycles: int
) -> bytes:
    data = struct.pack("<H3l", chan_ident, off_time, num_cycles)
    return _pack(0x04C3, dest, source, data=data)


def mot_req_sol_cycleparams(dest: int, source: int, chan_ident: int):
    return _pack(0x04C4, dest, source, param1=chan_ident)


def mot_set_sol_interlockmode(
    dest: int, source: int, chan_ident: int, mode: bool
) -> bytes:
    return _pack(0x04C6, dest, source, param1=chan_ident, param2=1 if mode else 2)


def mot_req_sol_interlockmode(dest: int, source: int, chan_ident: int):
    return _pack(0x04C7, dest, source, param1=chan_ident)


def mot_set_sol_state(dest: int, source: int, chan_ident: int, state: bool) -> bytes:
    return _pack(0x04CB, dest, source, param1=chan_ident, param2=1 if state else 2)


def mot_req_sol_state(dest: int, source: int, chan_ident: int):
    return _pack(0x04CC, dest, source, param1=chan_ident)
