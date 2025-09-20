from __future__ import annotations

import argparse
import os
from pathlib import Path

import markdown


def convert_md_to_html(md_file_path: str, output_html_path: str) -> None:
    """
    Convert a Markdown file to HTML and write it to the given output path.

    Parameters
    ----------
    md_file_path : str
        Path to the input Markdown file.
    output_html_path : str
        Path to the output HTML file to write.
    """
    if not os.path.isfile(md_file_path):
        raise FileNotFoundError(f"The file {md_file_path} does not exist.")

    with open(md_file_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    html_content = markdown.markdown(md_content, extensions=["fenced_code", "codehilite"])

    out_path = Path(output_html_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_content, encoding="utf-8")

    print(f"Conversion successful! HTML file saved as {output_html_path}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert README.md to HTML.")
    parser.add_argument(
        "--in",
        dest="inp",
        default="README.md",
        help="Input Markdown file (default: README.md)",
    )
    parser.add_argument(
        "--out",
        dest="out",
        default="docs/index.html",
        help="Output HTML file (default: docs/index.html)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    convert_md_to_html(args.inp, args.out)
