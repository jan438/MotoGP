
from svgpathtools import parse_path, Path, Line, CubicBezier
from cmath import rect
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import red, green

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
    
def hand(c, debug=1, fill=0):
    (startx, starty) = (0,0)
    curves = [
    ( 0, 2), ( 0, 4), ( 0, 8), # back of hand
    ( 5, 8), ( 7,10), ( 7,14),
    (10,14), (10,13), ( 7.5, 8), # thumb
    (13, 8), (14, 8), (17, 8),
    (19, 8), (19, 6), (17, 6),
    (15, 6), (13, 6), (11, 6), # index, pointing
    (12, 6), (13, 6), (14, 6),
    (16, 6), (16, 4), (14, 4),
    (13, 4), (12, 4), (11, 4), # middle
    (11.5, 4), (12, 4), (13, 4),
    (15, 4), (15, 2), (13, 2),
    (12.5, 2), (11.5, 2), (11, 2), # ring
    (11.5, 2), (12, 2), (12.5, 2),
    (14, 2), (14, 0), (12.5, 0),
    (10, 0), (8, 0), (6, 0), # pinky, then close
    ]

    if debug: 
        c.setLineWidth(6)
    u = inch*0.2
    p = c.beginPath()
    p.moveTo(startx, starty)
    ccopy = list(curves)
    while ccopy:
        [(x1,y1), (x2,y2), (x3,y3)] = ccopy[:3]
        del ccopy[:3]
        p.curveTo(x1*u,y1*u,x2*u,y2*u,x3*u,y3*u)
    p.close()
    c.drawPath(p, fill=fill)
    if debug:
        (lastx, lasty) = (startx, starty)
        ccopy = list(curves)
        while ccopy:
            [(x1,y1), (x2,y2), (x3,y3)] = ccopy[:3]
            del ccopy[:3]
            c.setStrokeColor(red)
            c.line(lastx*u,lasty*u, x1*u,y1*u)
            c.setStrokeColor(green)
            c.line(x2*u,y2*u, x3*u,y3*u)
            (lastx,lasty) = (x3,y3)
    
def hello(c):
    c.drawString(100,100,"Hello World")
    return

svg_path_str = "M 0,0 L 100,0 L 100,100 C 100,150 150,150 150,100"
path = parse_path(svg_path_str)

# Convert all Line segments to CubicBezier
converted_segments = []
for segment in path:
    if isinstance(segment, Line):
        converted_segments.append(line_to_cubic(segment))
    else:
        converted_segments.append(segment)
new_path = Path(*converted_segments)
print("Original path:", svg_path_str)
print("Converted path:", new_path.d())

c = canvas.Canvas("PDF/hello.pdf")
#hello(c)
f = open("cloud.svg")
print(f.read())
f.close()
hand(c, 1, 0)
c.showPage()
c.save()

key = input("Wait")

