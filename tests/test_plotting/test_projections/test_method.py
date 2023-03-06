import unittest

import numpy as np

import matplotlib.pyplot as plt

from hrosailing.plotting.projections import _plot, _get_convex_hull
from tests.test_plotting.image_testcase import ImageTestcase


class TestPlot(ImageTestcase):
    def setUp(self) -> None:
        self.slices = [
            np.array([
                [1, 1, 1, 1, 1, 1], [0, 45, 90, 180, 270, 315], [1, 2, 2, 2, 2, 2]
            ]),
            np.array([
                [2, 2, 2, 2, 2, 2], [0, 45, 90, 180, 270, 315], [10, 1, 2, 2, 2, 1]
            ])
        ]
        self.wa_rad = [0, np.pi/4, np.pi/2, np.pi, 3*np.pi/2, 7*np.pi/4]
        self.info = [
            ["A", "A", "B", "B", "B", "B"],
            ["A", "B", "A", "B", "A", "B"]
        ]

    def test_regular(self):
        #Input/Output Test

        #creating resulting plot
        ax = plt.subplot()
        _plot(ax, self.slices, None, False)
        self.set_result_plot()

        #creating expected plot
        plt.plot([0, 45, 90, 180, 270, 315], [1, 2, 2, 2, 2, 2])
        plt.plot([0, 45, 90, 180, 270, 315], [10, 1, 2, 2, 2, 1])
        self.set_expected_plot()

        self.assertPlotsEqual()

    def test_different_axis(self):
        #Input/Output plot with other `ax`
        ax = plt.subplot(projection = "polar")
        _plot(ax, self.slices, None, False)
        self.set_result_plot()

        ax = plt.subplot(projection="polar")
        ax.plot(self.slices)
        self.set_expected_plot()

        self.assertPlotsEqual()

    def test_using_info(self):
        # Input/Output Tests with `info != None`
        #creating resulting plot
        ax = plt.subplot()
        _plot(ax, self.slices, self.info, False)
        self.set_result_plot()

        #creating expected plot
        plt.plot([0, 45], [1, 2], color="C0")
        plt.plot([90, 180, 270, 315], [2, 2, 2, 2], color="C0")
        plt.plot([0, 90, 270], [10, 2, 2], color="C1")
        plt.plot([45, 180, 315], [1, 2, 1], color="C1")
        self.set_expected_plot()

        self.assertPlotsEqual()

    def test_using_radians(self):
        # Input/Output test with `use_radians = True`
        #creating resulting plot
        ax = plt.subplot()
        _plot(ax, self.slices, None, True)
        self.set_result_plot()

        #creating expected plot
        plt.plot([0, np.pi/4, np.pi/2, np.pi, 3*np.pi/2, 7*np.pi/4], [1, 2, 2, 2, 2, 2])
        plt.plot([0, np.pi/4, np.pi/2, np.pi, 3*np.pi/2, 7*np.pi/4], [10, 1, 2, 2, 2, 1])
        self.set_expected_plot()

        self.assertPlotsEqual()

    def test_using_convex_hull(self):
        # Input/Output test with `use_convex_hull = True`
        # creating resulting plot
        ax = plt.subplot()
        _plot(ax, self.slices, None, False, use_convex_hull=True)
        self.set_result_plot()

        # creating expected plot
        plt.plot([0, 45, 90, 180, 270, 315, 360], [np.sqrt(2), 2, 2, 2, 2, 2, np.sqrt(2)])
        plt.plot([0, 90, 180, 270, 360], [10, 2, 2, 2, 10])
        self.set_expected_plot()

        self.assertPlotsEqual()

    def test_using_scatter(self):
        # Input/Output Test with `use_scatter = True`
        ax = plt.subplot()
        _plot(ax, self.slices, None, False, use_convex_hull=False, use_scatter=True)
        self.set_result_plot()

        plt.scatter([0, 45, 90, 180, 270, 315], [1, 2, 2, 2, 2, 2])
        plt.scatter([0, 45, 90, 180, 270, 315], [10, 1, 2, 2, 2, 1])
        self.set_expected_plot()

        self.assertPlotsEqual()

    def test_with_keyword_arguments(self):
        # Input/Output Test using keyword arguments
        ax = plt.subplot()
        _plot(
            ax, self.slices, None, False,
            alpha=0.1,
            color="blue",
            dashes=[0.1, 0.2, 0.1, 0.2],
            linewidth=10,
            marker="H"
        )
        self.set_result_plot()

        plt.plot(
            [0, 45, 90, 180, 270, 315], [1, 2, 2, 2, 2, 2],
            alpha=0.1,
            color="blue",
            dashes=[0.1, 0.2, 0.1, 0.2],
            linewidth=10,
            marker="H"
        )
        plt.plot(
            [0, 45, 90, 180, 270, 315], [10, 1, 2, 2, 2, 1],
            alpha=0.1,
            color="blue",
            dashes=[0.1, 0.2, 0.1, 0.2],
            linewidth=10,
            marker="H"
        )
        self.set_expected_plot()

        self.assertPlotsEqual()


