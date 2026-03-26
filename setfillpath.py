import xml.etree.ElementTree as ET
from svgpathtools import svg2paths, wsvg

# --- Step 1: Load paths and attributes from an SVG ---
paths, attributes = svg2paths('input.svg')

# Example: modify the first path's geometry (optional)
# paths[0] = paths[0].translated(10 + 20j)  # move path by (10, 20)

# --- Step 2: Save modified paths to a new SVG ---
wsvg(paths, attributes=attributes, filename='temp.svg')

# --- Step 3: Edit the fill attribute using XML ---
tree = ET.parse('temp.svg')
root = tree.getroot()

# SVG namespace handling
ns = {'svg': 'http://www.w3.org/2000/svg'}

# Find all <path> elements and set fill
for path_elem in root.findall('.//svg:path', ns):
    path_elem.set('fill', '#ff0000')  # red fill

# Save final SVG
tree.write('output.svg', encoding='utf-8', xml_declaration=True)

print("SVG saved as output.svg with red fill applied to all paths.")