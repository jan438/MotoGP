
from svgpathtools import parse_path, Path, Line, CubicBezier
from cmath import rect
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import red, green
from xml.dom import minidom
from svglib.svglib import svg2rlg, load_svg_file, SvgRenderer

def scaleSVG(svgfile, scaling_factor):
    svg_root = load_svg_file(svgfile)
    svgRenderer = SvgRenderer(svgfile)
    drawing = svgRenderer.render(svg_root)
    scaling_x = scaling_factor
    scaling_y = scaling_factor
    drawing.width = drawing.minWidth() * scaling_x
    drawing.height = drawing.height * scaling_y
    drawing.scale(scaling_x, scaling_y)
    return drawing
    
def line_to_cubic(line: Line) -> CubicBezier:
    """
    Convert a straight line segment into a cubic Bézier curve
    where control points are placed along the line.
    """
    start = line.start
    end = line.end
    # Control points at 1/3 and 2/3 along the line
    ctrl1 = start + (end - start) / 3
    ctrl2 = start + 2 * (end - start) / 3
    return CubicBezier(start, ctrl1, ctrl2, end)

svg_path_str = "M 0,0 L 100,0 L 100,100 C 100,150 150,150 150,100"
path = parse_path(svg_path_str)
converted_segments = []
start_x = 0
start_y = 0
first_command = True
for segment in path:
    if isinstance(segment, Line):
        converted_segments.append(line_to_cubic(segment))
    else:
        converted_segments.append(segment)
c = canvas.Canvas("PDF/Path.pdf")
doc = minidom.parse("Aragónv.svg")
path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
doc.unlink()
p = c.beginPath()
for path_string in path_strings:
    path = parse_path(path_string)
    for e in path:
        if isinstance(e, Line):
            x0 = e.start.real
            y0 = e.start.imag
            x1 = e.end.real
            y1 = e.end.imag
            print("(%.2f, %.2f) - (%.2f, %.2f)" % (x0, y0, x1, y1))
        elif isinstance(e, CubicBezier):
            cubic = e
            start_x = cubic.start.real / 10
            start_y = cubic.start.imag / 10
            control1_x = cubic.control1.real / 10
            control1_y = cubic.control1.imag / 10
            control2_x = cubic.control2.real / 10
            control2_y = cubic.control2.imag / 10
            end_x = cubic.end.real / 10
            end_y = cubic.end.imag / 10
            if first_command:
                first_command = False
                p.moveTo(start_x, start_y)
                p.curveTo(control1_x, control1_y, control2_x, control2_y, end_x, end_y)
            else:
                p.curveTo(control1_x, control1_y, control2_x, control2_y, end_x, end_y)
p.close()
c.drawPath(p, stroke = 1, fill = 0)
c.showPage()
c.save()

key = input("Wait")

