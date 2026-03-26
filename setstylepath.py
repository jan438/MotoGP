import xml.etree.ElementTree as ET

# Load the SVG file
tree = ET.parse("input.svg")
root = tree.getroot()

# SVG namespace handling
ns = {"svg": "http://www.w3.org/2000/svg"}

# Loop through all path elements
for path in root.findall(".//svg:path", ns):
    # Option 1: Set stroke-width as a separate attribute
    path.set("stroke-width", "3")

    # Option 2: Modify inside the style attribute if present
    style = path.get("style")
    if style:
        styles = dict(item.split(":") for item in style.split(";") if item)
        styles["stroke-width"] = "3"
        path.set("style", ";".join(f"{k}:{v}" for k, v in styles.items()))

# Save the modified SVG
tree.write("output.svg")
