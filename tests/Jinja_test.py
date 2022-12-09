import unittest
import DTree
import json

import_obj_instance_hash = {}

class Testing(unittest.TestCase):

    def test_key(self):

        json_file = './jobs/jinja_test/jinja_test.json'
        flask_data = {}
        import_obj_instance = {}
        c = DTree.DTree(json.load(open(json_file)), name=json_file,
                        import_obj_instance=import_obj_instance, data=flask_data)

        # print(c.data)
        assert c.data == {'Key': ['Hello', 'World', 'BAD', 'GOOD', '3BAD', '3GOOD', 'GOOD', 'Hello', 'World', 'BAD', 'GOOD', '3BAD', '3GOOD', 'GOOD']}

if __name__ == '__main__':
    unittest.main()