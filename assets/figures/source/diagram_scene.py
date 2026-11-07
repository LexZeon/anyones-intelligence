"""Small, editable diagram scenes with SVG, PNG, and diagrams.net exports.

All geometry is in logical pixels. ``text(x, y, ...)`` places the top of its
first line at ``y``; explicit newlines advance by 1.35 * font size. ``width``
checks a label's width, but never wraps or truncates it. The public ``items``
list contains the geometry, text lines, measured widths, and overflow flags.

Matplotlib is the only external dependency. A caller may put it on sys.path
or set DIAGRAM_MPL_PATH to an existing dependency directory. DIAGRAM_CJK_FONT
and DIAGRAM_CJK_BOLD_FONT can override the Windows Microsoft YaHei font files.
No downloads or dependency installation are performed.
"""

from __future__ import annotations

import math
import os
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


_MPL = None
_DPI = 100
_DASH = (8.0, 6.0)


def _matplotlib():
    global _MPL
    if _MPL is None:
        dependency_path = os.environ.get("DIAGRAM_MPL_PATH")
        if dependency_path and dependency_path not in sys.path:
            sys.path.insert(0, dependency_path)
        try:
            import matplotlib
            from matplotlib import font_manager
            from matplotlib.backends.backend_agg import FigureCanvasAgg
            from matplotlib.figure import Figure
            from matplotlib.lines import Line2D
            from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle
            from matplotlib.textpath import TextToPath
        except ImportError as exc:
            raise ImportError(
                "diagram_scene requires an existing matplotlib installation; "
                "add its directory to sys.path or set DIAGRAM_MPL_PATH."
            ) from exc
        _MPL = {
            "module": matplotlib,
            "font_manager": font_manager,
            "canvas": FigureCanvasAgg,
            "figure": Figure,
            "line": Line2D,
            "circle": Circle,
            "rounded_rect": FancyBboxPatch,
            "polygon": Polygon,
            "rect": Rectangle,
            "text_path": TextToPath(),
        }
    return _MPL


def _number(value):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError("Scene coordinates and sizes must be finite.")
    return value


def _positive(value, name, allow_zero=False):
    value = _number(value)
    if value < 0 or (value == 0 and not allow_zero):
        raise ValueError(f"{name} must be {'nonnegative' if allow_zero else 'positive'}.")
    return value


def _fmt(value):
    return f"{float(value):.6f}".rstrip("0").rstrip(".") or "0"


def _none(color):
    return color is None or str(color).lower() in ("none", "transparent")


def _color(color):
    return "none" if _none(color) else str(color)


def _has_cjk(text):
    return any(
        "\u2e80" <= char <= "\ua4cf"
        or "\uf900" <= char <= "\ufaff"
        or "\uff00" <= char <= "\uffef"
        or "\U00020000" <= char <= "\U0002ffff"
        for char in text
    )


def _is_bold(weight):
    try:
        return float(weight) >= 600
    except (TypeError, ValueError):
        return str(weight).lower() in ("bold", "semibold", "demibold", "heavy", "black")


def _font(text, size, weight):
    fm = _matplotlib()["font_manager"]
    normalized_weight = int(weight) if str(weight).isdigit() else weight
    if _has_cjk(text):
        path = Path(os.environ.get("DIAGRAM_CJK_FONT", "C:/Windows/Fonts/msyh.ttc"))
        if _is_bold(weight):
            bold_path = Path(os.environ.get("DIAGRAM_CJK_BOLD_FONT", str(path.with_name("msyhbd.ttc"))))
            if bold_path.is_file():
                path = bold_path
        if not path.is_file():
            raise FileNotFoundError(
                "A CJK label requires Microsoft YaHei or a compatible font. "
                "Set DIAGRAM_CJK_FONT to its local font file."
            )
        prop = fm.FontProperties(fname=str(path), size=size, weight=normalized_weight)
        family = prop.get_name()
        return prop, family, str(path)
    prop = fm.FontProperties(family="DejaVu Sans", size=size, weight=normalized_weight)
    return prop, "DejaVu Sans", fm.findfont(prop)


