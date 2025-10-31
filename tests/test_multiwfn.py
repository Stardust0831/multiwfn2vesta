import unittest
from pathlib import Path
from src.multiwfn_vesta.multiwfn_controller import MultiwfnController

class TestMultiwfn(unittest.TestCase):
    def setUp(self):
        self.controller = MultiwfnController()
    
    def test_command_generation(self):
        commands = self.controller._build_commands('electron', 'test.cube')
        self.assertIn('5', commands)
        self.assertIn('test.cube', commands)

if __name__ == '__main__':
    unittest.main()