from typing import Optional
import struct

def _pack(msgid: int, dest: int, source: int, *, param1: int=0, param2: int=0, data: Optional[bytes]=None):
    if data is not None:
        assert param1 == param2 == 0
        return struct.pack("<HHbb", msgid, len(data), dest | 0x80, source) + data
    else:
        return struct.pack("<H4b", msgid, param1, param2, dest, source)

def mot_move_home(dest: int, source: int):
    return _pack(0x0443, dest, source)

def mot_move_absolute(dest: int, source: int, chan_ident: int, position: Optional[int]=None):
    msgid = 0x0453
    if position is None:
        return _pack(msgid, dest, source, param1=chan_ident)
    else:
        data = struct.pack("<Hl", chan_ident, position)
        return _pack(msgid, dest, source, data=data)

def hw_yes_flash_programming(dest: int, source: int):
    return _pack(0x0017, dest, source)

def hw_no_flash_programming(dest: int, source: int):
    return _pack(0x0018, dest, source)

def mot_ack_dcstatusupdate(dest: int, source: int):
    return _pack(0x0492, dest, source)

