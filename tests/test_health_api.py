import json
import unittest
from python.health_api import analyze

class HealthTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(analyze([]), {'devices': [], 'device_count': 0})
    def test_hot_hardware_triggers_inspection(self):
        lines = [json.dumps({'device_id': 'node-1', 'sequence': 0, 'temp_c': 82, 'power_w': 190})]
        self.assertEqual(analyze(lines)['devices'][0]['recommended_action'], 'inspect_and_cool')
    def test_latest_sample_wins(self):
        rows = [{'device_id': 'node-1', 'sequence': 1, 'temp_c': 60, 'power_w': 190},
                {'device_id': 'node-1', 'sequence': 0, 'temp_c': 95, 'power_w': 190}]
        self.assertEqual(analyze([json.dumps(r) for r in rows])['devices'][0]['health'], 'healthy')
    def test_power_limit(self):
        row = {'device_id': 'node-2', 'sequence': 0, 'temp_c': 40, 'power_w': 245}
        self.assertEqual(analyze([json.dumps(row)])['devices'][0]['health'], 'degraded')

if __name__=='__main__': unittest.main()
