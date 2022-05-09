import typing
import unittest

class base_case(unittest.TestCase):
    def assertHasAttr(self, obj, attr):
        self.assertTrue(hasattr(obj, attr))

    def assertGetAttr(self, obj, attr, val):
        self.assertHasAttr(obj, attr)
        
        if val is None:
            return
        
        cval = getattr(obj, attr, None)

        if cval is None:
            self.fail("{} is None".format(attr))

        if not(isinstance(val, typing.Iterable) and type(cval) != type(val)):
            return self.assertEqual(cval, val)

        self.assertIn(cval, val)    

    def assertGetAttrMin(self, obj, attr, min, allow_equal=False):
        self.assertHasAttr(obj, attr)
        val = getattr(obj, attr, None)
        if val is None:
            self.fail("{} is None".format(attr))
        
        if not allow_equal:
            self.assertGreater(val, min)
        else:
            self.assertGreaterEqual(val, min)

    def assertGetAttrMax(self, obj, attr, max, allow_equal=False):
        self.assertHasAttr(obj, attr)
        val = getattr(obj, attr, None)
        if val is None:
            self.fail("{} is None".format(attr))

        if not allow_equal:
            self.assertLess(val, max)
        else:
            self.assertLessEqual(val, max)
