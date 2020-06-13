# Thorlabs APT protocol

A functional implementation of the [Thorlabs APT protocol](https://www.thorlabs.com/Software/Motion%20Control/APT_Communications_Protocol.pdf)

## Outgoing messages

Outgoing messages are python functions in the top level namespace.
Each function has parameters relevant to the particular message, all messages have source and dest parameters.
The function names are lower-cased from the names in the documentation and the "MGMSG_" has been omitted.
These functions return bytes, they do not send the message over the transport layer

For example:

```python
>>> import thorlabs_apt_protocol as apt
>>> 
>>> apt.mot_move_home(source=1, dest=0x50 ,chan_ident=1)
b'C\x04\x01\x00P\x01'
>>> apt.mot_move_absolute(source=1, dest=0x50, chan_ident=1, position=2048)
b'S\x04\x06\x00\xd0\x01\x01\x00\x00\x08\x00\x00'
```

## Incoming messages

Functions which allow for parsing bytes into dictionaries are also provided, but are not imported into the top level namespace by default.
The recommended way of parsing is to use the provided `Unpacker` object.

This object takes a file-like object (such as a pyserial `Serial` instance) and provides a generator to parse the incomming messages.
If no file object is provided, and internal `BytesIO` instance is used, and can be provided with bytes via the `feed` method.
The generator yields `namedtuple` instances.

Usage with pyserial:

```python
>>> import thorlabs_apt_protocol as apt
>>> import serial
>>> 
>>> port = serial.Serial("/dev/ttyUSB0", 115200, rtscts=True)
>>> port.rts = True
>>> port.reset_input_buffer()
>>> port.reset_output_buffer()
>>> port.rts = False
>>> port.write(apt.hw_no_flash_programming(source=1, dest=0x50))
>>> unpacker = apt.Unpacker(port)
>>> for msg in unpacker:
...     print(msg)
... 
>>> 
```

On Windows, you must toggle a driver setting to make the COM port appear:

Within Device Manager, right click on the APT device (under USB devices), and go to `Properties`.
On the `Advanced` tab, check the box that says `Load VCP` (VCP stands for Virtual COM Port).
Unplug and replug the USB cable to make it load the COM Port.