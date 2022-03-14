import unittest
from jija.utils import collector
from ..test_data.utils import collector_data


class CollectorTests(unittest.TestCase):
    def test_collect_subclasses(self):
        subclasses = collector.collect_subclasses(collector_data, collector_data.TestData)

        self.assertTrue(isinstance(subclasses, map))
        self.assertEqual(list(subclasses), [collector_data.AData, collector_data.BData])
