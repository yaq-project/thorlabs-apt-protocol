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
    chan_ident, position, velocity, _, status_bits = struct.unpack_from("<HlHHL", data, HEADER_SIZE)
    ret = {
            "chan_ident": chan_ident,
            "position": position, 
            "velocity": velocity,
            }
    ret.update(_parse_status_bits(status_bits))
    return ret

def _parse_status_bits(status_bits: int) -> Dict[str, Any]:
    # Bitfield
    return {
            "forward_limit_switch": bool(status_bits & 0x1),
            "reverse_limit_switch": bool(status_bits & 0x2),
            "moving_forward": bool(status_bits & 0x10),
            "moving_reverse": bool(status_bits & 0x20),
            "jogging_forward": bool(status_bits & 0x40),
            "jogging_reverse": bool(status_bits & 0x80),
            "homing": bool(status_bits & 0x200),
            "homed": bool(status_bits & 0x400),
            "tracking": bool(status_bits & 0x1000),
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
    serial_number, model_number, type_, firmware_version*,_, _, hw_version, mod_state, nchs = struct.unpack_from("<l8cH4B60sHHH", data, HEADER_SIZE)
    return {"serial_number": serial_number,
            "model_number": model_number,
            "type": type_,
            "firmware_version": firmware_version,
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
    if bay_ident == 0xff:
        bay_ident = -1
    return {"bay_ident": bay_ident}

@parser(0x0226)
def rack_get_statusbits(data: bytes) -> Dict[str, Any]:
    # Bitfield
    status_bits = struct.unpack_from("<L", data, HEADER_SIZE)
    return {
            "digouts": [bool(status_bits & 0x1),
            bool(status_bits & 0x2),
            bool(status_bits & 0x3),
            bool(status_bits & 0x4),
            ]
            }

@parser(0x0230)
def rack_get_digoutputs(data: bytes) -> Dict[str, Any]:
    # Bitfield
    return {
            "digouts": [bool(data[2] & 0x1),
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
    chan_ident, min_velocity, acceleration, max_velocity = struct.unpack_from("<H3l", data, HEADER_SIZE)
    return {"chan_ident": chan_ident, "min_velocity": min_velocity, "acceleration": acceleration, "max_velocity": max_velocity}

@parser(0x0418)
def mot_get_jogparams(data: bytes) -> Dict[str, Any]:
    chan_ident, jog_mode, step_size, min_velocity, acceleration, max_velocity, stop_mode = struct.unpack_from("<HH4lH", data, HEADER_SIZE)
    return {"chan_ident": chan_ident,
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
    return {"adc_input1": adc_input1 * 5 / 2**15, "adc_input2": adc_input2 * 5 / 2 ** 15}

@parser(0x0428)
def mot_get_powerparams(data: bytes) -> Dict[str, Any]:
    chan_ident, rest_factor, move_factor = struct.unpack_from("<3H", data, HEADER_SIZE)
    return {"chan_ident": chan_ident, "rest_factor": rest_factor, "move_factor": move_factor}

@parser(0x043C)
def mot_genmoveparams(data: bytes) -> Dict[str, Any]:
    chan_ident, backlash_distance = struct.unpack_from("<Hl", data, HEADER_SIZE)
    return {"chan_ident": chan_ident, "backlash_distance": backlash_distance}

@parser(0x0447)
def mot_get_moverelparams(data: bytes) -> Dict[str, Any]:
    chan_ident, relative_distance = struct.unpack_from("<Hl", data, HEADER_SIZE)
    return {"chan_ident": chan_ident, "relative_distance": relative_distance}

@parser(0x0447)
def mot_get_moveabsparams(data: bytes) -> Dict[str, Any]:
    chan_ident, absolute_position = struct.unpack_from("<Hl", data, HEADER_SIZE)
    return {"chan_ident": chan_ident, "absolute_position": absolute_position}

@parser(0x0442)
def mot_get_homeparams(data: bytes) -> Dict[str, Any]:
    chan_ident, home_dir, limit_switch, home_velocity, offset_distance = struct.unpack_from("<3Hll", data, HEADER_SIZE)
    return {"chan_ident": chan_ident, "home_dir": home_dir, "limit_switch": limit_switch, "home_velocity": home_velocity, "offset_distance": offset_distance}

@parser(0x0425)
def mot_get_limswitchparams(data: bytes) -> Dict[str, Any]:
    chan_ident, cw_hardlimit, ccw_hardlimit, cw_softlimit, ccw_softlimit, soft_limit_mode = struct.unpack_from("<3HLLH", data, HEADER_SIZE)
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
    chan_ident, proportional, integral, differential, integral_limits, filter_control = struct.unpack_from("<H4LH", data, HEADER_SIZE)
    return {"chan_ident": data[2], "enabled": data[3] == 0x01}

@parser(0x04B5)
def mot_get_avmodes(data: bytes) -> Dict[str, Any]:
    chan_ident, mode_bits = struct.unpack_from("<HH", data, HEADER_SIZE)
    # Bitfield
    return {"chan_ident": chan_ident, "mode_bits": mode_bits}

@parser(0x04B2)
def mot_get_potparams(data: bytes) -> Dict[str, Any]:
    chan_ident, zero_wnd, vel1, wnd1, vel2, wnd2, vel3, wnd3, vel4 = struct.unpack_from("<HHlHlHlHl", data, HEADER_SIZE)
    return {"chan_ident": chan_ident, "zero_wnd": zero_wnd, "vel1": vel1, "wnd1": wnd1, "vel2": vel2, "wnd2": wnd2, "vel3": vel3, "wnd3": wnd3, "vel4": vel4}

@parser(0x04B8)
def mot_get_buttonparams(data: bytes) -> Dict[str, Any]:
    chan_ident, mode, position1, position2, time_out1, time_out2 = struct.unpack_from("<HHllHH", data, HEADER_SIZE)
    return {"chan_ident": chan_ident,
            "mode": mode,
            "position1": position1,
            "position2": position2,
            "time_out1": time_out1,
            "time_out2": time_out2,
            }

@parser(0x0491)
def mot_get_dcstatusupdate(data: bytes) -> Dict[str, Any]:
    return _parse_dcstatus(data)

@parser(0x042A)
def mot_get_statusbits(data: bytes) -> Dict[str, Any]:
    chan_ident, status_bits = struct.unpack_from("<HL", data, HEADER_SIZE)
    ret = {
            "chan_ident": chan_ident,
            }
    ret.update(_parse_status_bits(status_bits))
    # Bitfield
    return ret
    

