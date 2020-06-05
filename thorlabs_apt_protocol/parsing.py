import struct
import functools

id_to_func = {}
HEADER_SIZE = 6

def parser(msgid):
    def wrapper(func):
        @functools.wraps(func)
        def inner(data: bytes):
            msgid_read, _, dest, source = struct.unpack_from("<HHBB", data)
            dest = dest & ~0x80
            assert msgid == msgid_read
            ret = {"msg": func.__name__, "msgid": msgid, "dest": dest, "source": source}
            ret.update(func(data))
            return ret
        id_to_func[msgid] = inner
        return inner
    return wrapper

def _parse_dcstatus(data: bytes):
    chan_ident, position, velocity, _, status_bits = struct.unpack_from("<HlHHL", data, HEADER_SIZE)
    ret = {
            "chan_ident": chan_ident,
            "position": position, 
            "velocity": velocity,
            }
    ret.update(_parse_status_bits(status_bits))
    return ret

def _parse_status_bits(status_bits: int):
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


@parser(0x0491)
def mot_get_dcstatusupdate(data: bytes):
    return _parse_dcstatus(data)

@parser(0x0464)
def mot_move_completed(data: bytes):
    return _parse_dcstatus(data)

@parser(0x0444)
def mot_move_homed(data: bytes):
    return {"chan_ident": data[2]}

@parser(0x042A)
def mot_get_statusbits(data: bytes):
    chan_ident, status_bits = struct.unpack_from("<HL", data, HEADER_SIZE)
    ret = {
            "chan_ident": chan_ident,
            }
    ret.update(_parse_status_bits(status_bits))
    return ret
    

