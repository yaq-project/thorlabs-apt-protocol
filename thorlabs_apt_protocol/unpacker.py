__all__ = ["Unpacker"]

from collections import namedtuple
import io
import struct
import warnings

from .parsing import id_to_func

class Unpacker:

    def __init__(self, file_like=None):
        if file_like is None:
            self._file = io.BytesIO() 
        else:
            self._file = file_like

    def __iter__(self):
        return self

    def __next__(self):
        try:
            pos = self._file.tell()
            header = self._file.read(6)
            long_form = header[4] & 0x80
            msgid, length = struct.unpack_from("<HH", header)
            data = header
            if long_form:
                data = header + self._file.read(length)
        except:
            self._file.seek(pos)
            raise StopIteration
        try:
            dict_ = id_to_func[msgid](data)
        except KeyError:
            warnings.warn(f"Msgid: {hex(msgid)} not recognized")
            dict_ = {"msg": "unknown", "msgid": msgid}
            
        return namedtuple(dict_["msg"], dict_.keys())(**dict_)

    def feed(self, data: bytes):
        pos = self._file.tell()
        self._file.seek(0, 2)
        self._file.write(data)
        self._file.seek(pos)
