import sys
from svgpathtools import svg2paths, wsvg
from svgpathtools import parse_path, Path, Line, CubicBezier
from reportlab.lib.units import inch, mm
import lxml.etree as ET
import warnings

def flip_svg_path_vertically(input_svg, output_svg, pathid):
    try:
        circuit = ET.parse(input_svg)
        root = circuit.getroot()
        svg_height = root.get("height")
        measurement = svg_height[len(svg_height) - 2:]
        if measurement == "mm" or measurement == "cm" or measurement == "in" or measurement == "px" or measurement == "pt":
            svg_height = float(svg_height[:-2])
        else:
            svg_height = float(svg_height)
        original_d = circuit.xpath(f'//*[@id = "{pathid}"]')[0].attrib['d']
        original_s = circuit.xpath(f'//*[@id = "{pathid}"]')[0].attrib['style']
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
        for use_elem in root.findall('.//svg:use', nsmap):
            use_elem.getparent().remove(use_elem)
        for g_elem in root.findall('.//svg:g', nsmap):
            id_attr = g_elem.get("id")
            transform_attr = g_elem.get("transform")
            if transform_attr is not None:
                print(id_attr, transform_attr)
        circuit.write(output_svg, encoding='utf-8', xml_declaration=True)
    except Exception as e:
        raise ValueError(f"Invalid SVG path data: {e}")
    return

warnings.filterwarnings('ignore')

inputname = "Wiki/BalatonParkorig.svg"
pathid = "path1"

flip_svg_path_vertically(inputname, inputname[:-8] + ".svg", pathid)

inputname = "Wiki/PhillipIslandorig.svg"
pathid = "path2419"

flip_svg_path_vertically(inputname, inputname[:-8] + ".svg", pathid)

key = input("Wait")
