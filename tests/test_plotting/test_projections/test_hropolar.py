import unittest
import matplotlib.pyplot as plt

import hrosailing.plotting.projections
from hrosailing.polardiagram import PolarDiagramTable

class TestHROPolar(unittest.TestCase):
    def setUp(self) -> None:
        self.pd = PolarDiagramTable([1, 2, 3], [0, 90, 180], [[0,1,2], [1,2,3], [2,3,4]])

    def test_prepare_plot(self):
        #Execution Test
        ax = plt.subplot(projection="hro polar")
        ax._prepare_plot((self.pd,), [1,2,3], 20, ("black", "white"), True, {"location": "left"}, marker="H")

    def test_plot_polar_diagram(self):
        # Execution Test
        ax = plt.subplot(projection="hro polar")
        ax.plot(
            self.pd,
            ws=[1, 2],
            n_steps=1,
            colors=("green", "red"),
            show_legend=True,
            legend_kw={"location": "left"},
            use_convex_hull=False,
            marker="H"
        )

    def test_plot_other(self):
        # Execution test
        ax = plt.subplot(projection = "hro polar")
        ax.plot([1, 2, 3], [1, 2, 3], ls="--", marker="H")

    def test_scatter_polar_diagram(self):
        # Execution test
        ax = plt.subplot(projection = "hro polar")
        ax.scatter(
            self.pd,
            ws=[1, 2],
            n_steps=1,
            colors=("green", "red"),
            show_legend=True,
            legend_kw={"location": "left"},
            use_convex_hull=False,
            marker="H"
        )

    def test_scatter_other(self):
        # Execution test
        ax = plt.subplot(projection = "hro polar")
        ax.scatter([1, 2, 3], [1, 2, 3], ls="--", marker="H")
