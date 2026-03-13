# Install svgpathtools if not already installed:
# pip install svgpathtools

from svgpathtools import parse_path, Path, Line, CubicBezier
from cmath import rect

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

# Example SVG path string
svg_path_str = "M 0,0 L 100,0 L 100,100 C 100,150 150,150 150,100"

# Parse the path
path = parse_path(svg_path_str)

# Convert all Line segments to CubicBezier
converted_segments = []
for segment in path:
    if isinstance(segment, Line):
        converted_segments.append(line_to_cubic(segment))
    else:
        converted_segments.append(segment)

# Create new path
new_path = Path(*converted_segments)

# Output new SVG path string
print("Original path:", svg_path_str)
print("Converted path:", new_path.d())
key = input("Wait")
