import unittest
import DTree
import json

import_obj_instance_hash = {}

class Testing(unittest.TestCase):
    def test_string(self):
        a = 'some'
        b = 'some'
        self.assertEqual(a, b)

    def test_boolean(self):
        a = True
        b = True
        self.assertEqual(a, b)

    def test_start(self):

        json_file = './start.json'
        flask_data = {}
        import_obj_instance = {}
        c = DTree.DTree(json.load(open(json_file)), name=json_file,
                        import_obj_instance=import_obj_instance, data=flask_data)

        # print(c.data)
        assert c.data == {'Key': ['Hello', 'World', 'BAD', 'GOOD', '3BAD', '3GOOD', 'GOOD', 'Hello', 'World', 'BAD', 'GOOD', '3BAD', '3GOOD', 'GOOD']}

if __name__ == '__main__':
    unittest.main()