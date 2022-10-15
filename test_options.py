import unittest
from options import *

class TestSum_option(unittest.TestCase):

    def test_init(self):

        __set = set()
        __test = opt('alpha', oset=__set)
        self.assertTrue(__test in __set)

    def test_str(self):

        __test = opt('bravo', oset=set())
        self.assertEqual(str(__test), 'bravo')

    def test_hash(self):

        __test = opt('charlie', oset=set())
        self.assertEqual(hash(__test), hash(str(__test)))

    def test_iter(self):

        __short_names = ['d', 'del', 'D']
        __test = opt('delta', *__short_names, oset=set())

        __test_iter_list = []
        for __x in __test:
            __test_iter_list.append(__x)

        self.assertEqual(__short_names, __test_iter_list)

    def test_next(self):

        __short_names = ['e', 'eo', 'E']
        __test = opt('echo', *__short_names, oset=set())

        __s_iter = iter(__short_names)
        __t_iter = iter(__test)

        for _ in range(len(__short_names)):
            __a = next(__s_iter)
            __b = next(__t_iter)
            self.assertEqual(__a, __b)

        self.assertRaises(StopIteration, next, __t_iter)


class TestSum_translation(unittest.TestCase):

    test_args = 'script.py arg1 arg2 -b ba1 ba2 -c --delta da1'.split(' ')
    o_set = set()
    opt('bravo', 'b', oset=o_set)
    opt('charlie', 'c', oset=o_set)
    opt('delta', 'd', oset=o_set)

    def test_prefix(self):

        __test = translation([], '-', oset=set())
        __r = __test._pref('a')
        self.assertEqual(__r, '--a')

    def test_isset(self):

        __test = translation([], '-', oset=set())
        __test._translation__d_args = {'--bravo': ['ba1', 'ba2'], '--charlie': [], '--delta': ['da1']}
        self.assertTrue(__test.isset('bravo'))
        self.assertFalse(__test.isset('alpha'))

    def test_len(self):

        __test = translation([], '-', oset=set())
        __test._translation__d_args = {'--bravo': ['ba1', 'ba2'], '--charlie': [], '--delta': ['da1']}

        self.assertEqual(__test.len('bravo'), 2)
        self.assertEqual(__test.len('charlie'), 0)
        self.assertEqual(__test.len('alpha'), -1)

    def test_values(self):

        __test = translation([], '-', oset=set())
        __test._translation__d_args = {'--bravo': ['ba1', 'ba2'], '--charlie': [], '--delta': ['da1']}

        self.assertEqual(__test.values('bravo'), ['ba1', 'ba2'])
        self.assertEqual(__test.values('charlie'), [])
        self.assertEqual(__test.values('alpha'), None)

    def test_translate(self):

        __test = translation([], '-', oset=set())

        translation._translate(__test, self.test_args)

        self.assertEqual(__test.p_args, ['script.py', 'arg1', 'arg2'])
        self.assertEqual(__test.d_args, {'-b': ['ba1', 'ba2'], '-c': [], '--delta': ['da1']})

    def test_replace_to_long(self):

        __test = translation([], '-', oset=self.o_set)
        __d = {'-b': ['ba1', 'ba2'], '-c': [], '--delta': ['da1']}
        __test._replace_to_long(__d)
        self.assertEqual(__d, {'--bravo': ['ba1', 'ba2'], '--charlie': [], '--delta': ['da1']})

    def test_update(self):

        self.test_replace_to_long()

    def test_init(self):
            
        __test = translation(self.test_args, '-', oset=self.o_set)
        self.assertEqual(__test.p_args, ['script.py', 'arg1', 'arg2'])
        self.assertEqual(__test.d_args, {'--bravo': ['ba1', 'ba2'], '--charlie': [], '--delta': ['da1']})


if __name__ == "__main__":
	unittest.main()