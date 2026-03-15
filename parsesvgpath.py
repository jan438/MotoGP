from svgpathtools import parse_path, Line, CubicBezier, QuadraticBezier, Close
import cmath

def complex_to_tuple(c):
    """Convert complex number to (x, y) tuple."""
    return (c.real, c.imag)

# Example SVG path string
svg_path_str = "M 10 10 L 50 50 C 70 20, 100 80, 120 40 Q 140 60, 160 20 Z"

# Parse the path
path = parse_path(svg_path_str)

print("Parsed segments:")
for seg in path:
    if isinstance(seg, Line):
        print("Line:", complex_to_tuple(seg.start), "->", complex_to_tuple(seg.end))
    elif isinstance(seg, CubicBezier):
        print("CubicBezier:", 
              "start", complex_to_tuple(seg.start),
              "control1", complex_to_tuple(seg.control1),
              "control2", complex_to_tuple(seg.control2),
              "end", complex_to_tuple(seg.end))
    elif isinstance(seg, QuadraticBezier):
        print("QuadraticBezier:",
              "start", complex_to_tuple(seg.start),
              "control", complex_to_tuple(seg.control),
              "end", complex_to_tuple(seg.end))
    elif isinstance(seg, Close):
        print("Close path to:", complex_to_tuple(seg.end))
    else:
        print("Unknown segment type:", seg)

