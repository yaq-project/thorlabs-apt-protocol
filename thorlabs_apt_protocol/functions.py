from typing import Optional, Sequence
import struct

def _pack(msgid: int, dest: int, source: int, *, param1: int=0, param2: int=0, data: Optional[bytes]=None):
    if data is not None:
        assert param1 == param2 == 0
        return struct.pack("<HHbb", msgid, len(data), dest | 0x80, source) + data
    else:
        return struct.pack("<H4b", msgid, param1, param2, dest, source)

def mod_identify(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0223, dest, source, param1=chan_ident)

def mod_set_chanenablestate(dest: int, source: int, chan_ident: int, enable_state:int) -> bytes:
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

def mod_set_digoutputs(dest: int, source: int, chan_ident: int) -> bytes:
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

def mot_set_velparams(dest: int, source: int, chan_ident: int, min_velocity: int, acceleration: int, max_velocity: int) -> bytes:
    data = struct.pack("<H3l", chan_ident, min_velocity, acceleration, max_velocity)
    return _pack(0x0413, dest, source, data=data)

def mot_req_velparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0414, dest, source, param1=chan_ident)

def mot_set_jogparams(dest: int, source: int, chan_ident: int, jog_mode: int, step_size: int, min_velocity:int , acceleration:int , max_velocity:int , stop_mode: int) -> bytes:
    data = struct.pack("<HH4lH", chan_ident, jog_mode, step_size, min_velocity, acceleration, max_velocity, stop_mode)
    return _pack(0x0416, dest, source, param1=chan_ident)

def mot_req_jogparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0417, dest, source, param1=chan_ident)

def mot_req_adcinputs(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x042B, dest, source, param1=chan_ident)

def mot_set_powerparams(dest: int, source: int, chan_ident: int, rest_factor: int, move_factor: int) -> bytes:
    data = struct.pack("<3H", chan_ident, rest_factor, move_factor)
    return _pack(0x0426, dest, source, data=data)

def mot_req_powerparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0427, dest, source, param1=chan_ident)

def mot_set_genmoveparams(dest: int, source: int, chan_ident: int, backlash_distance: int) -> bytes:
    data = struct.pack("<Hl", chan_ident, backlash_distance)
    return _pack(0x043A, dest, source, data=data)

def mot_req_genmoveparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x043B, dest, source, param1=chan_ident)

def mot_set_moverelparams(dest: int, source: int, chan_ident: int, relative_distance: int) -> bytes:
    data = struct.pack("<Hl", chan_ident, relative_distance)
    return _pack(0x0445, dest, source, data=data)

def mot_req_moverelparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0446, dest, source, param1=chan_ident)


def mot_set_moveabsparams(dest: int, source: int, chan_ident: int, absolute_position: int) -> bytes:
    data = struct.pack("<Hl", chan_ident, absolute_position)
    return _pack(0x0450, dest, source, data=data)

def mot_req_moveabsparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0451, dest, source, param1=chan_ident)

def mot_set_homeparams(dest: int, source: int, chan_ident: int, home_dir: int, limit_switch: int, home_velocity: int, offset_distance: int) -> bytes:
    data = struct.pack("<3Hll", chan_ident, home_dir, limit_switch, home_velocity, offset_distance)
    return _pack(0x0440, dest, source, param1=chan_ident)

def mot_req_homeparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0441, dest, source, param1=chan_ident)

def mot_set_limswitchparams(dest: int, source: int, chan_ident: int, cw_hardlimit: int, ccw_hardlimit: int, cw_softlimit: int, ccw_softlimit: int, sort_limit_mode: int) -> bytes:
    data = struct.pack("<3HLLH", chan_ident, cw_hardlimit, ccw_hardlimit, cw_softlimit, ccw_softlimit, soft_limit_mode)
    return _pack(0x0423, dest, source, data=data)

def mot_req_limswitchparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0424, dest, source, param1=chan_ident)

def mot_move_home(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x0443, dest, source, param1=chan_ident)

def mot_move_relative(dest: int, source: int, chan_ident: int, distance: Optional[int]=None):
    msgid = 0x0448
    if distance is None:
        return _pack(msgid, dest, source, param1=chan_ident)
    else:
        data = struct.pack("<Hl", chan_ident, distance)
        return _pack(msgid, dest, source, data=data)


def mot_move_absolute(dest: int, source: int, chan_ident: int, position: Optional[int]=None):
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

def mot_set_dcpidparams(dest: int, source: int, chan_ident: int, proportional: Optional[int]=None, integral: Optional[int]=None, differential: Optional[int]=None, integral_limit: Optional[int]=None) -> bytes:
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
    data = struct.pack("<H4LH", chan_ident, proportional, integral, differential, integral_limits, filter_control)
    return _pack(0x04A0, dest, source, data=data)

def mot_req_dcpidparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x04A1, dest, source, param1=chan_ident)

def mot_set_avmodes(dest: int, source: int, chan_ident: int, mode_bits: int) -> bytes:
    data = struct.pack("<HH", chan_ident, mode_bits)
    return _pack(0x04B3, dest, source, data=data)

def mot_req_avmodes(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x04B4, dest, source, param1=chan_ident)

def mot_set_potparams(dest: int, source: int, chan_ident: int, zero_wnd: int, vel1: int, wnd1: int, vel2:int, wnd2: int, vel3:int, vel4:int) -> bytes:
    data = struct.pack("<HHlHlHlHl", chan_ident, zero_wnd, vel1, wnd1, vel2, wnd2, vel3, wnd3, vel4)
    return _pack(0x04B0, dest, source, data=data)

def mot_req_potparams(dest: int, source: int, chan_ident: int) -> bytes:
    return _pack(0x04B1, dest, source, param1=chan_ident)

def mot_set_buttonparams(dest: int, source: int, chan_ident: int, mode: int, position1: int, position2: int, time_out1: int, time_out2: int) -> bytes:
    data = struct.pack("<HHllHH", chan_ident, mode, position1, position2, time_out1, time_out2)
    return _pack(0x04B6, dest, source, data=data)

def mot_req_buttonparams(dest: int, source: int, chan_ident: int, msgid_param: int) -> bytes:
    data = struct.pack("<HH", chan_ident, msgid_param)
    return _pack(0x04B9, dest, source, data=data)

def mot_ack_dcstatusupdate(dest: int, source: int) -> bytes:
    return _pack(0x0492, dest, source)

