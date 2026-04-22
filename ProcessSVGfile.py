import sys
from svgpathtools import svg2paths, wsvg
from svgpathtools import parse_path, Path, Line, CubicBezier
from reportlab.lib.units import inch, mm
import lxml.etree as ET
import math
import warnings

def flip_svg_path_vertically(input_svg, output_svg, pathid):
    try:
        circuit = ET.parse(input_svg)
        root = circuit.getroot()
        svg_height = root.get("height")
        if svg_height is not None:
            measurement = svg_height[len(svg_height) - 2:]
            if measurement == "mm" or measurement == "cm" or measurement == "in" or measurement == "px" or measurement == "pt":
                svg_height = float(svg_height[:-2])
            else:
                svg_height = float(svg_height)
        else:
            svg_viewbox = root.get("viewBox")
            x = svg_viewbox.split()
            svg_height = float(x[3])
        original_d = circuit.xpath(f'//*[@id = "{pathid}"]')[0].attrib['d']
        path = parse_path(original_d)
        flipped_segments = []
        for segment in path:
            flipped_segments.append(segment.translated(complex(0, -svg_height)).scaled(1, -1).translated(complex(0, svg_height)))
        flipped_path = Path(*flipped_segments)
        nsmap = {'svg': 'http://www.w3.org/2000/svg'}
        for path_elem in root.findall('.//svg:path', nsmap):
            id_attr = path_elem.get("id")
            style_attr = path_elem.get("style")
            d_attr = path_elem.get("d")
            if id_attr == pathid:
                path_elem.set("id", pathid)
                path_elem.set("d", flipped_path.d())
                if style_attr:
                    styles = dict(item.split(":") for item in style_attr.split(";") if item)
                    styles["stroke-width"] = "3"
                    path_elem.set("style", ";".join(f"{k}:{v}" for k, v in styles.items()))
            else:
                path_elem.getparent().remove(path_elem)
        for text_elem in root.findall('.//svg:text', nsmap):
            text_elem.getparent().remove(text_elem)
        for rect_elem in root.findall('.//svg:rect', nsmap):
            rect_elem.getparent().remove(rect_elem)
        for elli_elem in root.findall('.//svg:ellipse', nsmap):
            elli_elem.getparent().remove(elli_elem)
        for circ_elem in root.findall('.//svg:circle', nsmap):
            circ_elem.getparent().remove(circ_elem)
        for use_elem in root.findall('.//svg:use', nsmap):
            use_elem.getparent().remove(use_elem)
        for g_elem in root.findall('.//svg:g', nsmap):
            id_attr = g_elem.get("id")
            transform_attr = g_elem.get("transform")
            if transform_attr is not None:
                g_elem.set("transform", "")
        min_x = math.inf
        min_y = math.inf
        for node in flipped_path:
            if isinstance(node, CubicBezier):
                start_x = node.start.real
                if start_x < min_x:
                    min_x = start_x
                start_y = node.start.imag
                if start_y < min_y:
                    min_y = start_y
                control1_x = node.control1.real
                if control1_x < min_x:
                    min_x = control1_x
                control1_y = node.control1.imag
                if control1_y < min_y:
                    min_y = control1_y
                control2_x = node.control2.real
                if control2_x < min_x:
                    min_x = control2_x 
                control2_y = node.control2.imag
                if control2_y < min_y:
                    min_y = control2_y
                end_x = node.end.real
                if end_x < min_x:
                    min_x = end_x 
                end_y = node.end.imag
                if end_y < min_y:
                    min_y = end_y
            if isinstance(node, Line):
                x0 = node.start.real
                if x0 < min_x:
                    min_x = x0
                y0 = node.start.imag
                if y0 < min_y:
                    min_y = y0
                x1 = node.end.real
                if x1 < min_x:
                    min_x = x1
                y1 = node.end.imag
                if y1 < min_y:
                    min_y = y1
        print("min_x", min_x, "min_y", min_y)
        min_x_str = str(-min_x)
        min_y_str = str(-min_y) 
        nsmap = {'svg': 'http://www.w3.org/2000/svg'}
        for path_elem in root.findall('.//svg:path', nsmap):
            id_attr = path_elem.get("id")
            if id_attr == pathid:
            	path_elem.set("transform", "translate(" + min_x_str + ", " + min_y_str + ")")
        circuit.write(output_svg, encoding='utf-8', xml_declaration=True)
    except Exception as e:
        raise ValueError(f"Invalid SVG path data: {e}")
    return

warnings.filterwarnings('ignore')

inputname = "Wiki/Original/BalatonParkorig.svg"
pathid = "path1"

flip_svg_path_vertically(inputname, inputname[:-8] + ".svg", pathid)

inputname = "Wiki/Original/PhillipIslandorig.svg"
pathid = "path2419"

flip_svg_path_vertically(inputname, inputname[:-8] + ".svg", pathid)

inputname = "Wiki/Original/RedBullRingorig.svg"
pathid = "path14"

inputname = "Wiki/Original/Jerezorig.svg"
pathid = "path3164"

flip_svg_path_vertically(inputname, inputname[:-8] + ".svg", pathid)

flip_svg_path_vertically(inputname, inputname[:-8] + ".svg", pathid)

key = input("Wait")
