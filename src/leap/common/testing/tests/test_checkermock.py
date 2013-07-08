# -*- coding: utf-8 -*-
# test_checkermock.py
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
Tests for:
    * leap/common/testing/checkermock.py
"""
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from leap.common.testing import checkermock


def func(a, b):
    return a + b


def func2():
    return 42


def func3(a, b=4):
    return a + b


class Class1(object):
    def somemethod(self, a):
        return 42


class CheckerMockTest(unittest.TestCase):
    def test_raises_with_no_args(self):
        with self.assertRaises(checkermock.CalledWithInvalidParams):
            ch = checkermock.CheckerMock(check=func)
            ch()

    def test_raises_with_some_args(self):
        with self.assertRaises(checkermock.CalledWithInvalidParams):
            ch = checkermock.CheckerMock(check=func)
            ch(1)

    def test_raises_with_wrong_kwarg(self):
        with self.assertRaises(checkermock.CalledWithInvalidParams):
            ch = checkermock.CheckerMock(check=func)
            ch(1, somearg="hello")

    def test_raises_with_class_method(self):
        obj = Class1()
        obj.somemethod = checkermock.CheckerMock(check=obj.somemethod,
                                                 return_value=42)

        with self.assertRaises(checkermock.CalledWithInvalidParams):
            obj.somemethod()

    def test_raises_with_class_method_kwarg(self):
        obj = Class1()
        obj.somemethod = checkermock.CheckerMock(check=obj.somemethod,
                                                 return_value=42)

        with self.assertRaises(checkermock.CalledWithInvalidParams):
            obj.somemethod(someparam="hello")

    def test_succeeds_with_all_args(self):
        ch = checkermock.CheckerMock(check=func, return_value=None)
        ch(1, 3)

    def test_succeeds_with_some_kwargs(self):
        ch = checkermock.CheckerMock(check=func, return_value=None)
        ch(1, b=3)

    def test_succeeds_with_all_kwargs(self):
        ch = checkermock.CheckerMock(check=func, return_value=None)
        ch(b=1, a=3)

    def test_succeeds_with_optional_args(self):
        ch = checkermock.CheckerMock(check=func3, return_value=None)
        ch(1)

    def test_succeeds_with_no_args(self):
        ch = checkermock.CheckerMock(check=func2, return_value=None)
        ch()

    def test_succeeds_with_both_args(self):
        ch = checkermock.CheckerMock(check=func3, return_value=None)
        ch(1, b=4)

    def test_succeeds_with_class_method(self):
        obj = Class1()
        obj.somemethod = checkermock.CheckerMock(check=obj.somemethod,
                                                 return_value=42)

        obj.somemethod(1)
