import unittest
import DTree
import json

import_obj_instance_hash = {}


class Testing(unittest.TestCase):

    def test_jinja(self):

        json_file = "./jobs/jinja_test/jinja_test.json"
        flask_data = {}
        import_obj_instance = {}
        c = DTree.DTree(json.load(open(json_file)), name=json_file,
                        import_obj_instance=import_obj_instance, data=flask_data)

        print('c.data: ', c.data)
        assert c.data == {
            './jobs/jinja_test/list.json': ['R1', 'R2', 'R3', 'R4', 'R5']}


if __name__ == '__main__':
    unittest.main()
