# -*- coding: utf-8 -*-

# BCDI: tools for pre(post)-processing Bragg coherent X-ray diffraction imaging data
#   (c) 07/2017-06/2019 : CNRS UMR 7344 IM2NP
#   (c) 07/2019-05/2021 : DESY PHOTON SCIENCE
#       authors:
#         Jerome Carnis, carnis_jerome@yahoo.fr

import numpy as np
import unittest
from bcdi.experiment.setup import Setup
from tests.config import run_tests


class Test(unittest.TestCase):
    """Tests related to setup instantiation."""

    def test_instantiation_missing_parameter(self):
        with self.assertRaises(TypeError):
            Setup()


class TestCheckSetup(unittest.TestCase):
    """
    Tests related to check_setup.

        def check_setup(
        self,
        grazing_angle: Optional[Tuple[Real, ...]],
        inplane_angle: Union[Real, np.ndarray],
        outofplane_angle: Union[Real, np.ndarray],
        tilt_angle: np.ndarray,
        detector_distance: Real,
        energy: Union[Real, np.ndarray],
    ) -> None:
    """

    def setUp(self) -> None:
        self.setup = Setup(beamline_name="ID01")
        self.params = {
            "grazing_angle": (1, 2),
            "inplane_angle": 1.23,
            "outofplane_angle": 49.2,
            "tilt_angle": np.array([1, 1.005, 1.01, 1.015]),
            "detector_distance": 0.5,
            "energy": 9000,
        }

    def test_check_setup_distance_predefined(self):
        self.setup.distance = 1.5
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.distance, 1.5)

    def test_check_setup_distance_none(self):
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.distance, self.params["detector_distance"])

    def test_check_setup_distance_undefined(self):
        self.params["detector_distance"] = None
        with self.assertRaises(ValueError):
            self.setup.check_setup(**self.params)

    def test_check_setup_distance_ndarray(self):
        self.params["distance"] = np.array([1, 1.2, 1.4])
        with self.assertRaises(TypeError):
            self.setup.check_setup(**self.params)

    def test_check_setup_energy_predefined(self):
        self.setup.energy = 12000
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.energy, 12000)

    def test_check_setup_energy_none(self):
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.energy, self.params["energy"])

    def test_check_setup_energy_undefined(self):
        self.params["energy"] = None
        with self.assertRaises(ValueError):
            self.setup.check_setup(**self.params)

    def test_check_setup_energy_ndarray(self):
        self.params["energy"] = np.array([10.005, 10.010, 10.015])
        with self.assertRaises(TypeError):
            self.setup.check_setup(**self.params)

    def test_check_setup_tilt_angle_predefined(self):
        self.setup.tilt_angle = 2
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.tilt_angle, 2)

    def test_check_setup_tilt_angle_none(self):
        self.setup.check_setup(**self.params)
        correct = np.mean(
            self.params["tilt_angle"][1:] - self.params["tilt_angle"][:-1]
        )
        self.assertEqual(self.setup.tilt_angle, correct)

    def test_check_setup_tilt_angle_undefined(self):
        self.params["tilt_angle"] = None
        with self.assertRaises(ValueError):
            self.setup.check_setup(**self.params)

    def test_check_setup_outofplane_angle_predefined(self):
        self.setup.outofplane_angle = 2
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.outofplane_angle, 2)

    def test_check_setup_outofplane_angle_none(self):
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.outofplane_angle, self.params["outofplane_angle"])

    def test_check_setup_outofplane_angle_ndarray(self):
        self.params["outofplane_angle"] = np.arange(10)
        with self.assertRaises(TypeError):
            self.setup.check_setup(**self.params)

    def test_check_setup_outofplane_angle_undefined(self):
        self.params["outofplane_angle"] = None
        with self.assertRaises(ValueError):
            self.setup.check_setup(**self.params)

    def test_check_setup_inplane_angle_predefined(self):
        self.setup.inplane_angle = 2
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.inplane_angle, 2)

    def test_check_setup_inplane_angle_none(self):
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.inplane_angle, self.params["inplane_angle"])

    def test_check_setup_inplane_angle_ndarray(self):
        self.params["inplane_angle"] = np.arange(10)
        with self.assertRaises(TypeError):
            self.setup.check_setup(**self.params)

    def test_check_setup_inplane_angle_undefined(self):
        self.params["inplane_angle"] = None
        with self.assertRaises(ValueError):
            self.setup.check_setup(**self.params)

    def test_check_setup_grazing_angle_predefined(self):
        self.setup.grazing_angle = (0.1,)
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.grazing_angle, self.params["grazing_angle"])

    def test_check_setup_grazing_angle_None(self):
        self.setup.grazing_angle = (0.1,)
        self.params["grazing_angle"] = None
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.grazing_angle, None)