def _arrow_geometry(points, stroke_width):
    """Return a shortened stroke and a filled triangular arrowhead."""
    tip = points[-1]
    previous_index = len(points) - 2
    while previous_index >= 0 and points[previous_index] == tip:
        previous_index -= 1
    if previous_index < 0:
        return points, None
    previous = points[previous_index]
    dx, dy = tip[0] - previous[0], tip[1] - previous[1]
    distance = math.hypot(dx, dy)
    ux, uy = dx / distance, dy / distance
    length = min(max(10.0, 3.2 * stroke_width), distance * 0.8)
    half_width = length * 0.42
    base = (tip[0] - length * ux, tip[1] - length * uy)
    head = [
        tip,
        (base[0] - half_width * uy, base[1] + half_width * ux),
        (base[0] + half_width * uy, base[1] - half_width * ux),
    ]
    stroke = list(points[:previous_index + 1]) + [
        (tip[0] - length * 0.75 * ux, tip[1] - length * 0.75 * uy)
    ]
    return stroke, {
        "points": head, "length": length, "half_width": half_width,
        "angle": math.degrees(math.atan2(dy, dx)),
        "center": (tip[0] - length * 0.5 * ux, tip[1] - length * 0.5 * uy),
    }


class Scene:
    """A white drawing surface whose native primitives remain editable."""

    def __init__(self, width, height, title=""):
        self.width = _positive(width, "width")
        self.height = _positive(height, "height")
        self.title = str(title)
        self.items = []

    def rect(self, x, y, w, h, fill="#fff", stroke="none", sw=1, r=0):
        w, h = _positive(w, "w"), _positive(h, "h")
        self.items.append({
            "type": "rect", "x": _number(x), "y": _number(y), "w": w, "h": h,
            "fill": _color(fill), "stroke": _color(stroke),
            "sw": _positive(sw, "sw", True), "r": min(_positive(r, "r", True), w / 2, h / 2),
        })
        return self

    def text(self, x, y, text, size=18, color="#17212B", anchor="start", weight="normal", width=None):
        if anchor not in ("start", "middle", "end"):
            raise ValueError("anchor must be 'start', 'middle', or 'end'.")
        size = _positive(size, "size")
        text = str(text).replace("\r\n", "\n").replace("\r", "\n")
        lines = text.split("\n")
        prop, family, path = _font(text, size, weight)
        line_widths = [
            float(_matplotlib()["text_path"].get_text_width_height_descent(line, prop, False)[0])
            if line else 0.0 for line in lines
        ]
        width = None if width is None else _positive(width, "width")
        measured_width = max(line_widths, default=0.0)
        self.items.append({
            "type": "text", "x": _number(x), "y": _number(y), "text": text,
            "lines": lines, "size": size, "color": _color(color), "anchor": anchor,
            "weight": weight, "width": width, "font_family": family, "font_path": path,
            "line_height": size * 1.35, "line_widths": line_widths,
            "measured_width": measured_width, "height": size * 1.35 * len(lines),
            "overflow": width is not None and measured_width > width + 0.5,
        })
        return self

    def poly(self, points, color="#0072B2", sw=3, dash=False, arrow=False):
        points = [(_number(point[0]), _number(point[1])) for point in points]
        if len(points) < 2:
            raise ValueError("A polyline requires at least two points.")
        self.items.append({
            "type": "poly", "points": points, "color": _color(color),
            "sw": _positive(sw, "sw"), "dash": bool(dash), "arrow": bool(arrow),
        })
        return self

    def dot(self, x, y, r=5, fill="#fff", stroke="#0072B2", sw=2):
        self.items.append({
            "type": "dot", "x": _number(x), "y": _number(y),
            "r": _positive(r, "r"), "fill": _color(fill), "stroke": _color(stroke),
            "sw": _positive(sw, "sw", True),
        })
        return self

    def save(self, basepath):
        """Export three files and return their paths; no implicit text wrapping."""
        base = Path(basepath)
        if base.suffix.lower() in (".svg", ".png", ".drawio"):
            base = base.with_suffix("")
        base.parent.mkdir(parents=True, exist_ok=True)
        paths = {extension: Path(str(base) + "." + extension) for extension in ("svg", "png", "drawio")}
        self._save_svg(paths["svg"])
        self._save_png(paths["png"])
        self._save_drawio(paths["drawio"])
        return {extension: str(path) for extension, path in paths.items()}

    def _save_svg(self, path):
        root = ET.Element("svg", {
            "xmlns": "http://www.w3.org/2000/svg", "width": _fmt(self.width),
            "height": _fmt(self.height), "viewBox": f"0 0 {_fmt(self.width)} {_fmt(self.height)}",
        })
        if self.title:
            ET.SubElement(root, "title").text = self.title
        ET.SubElement(root, "rect", {"width": "100%", "height": "100%", "fill": "#ffffff"})
        for item in self.items:
            kind = item["type"]
            if kind == "rect":
                ET.SubElement(root, "rect", {
                    "x": _fmt(item["x"]), "y": _fmt(item["y"]),
                    "width": _fmt(item["w"]), "height": _fmt(item["h"]),
                    "rx": _fmt(item["r"]), "fill": item["fill"], "stroke": item["stroke"],
                    "stroke-width": _fmt(item["sw"]),
                })
            elif kind == "dot":
                ET.SubElement(root, "circle", {
                    "cx": _fmt(item["x"]), "cy": _fmt(item["y"]), "r": _fmt(item["r"]),
                    "fill": item["fill"], "stroke": item["stroke"], "stroke-width": _fmt(item["sw"]),
                })
            elif kind == "text":
                for index, line in enumerate(item["lines"]):
                    element = ET.SubElement(root, "text", {
                        "x": _fmt(item["x"]), "y": _fmt(item["y"] + index * item["line_height"]),
                        "font-family": item["font_family"], "font-size": _fmt(item["size"]),
                        "font-weight": str(item["weight"]), "fill": item["color"],
                        "text-anchor": item["anchor"], "dominant-baseline": "text-before-edge",
                        "xml:space": "preserve",
                    })
                    element.text = line
            elif kind == "poly":
                points, head = _arrow_geometry(item["points"], item["sw"]) if item["arrow"] else (item["points"], None)
                attrs = {
                    "points": " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in points),
                    "fill": "none", "stroke": item["color"], "stroke-width": _fmt(item["sw"]),
                    "stroke-linecap": "round", "stroke-linejoin": "round",
                }
                if item["dash"]:
                    attrs["stroke-dasharray"] = "8 6"
                ET.SubElement(root, "polyline", attrs)
                if head:
                    ET.SubElement(root, "polygon", {
                        "points": " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in head["points"]),
                        "fill": item["color"], "stroke": "none",
                    })
        self._write_xml(path, root)

    def _save_png(self, path):
        mpl = _matplotlib()
        with mpl["module"].rc_context({"lines.scale_dashes": False, "text.usetex": False}):
            figure = mpl["figure"](figsize=(self.width / _DPI, self.height / _DPI), dpi=_DPI, facecolor="white")
            mpl["canvas"](figure)
            axes = figure.add_axes([0, 0, 1, 1])
            axes.set_xlim(0, self.width)
            axes.set_ylim(self.height, 0)
            axes.set_aspect("equal")
            axes.set_axis_off()
            unit = 72.0 / _DPI
            try:
                for index, item in enumerate(self.items):
                    kind = item["type"]
                    zorder = index + 1
                    if kind == "rect":
                        kwargs = {"facecolor": item["fill"], "edgecolor": item["stroke"], "linewidth": item["sw"] * unit, "zorder": zorder}
                        if item["r"]:
                            patch = mpl["rounded_rect"]((item["x"], item["y"]), item["w"], item["h"], boxstyle=f"round,pad=0,rounding_size={item['r']}", **kwargs)
                        else:
                            patch = mpl["rect"]((item["x"], item["y"]), item["w"], item["h"], **kwargs)
                        axes.add_patch(patch)
                    elif kind == "dot":
                        axes.add_patch(mpl["circle"]((item["x"], item["y"]), item["r"], facecolor=item["fill"], edgecolor=item["stroke"], linewidth=item["sw"] * unit, zorder=zorder))
                    elif kind == "text":
                        prop = mpl["font_manager"].FontProperties(fname=item["font_path"], size=item["size"] * unit, weight=item["weight"])
                        for line_index, line in enumerate(item["lines"]):
                            axes.text(item["x"], item["y"] + line_index * item["line_height"], line, color=item["color"], fontproperties=prop, ha={"start": "left", "middle": "center", "end": "right"}[item["anchor"]], va="top", zorder=zorder, clip_on=False, parse_math=False)
                    elif kind == "poly":
                        points, head = _arrow_geometry(item["points"], item["sw"]) if item["arrow"] else (item["points"], None)
                        line = mpl["line"]([p[0] for p in points], [p[1] for p in points], color=item["color"], linewidth=item["sw"] * unit, solid_capstyle="round", solid_joinstyle="round", dash_capstyle="round", dash_joinstyle="round", zorder=zorder)
                        if item["dash"]:
                            line.set_dashes([value * unit for value in _DASH])
                        axes.add_line(line)
                        if head:
                            axes.add_patch(mpl["polygon"](head["points"], closed=True, facecolor=item["color"], edgecolor="none", zorder=zorder + 0.1))
                figure.savefig(path, format="png", dpi=_DPI * 2, facecolor="white", edgecolor="none", transparent=False)
            finally:
                figure.clear()

    def _save_drawio(self, path):
        root = ET.Element("mxfile", {"host": "app.diagrams.net", "type": "device", "compressed": "false"})
        diagram = ET.SubElement(root, "diagram", {"id": "scene", "name": self.title or "Diagram"})
        model = ET.SubElement(diagram, "mxGraphModel", {
            "dx": _fmt(self.width), "dy": _fmt(self.height), "grid": "0", "gridSize": "10",
            "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1", "fold": "1",
            "page": "1", "pageScale": "1", "pageWidth": _fmt(self.width),
            "pageHeight": _fmt(self.height), "background": "#ffffff", "math": "0", "shadow": "0",
        })
        graph = ET.SubElement(model, "root")
        ET.SubElement(graph, "mxCell", {"id": "0"})
        ET.SubElement(graph, "mxCell", {"id": "1", "parent": "0"})
        for index, item in enumerate(self.items):
            identity = f"item-{index}"
            kind = item["type"]
            if kind in ("rect", "dot"):
                if kind == "rect":
                    x, y, w, h = item["x"], item["y"], item["w"], item["h"]
                    shape = f"shape=rectangle;rounded={int(item['r'] > 0)};absoluteArcSize=1;arcSize={_fmt(2 * item['r'])};"
                else:
                    x, y, w, h = item["x"] - item["r"], item["y"] - item["r"], 2 * item["r"], 2 * item["r"]
                    shape = "shape=ellipse;perimeter=ellipsePerimeter;"
                style = shape + f"html=0;fillColor={item['fill']};strokeColor={item['stroke']};strokeWidth={_fmt(item['sw'])};"
                self._vertex(graph, identity, "", style, x, y, w, h)
            elif kind == "text":
                for line_index, line in enumerate(item["lines"]):
                    w = max(item["line_widths"][line_index] + 4, 1)
                    x = item["x"] - {"start": 0, "middle": w / 2, "end": w}[item["anchor"]]
                    style = (
                        "text;html=0;whiteSpace=nowrap;overflow=visible;verticalAlign=top;spacing=0;"
                        "spacingTop=0;spacingBottom=0;spacingLeft=0;spacingRight=0;"
                        "fillColor=none;strokeColor=none;"
                        f"align={ {'start': 'left', 'middle': 'center', 'end': 'right'}[item['anchor']] };"
                        f"fontFamily={item['font_family']};fontSize={_fmt(item['size'])};"
                        f"fontStyle={int(_is_bold(item['weight']))};fontColor={item['color']};"
                    )
                    self._vertex(graph, f"{identity}-line-{line_index}", line, style, x, item["y"] + line_index * item["line_height"], w, item["line_height"])
            elif kind == "poly":
                points, head = _arrow_geometry(item["points"], item["sw"]) if item["arrow"] else (item["points"], None)
                style = (
                    "edgeStyle=none;noEdgeStyle=1;orthogonalLoop=0;rounded=0;curved=0;html=0;"
                    "startArrow=none;endArrow=none;"
                    f"strokeColor={item['color']};strokeWidth={_fmt(item['sw'])};"
                    f"dashed={int(item['dash'])};fixDash=1;dashPattern=8 6;"
                )
                cell = ET.SubElement(graph, "mxCell", {"id": identity, "value": "", "style": style, "edge": "1", "parent": "1"})
                geometry = ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
                ET.SubElement(geometry, "mxPoint", {"x": _fmt(points[0][0]), "y": _fmt(points[0][1]), "as": "sourcePoint"})
                ET.SubElement(geometry, "mxPoint", {"x": _fmt(points[-1][0]), "y": _fmt(points[-1][1]), "as": "targetPoint"})
                middle = ET.SubElement(geometry, "Array", {"as": "points"})
                for x, y in points[1:-1]:
                    ET.SubElement(middle, "mxPoint", {"x": _fmt(x), "y": _fmt(y)})
                if head:
                    cx, cy = head["center"]
                    style = f"shape=triangle;direction=east;rotation={_fmt(head['angle'])};html=0;fillColor={item['color']};strokeColor=none;"
                    self._vertex(graph, identity + "-arrow", "", style, cx - head["length"] / 2, cy - head["half_width"], head["length"], 2 * head["half_width"])
        self._write_xml(path, root)

    @staticmethod
    def _vertex(parent, identity, value, style, x, y, w, h):
        cell = ET.SubElement(parent, "mxCell", {"id": identity, "value": value, "style": style, "vertex": "1", "parent": "1"})
        ET.SubElement(cell, "mxGeometry", {"x": _fmt(x), "y": _fmt(y), "width": _fmt(w), "height": _fmt(h), "as": "geometry"})
        return cell

    @staticmethod
    def _write_xml(path, root):
        ET.indent(root, space="  ")
        document = ET.tostring(root, encoding="unicode", short_empty_elements=True)
        Path(path).write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + document + "\n", encoding="utf-8", newline="\n")


__all__ = ["Scene"]
