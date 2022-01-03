"""
Contains various helper functions for the plot_*-methods() of the
PolarDiagram subclasses
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import (
    LinearSegmentedColormap,
    Normalize,
    is_color_like,
    to_rgb,
)
from matplotlib.lines import Line2D
from scipy.spatial import ConvexHull


def plot_polar(ws, wa, bsp, ax, colors, show_legend, legend_kw, **plot_kw):
    """"""
    if ax is None:
        ax = _get_new_axis("polar")
    _set_polar_axis(ax)

    _plot(ws, wa, bsp, ax, colors, show_legend, legend_kw, **plot_kw)


def _get_new_axis(kind):
    return plt.axes(projection=kind)


def _set_polar_axis(ax):
    ax.set_theta_zero_location("N")
    ax.set_theta_direction("clockwise")


def _plot(ws, wa, bsp, ax, colors, show_legend, legend_kw, **plot_kw):
    _configure_colors(ax, ws, colors)

    if show_legend:
        _show_legend(ax, ws, colors, label="True Wind Speed", legend_kw)

    for x, y in zip(wa, bsp):
        ax.plot(x, y, **plot_kw)


def _configure_colors(ax, ws, colors):
    if _only_one_color(colors):
        ax.set_prop_cycle("color", [colors])
    elif _more_colors_than_plots(ws, colors):
        ax.set_prop_cycle("color", colors)
    elif _no_color_gradient(colors):
        _set_color_cycle(ax, ws, colors)
    else:
        _set_color_gradient(ax, ws, colors)


def _only_one_color(colors):
    return is_color_like(colors)


def _more_colors_than_plots(ws, colors):
    return len(ws) <= len(colors)


def _no_color_gradient(ws, colors):
    return len(colors) != 2


def _set_color_cycle(ax, ws, colors):
    color_cycle = ["blue"] * len(ws)
    _configure_color_cycle(color_cycle, colors, ws)
    ax.set_prop_cycle("color", color_cycle)


def _configure_color_cycle(color_cycle, colors, ws):
    if isinstance(colors[0], tuple):
        if _only_one_color(colors[0]):
            for i, c in enumerate(colors):
                color_cycle[i] = c
                return

        for w, c in colors:
            i = list(ws).index(w)
            color_cycle[i] = c
            return

    for i, c in enumerate(colors):
        color_cycle[i] = c


def _show_legend(ax, ws, colors, label, legend_kw):
    if legend_kw is None:
        legend_kw = {}

    _configure_legend(ax, ws, colors, label, **legend_kw)


def _configure_legend(ax, ws, colors, label, **legend_kw):

    if _plot_with_color_gradient(ws, colors):
        _set_colormap(ws, colors, ax, label, **legend_kw)
        return

    if isinstance(colors[0], tuple) and not is_color_like(colors[0]):
        _set_legend_without_wind_speeds(ax, colors, legend_kw)
        return

    _set_legend_with_wind_speeds(ax, colors, ws, legend_kw)


def _plot_with_color_gradient(ws, colors):
    return len(ws) > len(colors) == 2


def _set_colormap(ws, colors, ax, label, **legend_kw):
    color_map = _create_color_map(colors)
    plt.colorbar(
        ScalarMappable(norm=Normalize(vmin=min(ws), vmax=max(ws)), cmap=color_map),
        ax=ax,
        **legend_kw,
    ).set_label(label)


def _set_legend_without_wind_speeds(ax, colors, legend_kw):
    ax.legend(handles=[Line2D([0],[0], color=color, lw=1, label=f"TWS {ws}") for (ws, color) in colors], **legend_kw)


def _set_legend_with_wind_speeds(ax, colors, ws, legend_kw):
    slices = zip(ws, colors)

    ax.legend(handles=[Line2D([0], [0], color=color, lw=1, label=f"TWS {ws}") for (ws, colors) in slices], **legend_kw)


def plot_flat(ws, wa, bsp, ax, colors, show_legend, legend_kw, **plot_kw):
    """"""
    if ax is None:
        ax = _get_new_axis("rectlinear")

    _plot(ws, wa, bsp, ax, colors, show_legend, legend_kw, **plot_kw)


def plot_color_gradient(
    ws, wa, bsp, ax, colors, marker, ms, show_legend, **legend_kw
):
    """"""
    if ax is None:
        ax = _get_new_axis("rectlinear")

    if show_legend:
        _show_legend(ax, bsp, colors, label="Boat Speed", legend_kw)

    color_gradient = _determine_color_gradient(colors, bsp)

    ax.scatter(ws, wa, s=ms, marker=marker, c=color_gradient)


def _determine_color_gradient(colors, bsp):
    min_color = np.array(to_rgb(colors[0]))
    max_color = np.array(to_rgb(colors[1]))
    min_bsp = np.min(bsp)
    max_bsp = np.max(bsp)

    coeffs = [(b - min_bsp) / (max_bsp - min_bsp) for b in bsp]

    return [(1 - c) * min_color + c * max_color for c in coeffs]


def plot3d(ws, wa, bsp, ax, colors, **plot_kw):
    """"""
    if ax is None:
        ax = _get_new_axis("3d")

    _set_3d_axis_labels(ax)
    _remove_3d_axis_labels_for_polar_coordinates(ax) 

    color_map = _create_color_map(colors)

    ax.scatter(ws, wa, bsp, c=ws, cmap=color_map, **plot_kw)


def plot_surface(ws, wa, bsp, ax, colors):
    """"""
    if ax is None:
        ax = _get_new_axis("3d")

    _set_3d_axis_labels(ax)
    _remove_3d_tick_labels_for_polar_coordinates(ax) 

    color_map = _create_color_map(colors)    
    face_colors = _determine_face_colors(color_map, ws) 

    ax.plot_surface(ws, wa, bsp, facecolors=face_colors)


def _create_color_map(colors):
    return LinearSegmentedColormap.from_list("cmap", list(colors))


def _determine_face_colors(color_map, ws):
    return color_map((ws - ws.min()) / float((ws - ws.min()).max()))


def _set_3d_axis_labels(ax):
    ax.set_xlabel("TWS")
    ax.set_ylabel("Polar plane: TWA / BSP ")


def _remove_3d_tick_labels_for_polar_coordinates(ax):
    ax.yaxis.set_ticklabels([])
    ax.zaxis.set_ticklabel([])


def plot_convex_hull(
    ws, wa, bsp, ax, colors, show_legend, legend_kw, **plot_kw
):
    if ax is None:
        ax = _get_new_axis("polar")

    _set_polar_axis(ax)

    _prepare_plot(ax, ws, colors, show_legend, legend_kw, plot_kw)

    xs, ys = _get_convex_hull(wa, bsp)

    for x, y in zip(list(xs), list(ys)):
        ax.plot(x, y, **plot_kw)


def plot_convex_hull_multisails(
    ws, wa, bsp, members, ax, colors, show_legend, legend_kw, **plot_kw
):
    if ax is None:
        ax = _get_new_axis("polar")

    _set_polar_axis(ax)

    xs, ys, members = _get_convex_hull_multisails(ws, wa, bsp, members)

    if colors is None:
        colors = plot_kw.pop("color", None) or plot_kw.pop("c", None) or []
    colors = dict(colors)
    _set_colors_multisails(ax, members, colors)

    if legend_kw is None:
        legend_kw = {}
    if show_legend:
        _set_legend_multisails(ax, colors, **legend_kw)

    for x, y in zip(list(xs), list(ys)):
        ax.plot(x, y, **plot_kw)


def _prepare_plot(ax, ws, colors, show_legend, legend_kw, plot_kw):
    _set_color_cycle(ax, ws, colors)

    if legend_kw is None:
        legend_kw = {}
    if show_legend:
        _set_legend(ax, ws, colors, label="True Wind Speed", **legend_kw)


def _set_color_cycle(ax, ws, colors):

        if n_plots > n_colors != 2:
        colorlist = 
        _set_colorlist(colors, colorlist, ws)
        ax.set_prop_cycle("color", colorlist)

        return

    color_gradient = _determine_color_gradient(colors, ws)
    ax.set_prop_cycle("color", color_gradient)
    

def _set_colorlist(colors, colorlist, ws):
    


def _determine_convex_hull(wa, bsp):
    xs = []
    ys = []
    slices = zip(wa, bsp)

    for wa, bsp in slices:
        wa = np.asarray(wa)
        bsp = np.asarray(bsp)

        # convex hull is line between the two points
        # or is equal to one point
        if len(wa) < 3:
            xs.append(wa)
            ys.append(bsp)
            continue

        conv = _convex_hull_polar(w, b)
        vert = sorted(conv.vertices)
        x, y = zip(
            *([(w[i], b[i]) for i in vert] + [(w[vert[0]], b[vert[0]])])
        )
        xs.append(list(x))
        ys.append(list(y))

    return xs, ys


def _get_convex_hull_multisails(ws, wa, bsp, members):
    members = members[0]
    xs = []
    ys = []
    membs = []
    for s, w, b in zip(ws, wa, bsp):
        w = np.asarray(w)
        b = np.asarray(b)
        conv = _convex_hull_polar(w, b)
        vert = sorted(conv.vertices)

        x, y, memb = zip(
            *(
                [(w[i], b[i], members[i]) for i in vert]
                + [(w[vert[0]], b[vert[0]], members[vert[0]])]
            )
        )
        x = list(x)
        y = list(y)
        memb = list(memb)

        for i in range(len(vert)):
            xs.append(x[i : i + 2])
            ys.append(y[i : i + 2])
            membs.append(memb[i : i + 2] + [s])

    return xs, ys, membs


def _convex_hull_polar(wa, bsp):
    polar_pts = np.column_stack((bsp * np.cos(wa), bsp * np.sin(wa)))
    return ConvexHull(polar_pts)


def _set_colors_multisails(ax, members, colors):
    colorlist = []

    for member in members:
        # check if edge belongs to one or two sails
        # If it belongs to one sail, color it in that sails color
        # else color it in neutral color
        if len(set(member[:2])) == 1:
            color = colors.get(member[0], "blue")
        else:
            color = colors.get("neutral", "gray")

        if is_color_like(color):
            colorlist.append(color)
            continue

        color = dict(color)
        colorlist.append(color.get(member[2], "blue"))

    ax.set_prop_cycle("color", colorlist)


def _set_legend_multisails(ax, colors, **legend_kw):
    handles = []
    for key in colors:
        color = colors.get(key, "blue")

        if is_color_like(color):
            legend = Line2D([0], [0], color=color, lw=1, label=key)
            handles.append(legend)
            continue

        color = dict(color)
        legends = [
            Line2D(
                [0],
                [0],
                color=color.get(ws, "blue"),
                lw=1,
                label=f"{key} at TWS {ws}",
            )
            for ws in color
        ]
        handles.extend(legends)

    if "neutral" not in colors:
        legend = Line2D([0], [0], color="gray", lw=1, label="neutral")
        handles.append(legend)

    ax.legend(handles=handles, **legend_kw)
