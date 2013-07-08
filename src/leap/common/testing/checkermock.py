# -*- coding: utf-8 -*-
# checkermock.py
# Copyright (C) 2013 LEAP
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Helper Mock that also checks that the caller args are valid
"""

import inspect

from mock import MagicMock
from leap.common.check import leap_assert


class CalledWithInvalidParams(Exception):
    """
    Exception raised when the CheckerMock detects that a function
    wasn't called with the expected arguments.
    """
    pass


class CheckerMock(MagicMock):
    def __init__(self, check, *args, **kwargs):
        """
        Constructor for CheckerMock

        :param check: function to check parameters against
        :type check: callable
        """
        MagicMock.__init__(self, *args, **kwargs)
        leap_assert(callable(check),
                    "We need a callable function to check against")
        self._check = check

    def __call__(self, *args, **kwargs):
        try:
            inspect.getcallargs(self._check, *args, **kwargs)
        except Exception as e:
            raise CalledWithInvalidParams(e)
        MagicMock.__call__(self, *args, **kwargs)
