# pylint: disable-all

from unittest import TestCase

import numpy as np

import hrosailing.processing.neighbourhood as nbh


class TestScalingBall(TestCase):
    def setUp(self) -> None:
        self.min_pts = 2
        self.norm = lambda x: np.linalg.norm(x, ord=2, axis=1)
        self.pts = [[1, 2], [3, 1], [0.5, 0.5]]

    def test_init_Error(self):
        """
        Negative min_pts causes ValueError.
        """
        with self.assertRaises(ValueError):
            nbh.ScalingBall(min_pts=0)

    def test_repr(self):
        """
        Input/Output-Test.
        """

        result = repr(nbh.ScalingBall(self.min_pts, self.norm))
        expected_result = (
            f"ScalingBall(min_pts={self.min_pts}, norm={self.norm.__name__})"
        )
        self.assertEqual(
            result,
            expected_result,
            f"Expected {expected_result} but got {result}!",
        )

    def test_is_contained_in_custom_min_pts(self):
        """
        Input/Output-Test.
        """

        result = nbh.ScalingBall(self.min_pts).is_contained_in(self.pts)
        expected_result = [True, False, True]
        np.testing.assert_array_equal(
            result,
            expected_result,
            f"Expected {expected_result} but got {result}!",
        )

    def test_is_contained_in_custom_min_pts_custom_norm(self):
        """
        Input/Output-Test.
        """
        result = nbh.ScalingBall(self.min_pts, self.norm).is_contained_in(
            self.pts
        )
        expected_result = [True, False, True]
        np.testing.assert_array_equal(
            result,
            expected_result,
            f"Expected {expected_result} but got {result}!",
        )

    def test_is_contained_in_edge_empty_pts(self):
        """
        EdgeCase: Empty pts.
        """
        result = nbh.ScalingBall(self.min_pts).is_contained_in([])
        expected_result = []
        np.testing.assert_array_equal(
            result,
            expected_result,
            f"Expected {expected_result} but got {result}!",
        )
