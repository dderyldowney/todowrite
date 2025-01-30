import argparse
import markdown2
import html2text
import os
import glob


def convert_markdown_to_html(
    input_file, output_file, title, css, extensions, template_file
):
    with open(input_file, "r") as file:
        markdown_content = file.read()

    extras = extensions.split(",") if extensions else []
    html_content = markdown2.markdown(markdown_content, extras=extras)

    if template_file:
        with open(template_file, "r") as file:
            template_content = file.read()
            full_html_content = template_content.replace(
                "{{content}}", html_content
            )
    else:
        css_link = (
            f'<link rel="stylesheet" type="text/css" href="{css}">'
            if css
            else ""
        )
        full_html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title if title else 'Markdown Converted HTML'}</title>
    {css_link}
</head>
<body>
{html_content}
</body>
</html>
"""

    with open(output_file, "w") as file:
        file.write(full_html_content)
    print(f"Converted {input_file} to {output_file}")


def interactive_mode():
    input_path = input("Enter the input file path: ")
    output_path = input("Enter the output file path: ")
    conversion_direction = input(
        "Convert to HTML (h) or Markdown (m)? [h/m]: "
    )
    title = (
        input(
            "Enter a title for the HTML document (leave blank for default): "
        )
        if conversion_direction == "h"
        else None
    )
    css = (
        input(
            "Enter the path to a CSS file for styling (leave blank for none): "
        )
        if conversion_direction == "h"
        else None
    )
    extensions = (
        input(
            "Enter any markdown2 extensions to use (comma-separated, leave blank for none): "
        )
        if conversion_direction == "h"
        else None
    )
    template_file = (
        input(
            "Enter the path to an HTML template file (leave blank for none): "
        )
        if conversion_direction == "h"
        else None
    )

    if conversion_direction == "h":
        convert_markdown_to_html(
            input_path, output_path, title, css, extensions, template_file
        )
    else:
        convert_html_to_markdown(input_path, output_path)


def convert_html_to_markdown(input_file, output_file):
    with open(input_file, "r") as file:
        html_content = file.read()

    markdown_content = html2text.html2text(html_content)
    with open(output_file, "w") as file:
        file.write(markdown_content)
    print(f"Converted {input_file} to {output_file}")


def batch_convert(files, output_dir, to_html, title=None, css=None):
    for file in files:
        filename, file_extension = os.path.splitext(os.path.basename(file))
        output_file = os.path.join(
            output_dir, filename + (".html" if to_html else ".md")
        )
        if to_html:
            convert_markdown_to_html(file, output_file, title, css)
        else:
            convert_html_to_markdown(file, output_file)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown to HTML and vice versa."
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Input file path or pattern for batch conversion (e.g., '*.md')",
    )
    parser.add_argument(
        "output",
        nargs="?",
        help="Output file path or output directory for batch conversion",
    )
    parser.add_argument(
        "--to_html", help="Convert from Markdown to HTML", action="store_true"
    )
    parser.add_argument(
        "--to_md", help="Convert from HTML to Markdown", action="store_true"
    )
    parser.add_argument(
        "--title", help="Custom title for the HTML document", default=None
    )
    parser.add_argument(
        "--css",
        help="Path to a CSS file for styling the HTML document",
        default=None,
    )
    parser.add_argument(
        "--extensions",
        help="Comma-separated list of markdown2 extensions",
        default=None,
    )
    parser.add_argument(
        "--template", help="Path to an HTML template file", default=None
    )
    parser.add_argument(
        "--interactive", help="Run in interactive mode", action="store_true"
    )

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif "*" in args.input:
        files = glob.glob(args.input)
        if not os.path.isdir(args.output):
            print(
                f"Output path {args.output} must be a directory for batch conversion."
            )
            return
        batch_convert(files, args.output, args.to_html, args.title, args.css)
    elif args.input and args.output:
        if args.to_html:
            convert_markdown_to_html(
                args.input,
                args.output,
                args.title,
                args.css,
                args.extensions,
                args.template,
            )
        elif args.to_md:
            convert_html_to_markdown(args.input, args.output)
    else:
        print(
            "Please specify the conversion direction using --to_html or --to_md or run in interactive mode with --interactive"
        )


if __name__ == "__main__":
    main()
