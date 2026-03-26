from lxml import etree

def set_svg_path_id(svg_input_path, svg_output_path, new_id, path_index=0):
    """
    Set the 'id' attribute of a <path> element in an SVG file.

    :param svg_input_path: Path to the input SVG file
    :param svg_output_path: Path to save the modified SVG
    :param new_id: The new ID to assign to the path
    :param path_index: Index of the <path> element to modify (0-based)
    """
    try:
        # Parse the SVG file
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(svg_input_path, parser)
        root = tree.getroot()

        # SVG namespace handling
        nsmap = {'svg': 'http://www.w3.org/2000/svg'}

        # Find all <path> elements
        paths = root.findall('.//svg:path', namespaces=nsmap)
        if not paths:
            raise ValueError("No <path> elements found in the SVG.")

        if path_index < 0 or path_index >= len(paths):
            raise IndexError(f"path_index {path_index} is out of range. Found {len(paths)} paths.")

        # Set the new ID
        paths[path_index].set('id', new_id)

        # Save the modified SVG
        tree.write(svg_output_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        print(f"Updated path[{path_index}] with id='{new_id}' and saved to {svg_output_path}")

    except (OSError, etree.XMLSyntaxError, ValueError, IndexError) as e:
        print(f"Error: {e}")

# Example usage:
if __name__ == "__main__":
    set_svg_path_id(
        svg_input_path="input.svg",
        svg_output_path="output.svg",
        new_id="myPath123",
        path_index=0
    )