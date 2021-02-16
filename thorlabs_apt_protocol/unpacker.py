__all__ = ["Unpacker"]

import asyncio
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
        self.buf = b""

    def __iter__(self):
        return self

    def __next__(self):
        try:
            if len(self.buf) < 6:
                self.buf += self._file.read(6 - len(self.buf))
            long_form = self.buf[4] & 0x80
            msgid, length = struct.unpack_from("<HH", self.buf)
            if not long_form:
                length = 0
            if long_form and len(self.buf) < length + 6:
                self.buf += self._file.read(length - len(self.buf) + 6)
            if len(self.buf) < length + 6:
                raise StopIteration
            data = self.buf[: length + 6]
        except:
            raise StopIteration
        try:
            self.buf = self.buf[len(data) :]
            dict_ = id_to_func[msgid](data)
        except KeyError:
            warnings.warn(f"Msgid: {hex(msgid)} not recognized")
            dict_ = {
                "msg": "unknown",
                "msgid": msgid,
                "source": data[5],
                "dest": data[4],
            }
        except:
            print("Unhandled response", data)
            raise StopIteration

        return namedtuple(dict_["msg"], dict_.keys())(**dict_)

    def __aiter__(self):
        return self

    async def __anext__(self):
        while True:
            try:
                return next(self)
            except StopIteration:
                await asyncio.sleep(0.001)

    def feed(self, data: bytes):
        # Must support random access, if it does not, must be fed externally (e.g. serial)
        pos = self._file.tell()
        self._file.seek(0, 2)
        self._file.write(data)
        self._file.seek(pos)