class TestGetConvexHull(unittest.TestCase):
    def setUp(self) -> None:
        self.slice_ = np.array([
            [1, 2, 3, 4, 5, 6],
            [0, 45, 90, 135, 180, 270],
            [1, 1, 0, 1, 1, 1]
        ])

    def assertOutputEqual(self, result, expected):
        ws, wa, bsp, info_ = result
        exp_ws, exp_wa, exp_bsp, exp_info_ = expected
        np.testing.assert_array_equal(
            ws, exp_ws,
            err_msg="Wind speeds not as expected!"
        )
        np.testing.assert_array_equal(
            wa, exp_wa,
            err_msg="Wind angles not as expected!"
        )
        np.testing.assert_array_equal(
            bsp, exp_bsp,
            err_msg="Boat speeds not as expected!"
        )
        self.assertEqual(
            info_, exp_info_,
            msg="Info not as expected!"
        )

    def test_ValueError_in_ConvexHull(self):
        # Input/Output Test with Input causing a `ValueError` in the
        # application of `ConvexHull`
        slice_ = np.array([
            [],
            [],
            []
        ])
        result = _get_convex_hull(slice_, None)
        expected = (
            np.array([]),
            np.array([]),
            np.array([]),
            None
        )
        self.assertOutputEqual(result, expected)

    def test_QHullError_in_ConvexHull(self):
        # Input/Output Test with Input causing a `QHullError` in the
        # application of `ConvexHull`
        slice_ = np.array([
            [1, 2],
            [0, 315],
            [1, 1]
        ])
        result = _get_convex_hull(slice_, None)
        expected = (
            np.array([1, 2]),
            np.array([0, 315]),
            np.array([1, 1]),
            None
        )
        self.assertOutputEqual(result, expected)

    # Input/Output Test with relevant wa at 0 and 360
    def test_wa_given_at_0_and_360(self):
        slice_ = np.array([
            [1, 2, 3],
            [0, 315, 360],
            [1, 1, 2]
        ])
        result = _get_convex_hull(slice_, None)
        expected = (
            np.array([1, 2, 3]),
            np.array([0, 315, 360]),
            np.array([1, 1, 2]),
            None
        )
        self.assertOutputEqual(result, expected)

    def test_first_and_last_wa_less_than_180_apart(self):
        # Input/Output test with smallest and biggest relevant wa less than 180
        # degrees apart
        slice_ = np.array([
            [1, 2, 3],
            [0, 45, 135],
            [1, 1, 1]
        ])
        result = _get_convex_hull(slice_, None)
        expected = (
            np.array([1, 2, 3]),
            np.array([0, 45, 135]),
            np.array([1, 1, 1]),
            None
        )
        self.assertOutputEqual(result, expected)

    def test_wa_given_at_0(self):
        #Input/Output test with relevant wa at 0
        slice_ = np.array([
            [1, 2, 3, 4, 5, 6],
            [0, 45, 90, 135, 180, 270],
            [1, 1, 0, 1, 1, 1]
        ])
        result = _get_convex_hull(slice_, None)
        expected = (
            np.array([1, 2, 4, 5, 6, 1]),
            np.array([0, 45, 135, 180, 270, 360]),
            np.array([1, 1, 1, 1, 1, 1]),
            None
        )
        self.assertOutputEqual(result, expected)

    def test_wa_given_at_0_info_not_None(self):
        # Input/Output test with relevant wa at 0 and `info != None`
        slice_ = np.array([
            [1, 2, 3, 4, 5, 6],
            [0, 45, 90, 135, 180, 270],
            [1, 1, 0, 1, 1, 1]
        ])
        info_ = ["A", "B", "A", "B", "A", "B"]
        result = _get_convex_hull(slice_, info_)
        expected = (
            np.array([1, 2, 4, 5, 6, 1]),
            np.array([0, 45, 135, 180, 270, 360]),
            np.array([1, 1, 1, 1, 1, 1]),
            ["A", "B", "B", "A", "B", "A"]
        )
        self.assertOutputEqual(result, expected)

    def test_wa_given_at_360(self):
        # Input/Output Test with relevant wa at 360
        slice_ = np.array([
            [2, 3, 4, 5, 6, 1],
            [45, 90, 135, 180, 270, 360],
            [1, 0, 1, 1, 1, 1]
        ])
        result = _get_convex_hull(slice_, None)
        expected = (
            np.array([1, 2, 4, 5, 6, 1]),
            np.array([0, 45, 135, 180, 270, 360]),
            np.array([1, 1, 1, 1, 1, 1]),
            None
        )
        self.assertOutputEqual(result, expected)

    def test_wa_given_at_360_info_not_None(self):
        # Input/Output Test with relevant wa at 360 and `info != None`
        slice_ = np.array([
            [2, 3, 4, 5, 6, 1],
            [45, 90, 135, 180, 270, 360],
            [1, 0, 1, 1, 1, 1]
        ])
        info_ = ["A", "B", "A", "B", "A", "B"]
        result = _get_convex_hull(slice_, info_)
        expected = (
            np.array([1, 2, 4, 5, 6, 1]),
            np.array([0, 45, 135, 180, 270, 360]),
            np.array([1, 1, 1, 1, 1, 1]),
            ["B", "A", "A", "B", "A", "B"]
        )
        self.assertOutputEqual(result, expected)

    def test_no_wa_at_0_no_wa_at_360_more_than_180_apart(self):
        # Input/Output Test, no relevant wa at 0 or 360
        # smallest and biggest relevant wa is more than 180 apart
        slice_ = np.array([
            [1, 2, 3, 4, 5, 6],
            [0, 45, 90, 180, 270, 315],
            [0, 1, 1, 1, 1, 1]
        ])
        result = _get_convex_hull(slice_, None)
        expected = (
            np.array([4, 2, 3, 4, 5, 6, 4]),
            np.array([0, 45, 90, 180, 270, 315, 360]),
            np.array([1/np.sqrt(2), 1, 1, 1, 1, 1, 1/np.sqrt(2)]),
            None
        )
        self.assertOutputEqual(result, expected)

    def test_no_wa_at_0_no_wa_at_360_more_than_180_apart_info_not_None(self):
        # Input/Output Test, no relevant wa at 0 or 360
        # smallest and biggest relevant wa is more than 180 apart
        # `info != None`
        slice_ = np.array([
            [1, 2, 3, 4, 5, 6],
            [0, 45, 90, 180, 270, 315],
            [0, 1, 1, 1, 1, 1]
        ])
        info_ = ["A", "B", "A", "B", "A", "B"]
        result = _get_convex_hull(slice_, info_)
        expected = (
            np.array([4, 2, 3, 4, 5, 6, 4]),
            np.array([0, 45, 90, 180, 270, 315, 360]),
            np.array([1 / np.sqrt(2), 1, 1, 1, 1, 1, 1 / np.sqrt(2)]),
            [None, "B", "A", "B", "A", "B", None]
        )
        self.assertOutputEqual(result, expected)