class TestCorrectDirectBeam(unittest.TestCase):
    """
    Tests related to correct_direct_beam.

    def correct_direct_beam(
            self, direct_beam: Optional[List[Real]]
    ) -> Optional[Tuple[Real, ...]]:
    """

    def setUp(self) -> None:
        self.setup = Setup(
            beamline_name="ID01",
            direct_beam=[12, 324],
            dirbeam_detector_angles=[-1, 1],
            distance=1.23,
        )

    def test_direct_beam_none(self):
        self.setup.direct_beam = None
        self.assertTrue(self.setup.correct_direct_beam() is None)

    def test_dirbeam_detector_angles_none(self):
        self.setup.dirbeam_detector_angles = None
        self.assertEqual(
            self.setup.correct_direct_beam(), tuple(self.setup.direct_beam)
        )

    def test_dirbeam_detector_angles_not_none(self):
        self.assertTrue(
            np.allclose(
                self.setup.correct_direct_beam(),
                (402.3190872641864, -66.31908726418641),
                rtol=1e-09,
                atol=1e-09,
            )
        )


class TestCorrectDetectorAngles(unittest.TestCase):
    """
    Tests related to correct_direct_beam.

    def correct_detector_angles(self, bragg_peak_position: Tuple[Real, Real]) -> None:
    """

    def setUp(self) -> None:
        self.setup = Setup(
            beamline_name="ID01",
            direct_beam=[12, 324],
            dirbeam_detector_angles=[0.5, 1],
            distance=1.23,
            inplane_angle=12.2,
            outofplane_angle=34.5,
        )

    def test_direct_beam_none(self):
        self.setup.direct_beam = None
        output = self.setup.correct_detector_angles(bragg_peak_position=(165, 35))
        self.assertTrue(
            np.isclose(self.setup.inplane_angle, 12.2)
            and np.isclose(self.setup.outofplane_angle, 34.5)
            and output is None
        )

    def test_dirbeam_detector_angles_none(self):
        self.setup.dirbeam_detector_angles = None
        output = self.setup.correct_detector_angles(bragg_peak_position=(165, 35))
        self.assertTrue(
            np.isclose(self.setup.inplane_angle, 12.2)
            and np.isclose(self.setup.outofplane_angle, 34.5)
            and output is None
        )

    def test_distance_undefined(self):
        self.setup.distance = None
        with self.assertRaises(ValueError):
            self.setup.correct_detector_angles(bragg_peak_position=(165, 35))

    def test_inplane_undefined(self):
        self.setup.inplane_angle = None
        with self.assertRaises(ValueError):
            self.setup.correct_detector_angles(bragg_peak_position=(165, 35))

    def test_outofplane_undefined(self):
        self.setup.outofplane_angle = None
        with self.assertRaises(ValueError):
            self.setup.correct_detector_angles(bragg_peak_position=(165, 35))

    def test_bragg_peak_none(self):
        output = self.setup.correct_detector_angles(bragg_peak_position=None)
        self.assertTrue(
            np.isclose(self.setup.inplane_angle, 12.2)
            and np.isclose(self.setup.outofplane_angle, 34.5)
            and output is None
        )

    def test_correct(self):
        self.setup.correct_detector_angles(bragg_peak_position=(165, 35))
        print(self.setup.inplane_angle, self.setup.outofplane_angle)
        self.assertTrue(
            np.isclose(self.setup.inplane_angle, 11.940419849886538)
            and np.isclose(self.setup.outofplane_angle, 33.6080130206483)
        )


class TestRepr(unittest.TestCase):
    """Tests related to __repr__."""

    def setUp(self) -> None:
        self.setup = Setup(beamline_name="ID01")

    def test_return_type(self):
        self.assertIsInstance(eval(repr(self.setup)), Setup)

    def test_rocking_angle_str(self):
        self.setup.rocking_angle = "outofplane"
        self.assertIsInstance(eval(repr(self.setup)), Setup)


if __name__ == "__main__":
    run_tests(Test)
    run_tests(TestCheckSetup)
    run_tests(TestCorrectDirectBeam)
    run_tests(TestCorrectDetectorAngles)
    run_tests(TestRepr)
