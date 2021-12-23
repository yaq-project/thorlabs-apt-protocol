# [Unreleased]

# [29.0.0]

- Correctly offset messages with submsgid to parse the remaining values correctly
- Update parsing of DCStatusupdate to match current version of spec
- correctly handle short dcstatus messages

# [25.2.0]

- Add missing `req_dcstatusupdate` function
- Add data fields to `get_dcpidparams`
- Allow for signed velocity
- Fix name of `mot_get_genmoveparams`
- Convert uint8 to singed char for packing in `mot_set_trigger`
- Unpack richresponse as string rather than tuple of char
- Improve robustness of unpacking

Thanks to Patrick Tapping for providing all of these fixes.

# [25.1.0]

- Fix 3 functions that did not properly encode the parameter data
- Add missing messages related to piezo controllers, laser control, quad, etc

# [25.0.1]

- Switch to flit for packaging

# [25.0.0]

Initial release

Please note that not _all_ of the messages in the protocol are represented at this time
In particular, those related to Piezo controllers, Laser Control, and Quad control are not yet implemented


[Unreleased]: https://gitlab.com/yaq/thorlabs-apt-protocol/-/compare/v29.0.0...main
[29.0.0]: https://gitlab.com/yaq/thorlabs-apt-protocol/-/compare/v25.2.0...v29.0.0
[25.1.0]: https://gitlab.com/yaq/thorlabs-apt-protocol/-/compare/v25.1.0...v25.2.0
[25.1.0]: https://gitlab.com/yaq/thorlabs-apt-protocol/-/compare/v25.0.1...v25.1.0
[25.0.1]: https://gitlab.com/yaq/thorlabs-apt-protocol/-/compare/v25.0.0...v25.0.1
[25.0.0]: https://gitlab.com/yaq/thorlabs-apt-protocol/-/tags/v25.0.0
