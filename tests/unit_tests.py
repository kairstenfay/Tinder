import unittest
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.io import read_json

class TestHarvest(unittest.TestCase):

    def setUp(self):
        self.data = read_json()

    def testInstances(self):
        self.assertEqual(self.instances, {
            'target': None,
            'complete_tos': None,
            'complete_kr': None,
            'incomplete_kr': None,
        })

    def testSplit(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
