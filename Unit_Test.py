import unittest
from ToDo import *


class Test_TaskManager(unittest.TestCase):

    def test_todo_completed(self):
        Test1 = ToDo('test', '1', False)
        Test1.completed()
        result2 = Test1.done
        self.assertEqual(result2, True)

    def test_todo_value(self):
        Test1 = ToDo('test', '1', False)
        result = Test1.value()
        self.assertEqual(result, '   -   |   1   | t e s t                     |       -      ')

    def test_todo_com(self):
        Test1 = ToDo('test', '1', False)
        result = Test1.com()
        self.assertEqual(result, [' 1 ', '  -   ', '        -        ', 't e s t'])



if __name__ == '__main__':
    unittest.main()