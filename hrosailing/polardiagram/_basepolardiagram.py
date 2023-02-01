# pylint: disable=missing-module-docstring

from abc import ABC, abstractmethod
import numpy as np


class PolarDiagramException(Exception):
    """Exception raised if some nonstandard error occurs,
    while doing something with polar diagrams.
    """


class PolarDiagramInitializationException(Exception):
    """Exception raised if an error occurs during
    initialization of a `PolarDiagram`.
    """


class PolarDiagram(ABC):
    """Base class for all polar diagrams.

    Properties
    -----------
    default_slices (abstract) :
        Should set the default windspeeds for `get_slices`.

    Abstract Methods
    ----------------
    to_csv(csv_path)

    __from_csv__(cls, file)

    symmetrize()

    get_slices(ws)

    plot_polar(
        ws,
        ax=None,
        colors=("green", "red"),
        show_legend=False,
        legend_kw=None,
        **plot_kw
    )

    plot_flat(
        ws,
        ax=None,
        colors=("green", "red"),
        show_legend=False,
        legend_kw=None,
        **plot_kw
    )

    plot_3d(ax=None, **plot_kw)

    plot_color_gradient(
        ax=None,
        colors=("green", "red"),
        marker=None,
        ms=None,
        show_legend=False,
        **legend_kw,
    )

    plot_convex_hull(
        ws,
        ax=None,
        colors=("green", "red"),
        show_legend=False,
        legend_kw=None,
        **plot_kw,
    )
    """

    @abstractmethod
    def to_csv(self, csv_path):
        """This method should, given a path, write a .csv file in
        the location, containing human-readable information about the
        polar diagram object that called the method.

        Parameters
        ----------
        csv_path: str
            Path of the created csv file.
        """

    @classmethod
    @abstractmethod
    def __from_csv__(cls, file):
        """"""

    @abstractmethod
    def symmetrize(self):
        """This method should return a new `PolarDiagram` object that is a
        symmetric (i.e. mirrored along the 0 - 180° axis) version of the
        `PolarDiagram` object called the method.
        """

    def get_slices(self, ws=None, n_steps=None, full_info=False, **kwargs):
        """This method should produce a list of 'slices' describing the
        performance of specified wind_speed as well as wind angles and
        corresponding boat speeds, that reflect how the vessel behaves near
        the given wind speeds.

        Parameters
        ----------
        ws : int, float or iterable thereof, optional
            The wind speeds corresponding to the requested slices.

            Defaults to `self.default_slices`

        n_steps : int, optional
            If set, a total of `n_steps` wind_speeds between each value given
            in `ws` is taken into account. For example `n_steps = 1` adds all
            midpoints.

            Defaults to 0.

        full_info : bool, optional
            Specifies wether the additional value `info` will be
            returned or not

            Defaults to `False`.

        **kwargs :
            Additional keyword arguments whose functionality depends on the
            inheriting class. Are forwarded to `ws_to_slices`.

        Returns
        ---------
        labels : np.ndarray
            The wind speeds corresponding to the slices

        slices : list of `numpy.ndarray` of shape (3, *)
            A list of slices.
            A slice stores row wise data points consisting of actual
            wind speed, wind angle and boat speed.
            Note that the actual wind speed can differ (slightly) from the
            wind speed corresponding to the slice, depending on the inheriting
            class.
        """
        ws = self._get_windspeeds(ws, n_steps)
        kwargs["full_info"] = full_info
        slices = self.ws_to_slices(ws, **kwargs)
        if full_info:
            info = self.get_slice_info(ws, slices, **kwargs)
            return ws, slices, info
        return ws, slices

    def _get_windspeeds(self, ws, n_steps):
        if ws is None:
            ws = self.default_slices
        if isinstance(ws, (int, float)):
            return [ws]
        try:
            all_numbers = all([isinstance(ws_, (int, float)) for ws_ in ws])
        except TypeError:
            raise TypeError(
                "`ws` has to be an int a float or an iterable"
            )
        if not all_numbers:
            raise TypeError(
                "If `ws` is an iterable, it needs to iterate over int or float"
            )
        if n_steps is None:
            return np.array(ws)
        if n_steps <= 0:
            raise ValueError("`n_steps` has to be positive")
        return np.concatenate(
            [
                np.linspace(ws_before, ws_next, n_steps + 2)
                for ws_before, ws_next in zip(ws, ws[1:])
            ] + [[ws[-1]]]
        )

    def _get_wind(self, wind):
        if isinstance(wind, np.ndarray):
            if wind.shape[1] == 2:
                return wind
            if wind.shape[0] == 2:
                return wind.T
            raise ValueError(
                 f"`wind` should be a tuple or an array with a dimension of shape 2,\n"
                 f"got an array of shape {wind.shape} instead."
            )
        if isinstance(wind, tuple):
            if len(wind) != 2:
                raise ValueError(
                    f"`wind` should be a tuple of size 2 or an array,\n"
                    f"got a tuple of size {len(wind)} instead."
                )
            ws, wa = wind
            return np.array(list(zip(ws.ravel(), wa.ravel())))
        raise ValueError(
            f"`wind` should be a tuple or an array, got {type(wind)} instead."
        )

    @property
    @abstractmethod
    def default_points(self):
        pass

    @property
    @abstractmethod
    def default_slices(self):
        pass

    @abstractmethod
    def ws_to_slices(self, ws, **kwargs):
        """
        Should produce slices for the windspeeds given in ws.

        Parameters
        ---------
        ws : 1 dimensional numpy.ndarray
            The wind speeds corresponding to the requested slices.

        **kwargs :
            Further keyword arguments that may be used by custom
            implementations. Are forwarded by the `get_slices` method.
            Supports the key 'full_info'.

        Returns
        --------
        slices : list of (3, *) numpy.ndarrays
            List of the requested slices. The three rows of a slice
            should correspond to the actual
            wind speeds, the wind angles and the boat speeds

        See also
        -----------
        `get_slices`
        """

    def points(self, wind=None):
        """
        Returns a read only version of all relevant points specified by wind

        Parameters
        ----------
        wind : (2, d) or (d, 2) numpy.ndarray or tuple of 2 (1, d) numpy.ndarray or `None`, optional
            A specification of the wind.

            - If given as a (2, d) or (d, 2) numpy.ndarray the columns (rows)
                are interpreted as different wind records
                (for d=2 we assume the shape (d, 2))
            - If given as a tuple, the first array defines the wind speed
             resolution, the second array defines the wind angle resolution.
             The wind records are all combinations thereof.

        Returns
        ---------
        points : (m, 3) numpy.ndarray
            Row-wise contains all records specified in `wind`
            consisting of wind speed, wind angle, boat speed.
            If `wind` is not specified, `self.default_points` is returned.
        """

        if wind is None:
            return self.default_points
        wind = self._get_wind(wind)
        bsps = [self(wa, ws) for wa, ws in wind]
        return np.column_stack([wind, bsps])


    def get_slice_info(self, ws, slices, **kwargs):
        """
        Should produce additional information about slices depending on the
        inheriting class which is returned when the `full_info` parameter of
        the `get_slices` method is set to `True`. If no further information
        is known, return None.

        Parameters
        ----------
        ws : 1 dimensional numpy.ndarray
            The wind speeds corresponding to the requested slices.

        slices : list of (3, *) `np.ndarray`
            Slices produced by `ws_to_slices`

        **kwargs :
            Further keyword arguments that may be used by custom
            implementations. Are forwarded by the `get_slices` method.
            Supports the key 'full_info'.

        Returns
        -------
        info : list of lists
            List of additional information for each record of each slice
            organized in the same manner as a slice.

        See also
        -----------
        `get_slices`
        """
        return None


    def plot_polar_slice(self, ws, ax=None, **plot_kw):
        """Creates a polar plot of a given slice of the
        polar diagram.

        Parameters
        ----------
        ws : int/float
            Description of slices of the polar diagram to be plotted.

            For a description of what the slice is made of,
            see the `plot_polar()`-method of the respective
            `PolarDiagram` subclass.

        ax : matplotlib.projections.polar.PolarAxes, optional
            Axes instance where the plot will be created.

            If nothing is passed, the function will create
            a suitable axes.

        plot_kw : Keyword arguments
            Keyword arguments that will be passed to the
            `matplotlib.axes.Axes.plot` function, to change
            certain appearances of the plot.
        """
        self.plot_polar(
            ws, ax, colors=None, show_legend=False, legend_kw=None, **plot_kw
        )

    def plot_flat_slice(self, ws, ax=None, **plot_kw):
        """Creates a cartesian plot of a given slice of the
        polar diagram.

        Parameters
        ----------
        ws : int/float
            Slice of the polar diagram.

            For a description of what the slice is made of,
            see the `plot_flat()`-method of the respective
            `PolarDiagram` subclass.

        ax : matplotlib.axes.Axes, optional
            Axes instance where the plot will be created.

            If nothing is passed, the function will create
            a suitable axes.

        plot_kw : Keyword arguments
            Keyword arguments that will be passed to the
            `matplotlib.axes.Axes.plot` function, to change
            certain appearances of the plot.
        """
        self.plot_flat(
            ws, ax, colors=None, show_legend=False, legend_kw=None, **plot_kw
        )

    @abstractmethod
    def plot_polar(
        self,
        ws=None,
        ax=None,
        colors=("green", "red"),
        show_legend=False,
        legend_kw=None,
        **plot_kw,
    ):
        """This method should create a polar plot of one or more slices,
        corresponding to `ws`, of the polar diagram object.

        Parameters
        ---------

        ws : int/float
            Description of slices of the polar diagram to be plotted.

            For details refer to the `plot_polar()`-method of the respective
            `PolarDiagram` subclass.

        ax : matplotlib.projections.polar.PolarAxes, optional
            Axes instance where the plot will be created.

        colors : sequence of color_likes or (ws, color_like) pairs, optional
            Specifies the colors to be used for the different slices.

            For details refer to the `plot_polar()`-method of the respective
            `PolarDiagram` subclass.

            Defaults to `("green", "red")`.

        show_legend : bool, optional
            Specifies whether or not a legend will be shown next to the plot.

            For details refer to the `plot_polar()`-method of the respective
            `PolarDiagram` subclass.

            Defaults to `False`.

        legend_kw : dict, optional
            Keyword arguments to change position and appearance of the legend.

            See `matplotlib.colorbar.Colorbar` for possible keywords
            when a colorbar is created and `matplotlib.legend.Legend` for
            possible keywords in cases where a Legend is created.

            For details refer to the `plot_polar()`-method of the respective
            `PolarDiagram` subclass.

            Will only be used if `show_legend` is `True`.

        plot_kw : Keyword arguments
            Keyword arguments to change various appearances of the plot.

            See `matplotlib.axes.Axes.plot` for possible keywords and their
            effects.
        """

    @abstractmethod
    def plot_flat(
        self,
        ws=None,
        ax=None,
        colors=("green", "red"),
        show_legend=False,
        legend_kw=None,
        **plot_kw,
    ):
        """This method should create a cartesian plot of one or more slices,
        corresponding to `ws`, of the `PolarDiagram` object.


        Parameters
        ----------
        ws : tuple of length 2, iterable, int or float, optional
            Slices of the polar diagram.

            For details refer to the `plot_flat()`-method of the respective
            `PolarDiagram` subclass.

            If nothing is passed, it will default to `(0, 20)`.

        ax : matplotlib.axes.Axes, optional
            Axes instance where the plot will be created.

        colors : sequence of color_likes or (ws, color_like) pairs, optional
            Specifies the colors to be used for the different slices.

            For details refer to the `plot_flat()`-method of the respective
            `PolarDiagram` subclass.

            Defaults to `("green", "red")`.

        show_legend : bool, optional
            Specifies whether a legend will be shown next to the plot.

            For details refer to the `plot_flat()`-method of the respective
            `PolarDiagram` subclass.

            Defaults to `False`.

        legend_kw : dict, optional
            Keyword arguments to change position and appearance of the legend.

            See `matplotlib.colorbar.Colorbar` and `matplotlib.legend.Legend` for
            possible keywords and their effects.

            Will only be used if `show_legend` is `True`.

        plot_kw : Keyword arguments
            Keyword arguments to change various appearances of the plot.

            See `matplotlib.axes.Axes.plot` for possible keywords and their
            effects.
        """

    @abstractmethod
    def plot_3d(self):
        """This method should create a 3d plot of the polar diagram object."""

    @abstractmethod
    def plot_color_gradient(
        self,
        ax=None,
        colors=("green", "red"),
        marker=None,
        ms=None,
        show_legend=False,
        **legend_kw,
    ):
        """This method should create 'wind speed vs. wind angle'
        color gradient plot of the polar diagram object with respect
        to the corresponding boat speeds.

        Parameters
        ----------

        ax : matplotlib.axes.Axes, optional
            Axes instance where the plot will be created.

        colors : tuple of two (2) color_likes, optional
            Color pair determining the color gradient with which the
            polar diagram will be plotted.

            For details refer to the `plot_color_gradient()`-method of
            the respective `PolarDiagram` subclass.

            Defaults to `("green", "red")`.

        marker : matplotlib.markers.Markerstyle or equivalent, optional
            Markerstyle for the created scatter plot.

            Defaults to `"o"`

        ms : float or array_like of fitting shape, optional
            Marker size in points**2.

        show_legend : bool, optional
            Specifies whether or not a legend will be shown next
            to the plot.

            Legend will be a `matplotlib.colorbar.Colorbar` instance.

            Defaults to `False`.

        legend_kw : Keyword arguments
            Keyword arguments to change position and appearance of the legend.

            See `matplotlib.legend.Legend` for possible keywords and
            their effects.

            Will only be used if `show_legend` is `True`.
        """

    def plot_convex_hull_slice(self, ws, ax=None, **plot_kw):
        """Computes the convex hull of a given slice of
        the polar diagram and creates a polar plot of it.

        Parameters
        ----------
        ws : int/float
            Slice of the polar diagram.

            For a description of what the slice is made of,
            see the `plot_convex_hull()`-method of the respective
            `PolarDiagram` subclass.

        ax : matplotlib.projections.polar.PolarAxes, optional
            Axes instance where the plot will be created.

            If nothing is passed, the function will create
            a suitable axes.

        plot_kw : Keyword arguments
            Keyword arguments that will be passed to the
            `matplotlib.axes.Axes.plot` function, to change
            certain appearances of the plot.
        """
        self.plot_convex_hull(
            ws, ax, colors=None, show_legend=False, legend_kw=None, **plot_kw
        )

    @abstractmethod
    def plot_convex_hull(
        self,
        ws=None,
        ax=None,
        colors=("green", "red"),
        show_legend=False,
        legend_kw=None,
        **plot_kw,
    ):
        """This method should compute the convex hull of one or multiple
        slices, corresponding to `ws`, of the polar diagram and then create
        a polar plot of them.

        Parameters
        ----------
        ws : tuple of length 2, iterable, int or float, optional
            Slices of the polar diagram.

            For details refer to the `plot_convex_hull()`-method of
            the respective `PolarDiagram` subclass.

            If nothing is passed, it will default to `(0, 20)`.

        ax : matplotlib.projections.polar.PolarAxes, optional
            Axes instance where the plot will be created.

        colors : sequence of color_likes or (ws, color_like) pairs, optional
            Specifies the colors to be used for the different slices.

            For details refer to the `plot_convex_hull()`-method of
            the respective `PolarDiagram` subclass.

            Defaults to `("green", "red")`.

        show_legend : bool, optional
            Specifies whether or not a legend will be shown next to the plot.

            The type of legend depends on the color options.

            For details refer to the `plot_convex_hull()`-method of
            the respective `PolarDiagram` subclass.

            Defaults to `False`.

        legend_kw : dict, optional
            Keyword arguments to change position and appearance of the legend.

            See `matplotlib.colorbar.Colorbar` and `matplotlib.legend.Legend`
            for possible keywords and their effects.

            Will only be used if show_legend is `True`.

        plot_kw : Keyword arguments
            Keyword arguments to change various appearances of the plot.

            See `matplotlib.axes.Axes.plot` for possible keywords and their
            effects.

        """
