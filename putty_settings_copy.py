#!/usr/bin/env python
"""Script to copy PuTTY settings from "Default Settings" to other session profiles.

For example, you can make a change to the color settings in the Default Settings and then copy
those colors over to all of the other session profiles.

Author, Copyright, and License
------------------------------
Copyright (c) 2023-2025 Hauke Daempfling (haukex@zero-g.net)
at the Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB),
Berlin, Germany, https://www.igb-berlin.de/

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see https://www.gnu.org/licenses/
"""
from typing import Any
from winreg import OpenKeyEx, HKEY_CURRENT_USER, KEY_WRITE, QueryInfoKey, EnumKey, EnumValue, SetValueEx
from urllib.parse import unquote
from igbpyutils.iter import is_unique_everseen

# spell-checker: ignore igbpyutils everseen Tatham

DEFAULT_KEY = 'Default%20Settings'
EXCLUDE_KEYS = {'HostName','PortNumber','UserName','Protocol'}

with OpenKeyEx(HKEY_CURRENT_USER, r'SOFTWARE\SimonTatham\PuTTY\Sessions') as main_key:
    def get_session_as_dict(s_key):
        with OpenKeyEx(main_key, s_key) as key:
            session_values = [ EnumValue(key, vi) for vi in range(QueryInfoKey(key)[1]) ]
        session_values.sort()
        assert all(is_unique_everseen( x[0] for x in session_values ))  # no duplicate names
        session_dict :dict[str, tuple[Any, int]] = { name: (data, typ) for name, data, typ in session_values }
        return session_dict
    sessions = [ EnumKey(main_key, si) for si in range(QueryInfoKey(main_key)[0]) ]
    sessions.sort()
    sessions.remove(DEFAULT_KEY)
    defaults = get_session_as_dict(DEFAULT_KEY)
    def_keys = set(defaults.keys())
    for session_key in sessions:
        session_name = unquote(session_key)
        values = get_session_as_dict(session_key)
        cur_keys = set(values.keys())
        if def_keys != cur_keys:
            if diff := def_keys-cur_keys:
                print(f"Keys in default but not in {session_name!r}: {diff}")
            if diff := cur_keys-def_keys:
                print(f"Keys in {session_name!r} but not in default: {diff}")
        for k in sorted( def_keys & cur_keys - EXCLUDE_KEYS ):
            if values[k] != defaults[k]:
                assert values[k][1] == defaults[k][1]  # assume they'll have the same type
                if input(f"{session_name!r} {k!r}: {values[k][0]!r} => {defaults[k][0]!r}? [yN] ").lower().startswith('y'):
                    with OpenKeyEx(main_key, session_key, access=KEY_WRITE) as wr_key:
                        SetValueEx(wr_key, k, 0, defaults[k][1], defaults[k][0])
