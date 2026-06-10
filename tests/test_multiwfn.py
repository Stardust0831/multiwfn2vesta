import unittest

from multiwfn2vesta.multiwfn_grid import build_grid_commands, resolve_grid_function

class TestMultiwfn(unittest.TestCase):
    def test_command_generation(self):
        function = resolve_grid_function("density")
        commands = build_grid_commands(function, grid_mode="points", grid_points=(12, 12, 12))
        self.assertEqual(commands, ["5", "1", "4", "12,12,12", "2", "0", "q"])

if __name__ == '__main__':
    unittest.main()
