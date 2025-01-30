import markdown
import os


def convert_md_to_html(md_file_path, output_html_path):
    # Check if the markdown file exists
    if not os.path.isfile(md_file_path):
        raise FileNotFoundError(f"The file {md_file_path} does not exist.")

    # Read the markdown file
    with open(md_file_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    # Convert markdown to HTML
    html_content = markdown.markdown(
        md_content, extensions=["fenced_code", "codehilite"]
    )

    # Write the HTML content to the output file
    with open(output_html_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    print(f"Conversion successful! HTML file saved as {output_html_path}")


# Example usage
if __name__ == "__main__":
    convert_md_to_html("README.md", "docs/index2.html")
