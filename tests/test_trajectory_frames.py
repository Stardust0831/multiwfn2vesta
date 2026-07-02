from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import io

from multiwfn2vesta import trajectory_frames


class TestTrajectoryFrames(unittest.TestCase):
    def test_iter_xyz_frames_reads_multiple_frames(self):
        with tempfile.TemporaryDirectory() as tmp:
            traj = Path(tmp) / "traj.xyz"
            traj.write_text(
                "2\n"
                "first\n"
                "C 0 0 0\n"
                "H 0 0 1\n"
                "2\n"
                "second\n"
                "C 0.1 0 0\n"
                "H 0 0 1.1\n",
                encoding="utf-8",
            )

            frames = list(trajectory_frames.iter_xyz_frames(traj))

        self.assertEqual([frame.index for frame in frames], [1, 2])
        self.assertEqual(frames[0].atoms[0].element, "C")
        self.assertEqual(frames[1].atoms[1].coords, (0.0, 0.0, 1.1))

    def test_render_molecule_frame_disables_bonds_without_rules(self):
        frame = trajectory_frames.TrajectoryFrame(
            index=1,
            comment="molecule",
            atoms=(
                trajectory_frames.TrajectoryAtom("C", (0.0, 0.0, 0.0)),
                trajectory_frames.TrajectoryAtom("H", (0.0, 0.0, 1.0)),
            ),
            lattice=None,
        )

        text = trajectory_frames.render_frame_vesta_text(frame, title="case")

        self.assertIn("\nMOLECULE\n", text)
        self.assertIn("C1", text)
        self.assertIn("H1", text)
        self.assertIn("BONDS   0", text)
        self.assertIn("COMPS 0", text)
        self.assertIn("SBOND\n  0 0 0 0\n", text)

    def test_extxyz_lattice_writes_crystal_fractional_coordinates_and_boundary(self):
        frame = next(
            trajectory_frames.iter_xyz_frames(
                self._write_tmp_text(
                    "1\n"
                    'Lattice="10 0 0 0 10 0 0 0 20" Properties=species:S:1:pos:R:3\n'
                    "Cd 5 5 10\n"
                )
            )
        )

        text = trajectory_frames.render_frame_vesta_text(
            frame,
            title="periodic",
            boundary=(-0.05, 1.05, -0.05, 1.05, -0.05, 1.05),
        )

        self.assertIn("\nCRYSTAL\n", text)
        self.assertIn("10.000000 10.000000 20.000000", text)
        self.assertIn("  0.500000   0.500000   0.500000", text)
        self.assertIn("  -0.050   1.050  -0.050   1.050  -0.050   1.050", text)

    def test_bond_rule_writes_sbond_and_enables_bonds(self):
        frame = trajectory_frames.TrajectoryFrame(
            index=1,
            comment="bond",
            atoms=(
                trajectory_frames.TrajectoryAtom("Cd", (0.0, 0.0, 0.0)),
                trajectory_frames.TrajectoryAtom("Cl", (0.0, 0.0, 2.6)),
            ),
            lattice=None,
        )
        rule = trajectory_frames.BondRule("Cd", "Cl", 0.0, 3.5)

        text = trajectory_frames.render_frame_vesta_text(frame, title="cdcl", bond_rules=(rule,))

        self.assertIn("   Cd    Cl    0.00000    3.50000  0  1  1  0  1  0.250  2.000 127 127 127", text)
        self.assertIn("BONDS   1", text)

    def test_write_trajectory_frames_selects_stride_and_writes_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            traj = Path(tmp) / "traj.xyz"
            traj.write_text(
                "1\nf1\nCd 0 0 0\n"
                "1\nf2\nCd 0 0 1\n"
                "1\nf3\nCd 0 0 2\n",
                encoding="utf-8",
            )
            out = Path(tmp) / "out"

            result = trajectory_frames.write_trajectory_frames(
                traj,
                out,
                start=1,
                stop=3,
                stride=2,
                bond_rules=(trajectory_frames.BondRule("Cd", "Cl", 0.0, 3.5),),
            )

            self.assertEqual(result.frame_indices, (1, 3))
            self.assertEqual(len(result.frame_paths), 2)
            self.assertTrue((out / "vesta" / "frame_0001.vesta").exists())
            manifest = result.manifest_path.read_text(encoding="utf-8")
            self.assertIn('"frame_count": 2', manifest)
            self.assertIn('"stride": 2', manifest)
            self.assertIn('"element1": "Cd"', manifest)
            self.assertIn('"bond_radius": 0.25', manifest)
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("Cd-Cl 0-3.5", recipe)
            self.assertIn("The `.vesta` frame files are in", recipe)
            self.assertIn("trajectory-video png_frames trajectory.mp4", recipe)
            self.assertIn("ASE `.traj` reading", recipe)

    def test_reference_vesta_tail_is_reused(self):
        frame = trajectory_frames.TrajectoryFrame(
            index=1,
            comment="ref",
            atoms=(trajectory_frames.TrajectoryAtom("C", (0.0, 0.0, 0.0)),),
            lattice=None,
        )
        with tempfile.TemporaryDirectory() as tmp:
            ref = Path(tmp) / "ref.vesta"
            ref.write_text("#VESTA_FORMAT_VERSION 3.5.4\nSCENE\nREFSCENE\nSTYLE\nBONDS   1\n", encoding="utf-8")

            text = trajectory_frames.render_frame_vesta_text(
                frame,
                title="ref",
                reference_tail=trajectory_frames._tail_from_reference(ref),  # pylint: disable=protected-access
            )

        self.assertIn("REFSCENE", text)
        self.assertTrue(text.rstrip().endswith("BONDS   1"))

    def test_cli_writes_frames(self):
        with tempfile.TemporaryDirectory() as tmp:
            traj = Path(tmp) / "traj.xyz"
            traj.write_text("1\nframe\nCd 0 0 0\n", encoding="utf-8")
            out = Path(tmp) / "out"
            stdout = io.StringIO()

            with patch("sys.stdout", stdout):
                code = trajectory_frames.main([str(traj), str(out), "--bond", "Cd", "Cl", "0", "3.5"])

            self.assertEqual(code, 0)
            self.assertIn("frames=1", stdout.getvalue())
            self.assertTrue((out / "vesta" / "frame_0001.vesta").exists())

    def _write_tmp_text(self, text: str) -> Path:
        tmp = tempfile.NamedTemporaryFile("w", delete=False, suffix=".xyz", encoding="utf-8")
        with tmp:
            tmp.write(text)
        self.addCleanup(lambda: Path(tmp.name).unlink(missing_ok=True))
        return Path(tmp.name)


if __name__ == "__main__":
    unittest.main()
