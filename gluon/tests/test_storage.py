#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit tests for storage.py """

import pickle
import unittest

from gluon.http import HTTP
from gluon.storage import List, Storage, StorageList


class TestStorage(unittest.TestCase):
    """Tests storage.Storage"""

    def test_attribute(self):
        """Tests Storage attribute handling"""

        s = Storage(a=1)

        self.assertEqual(s.a, 1)
        self.assertEqual(s["a"], 1)
        self.assertEqual(s.b, None)

        s.b = 2
        self.assertEqual(s.a, 1)
        self.assertEqual(s["a"], 1)
        self.assertEqual(s.b, 2)
        self.assertEqual(s["b"], 2)

        s["c"] = 3
        self.assertEqual(s.c, 3)
        self.assertEqual(s["c"], 3)

        s.d = list()
        self.assertTrue(s.d is s["d"])

    def test_store_none(self):
        """Test Storage store-None handling
        s.key = None deletes an item
        s['key'] = None sets the item to None
        """

        s = Storage(a=1)

        self.assertTrue("a" in s)
        self.assertFalse("b" in s)
        s.a = None
        # self.assertFalse('a' in s) # how about this?

        s.a = 1
        self.assertTrue("a" in s)
        s["a"] = None
        self.assertTrue("a" in s)
        self.assertTrue(s.a is None)

    def test_item(self):
        """Tests Storage item handling"""

        s = Storage()

        self.assertEqual(s.d, None)
        self.assertEqual(s["d"], None)
        # self.assertRaises(KeyError, lambda x: s[x], 'd')   # old Storage
        s.a = 1
        s["a"] = None
        self.assertEqual(s.a, None)
        self.assertEqual(s["a"], None)
        self.assertTrue("a" in s)

    def test_pickling(self):
        """Test storage pickling"""
        s = Storage(a=1)
        sd = pickle.dumps(s, pickle.HIGHEST_PROTOCOL)
        news = pickle.loads(sd)
        self.assertEqual(news.a, 1)

    def test_getlist(self):
        # usually used with request.vars
        a = Storage()
        a.x = "abc"
        a.y = ["abc", "def"]
        self.assertEqual(a.getlist("x"), ["abc"])
        self.assertEqual(a.getlist("y"), ["abc", "def"])
        self.assertEqual(a.getlist("z"), [])

    def test_getfirst(self):
        # usually with request.vars
        a = Storage()
        a.x = "abc"
        a.y = ["abc", "def"]
        self.assertEqual(a.getfirst("x"), "abc")
        self.assertEqual(a.getfirst("y"), "abc")
        self.assertEqual(a.getfirst("z"), None)

    def test_getlast(self):
        # usually with request.vars
        a = Storage()
        a.x = "abc"
        a.y = ["abc", "def"]
        self.assertEqual(a.getlast("x"), "abc")
        self.assertEqual(a.getlast("y"), "def")
        self.assertEqual(a.getlast("z"), None)


class TestStorageList(unittest.TestCase):
    """Tests storage.StorageList"""

    def test_attribute(self):
        s = StorageList(a=1)

        self.assertEqual(s.a, 1)
        self.assertEqual(s["a"], 1)
        self.assertEqual(s.b, [])
        s.b.append(1)
        self.assertEqual(s.b, [1])


class TestList(unittest.TestCase):
    """Tests Storage.List (fast-check for request.args())"""

    def test_listcall(self):
        a = List((1, 2, 3))
        self.assertEqual(a(1), 2)
        self.assertEqual(a(-1), 3)
        self.assertEqual(a(-5), None)
        self.assertEqual(a(-5, default="x"), "x")
        self.assertEqual(a(-3, cast=str), "1")
        a.append("1234")
        self.assertEqual(a(3), "1234")
        self.assertEqual(a(3, cast=int), 1234)
        a.append("x")
        self.assertRaises(HTTP, a, 4, cast=int)
        b = List()
        # default is always returned when especified
        self.assertEqual(b(0, cast=int, default=None), None)
        self.assertEqual(b(0, cast=int, default=None, otherwise="teste"), None)
        self.assertEqual(b(0, cast=int, default="a", otherwise="teste"), "a")
        # if don't have value and otherwise is especified it will called
        self.assertEqual(b(0, otherwise=lambda: "something"), "something")
        self.assertEqual(b(0, cast=int, otherwise=lambda: "something"), "something")
        # except if default is especified
        self.assertEqual(b(0, default=0, otherwise=lambda: "something"), 0)

    def test_listgetitem(self):
        """Mantains list behaviour."""
        a = List((1, 2, 3))
        self.assertEqual(a[0], 1)
        self.assertEqual(a[::-1], [3, 2, 1])
