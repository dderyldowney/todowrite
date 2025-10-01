from __future__ import annotations

import argparse
import os
import re
from html import escape
from pathlib import Path
from typing import Literal


def _render_markdown_to_html_fragment(markdown_text: str) -> str:
    """Render Markdown using a standards-compliant parser with fallbacks.

    Strategy
    --------
    1) Prefer markdown-it-py (CommonMark-compliant) with plugins for
       GFM tables, footnotes, and task lists; enable linkify for autolinks.
    2) Fallback to markdown2 with appropriate extras for tables, footnotes,
       strikethrough, and task lists; add URL autolinking via link-patterns.
    3) Fallback to Python-Markdown with core extensions; apply minimal
       post-processing for autolinks and strikethrough if necessary.

    Parameters
    ----------
    markdown_text : str
        Markdown input text.

    Returns
    -------
    str
        HTML fragment content (no outer HTML wrapper).
    """
    # 1) markdown-it-py + plugins
    try:
        from markdown_it import MarkdownIt

        md = MarkdownIt("commonmark", options_update={"linkify": True, "html": True})
        try:
            md.enable("strikethrough")
        except Exception:
            pass
        plugins_ok = True
        try:
            # Prefer plugins for GFM-like features
            from mdit_py_plugins.footnote import footnote_plugin  # type: ignore[import-not-found]
            from mdit_py_plugins.table import table_plugin  # type: ignore[import-not-found]
            from mdit_py_plugins.tasklists import tasklists_plugin  # type: ignore[import-not-found]

            md = md.use(footnote_plugin).use(tasklists_plugin).use(table_plugin)
        except Exception:
            plugins_ok = False

        if plugins_ok:
            md_input = re.sub(r"~~(.*?)~~", r"<del>\1</del>", markdown_text)
            html = md.render(md_input)
            labels = _collect_footnote_labels(markdown_text)
            html = _normalize_footnote_ids(html, labels)
            # Normalize strike <s> to <del> for consistency across engines
            html = html.replace("<s>", "<del>").replace("</s>", "</del>")
            html = _ensure_footnotes_heading(html)
            html = _inject_footnote_aliases(html, labels)
            # markdown-it-py handles emphasis; strikethrough plugin not required
            if "<del>" not in html and "~~" in markdown_text:
                html = re.sub(r"~~(.*?)~~", r"<del>\1</del>", html)
            return html
        # If plugins missing, prefer markdown2 path below for full features
    except Exception:
        pass

    # 2) markdown2 with extras
    try:
        import markdown2  # type: ignore[import-untyped]

        url_re = re.compile(r"(https?://[^\s<]+)")

        def _linkify_url(match: re.Match[str]) -> str:
            url = match.group(1)
            return f'<a href="{escape(url)}">{escape(url)}</a>'

        extras = {
            "fenced-code-blocks": None,
            "tables": None,
            "footnotes": None,
            "strike": None,
            "task_list": None,
            "code-friendly": None,
            "link-patterns": [(url_re, _linkify_url)],
        }
        html = markdown2.markdown(markdown_text, extras=extras)
        # Normalize strike tag name to <del>
        html = html.replace("<strike>", "<del>").replace("</strike>", "</del>")
        labels = _collect_footnote_labels(markdown_text)
        html = _normalize_footnote_ids(html, labels)
        html = _ensure_footnotes_heading(html)
        html = _inject_footnote_aliases(html, labels)
        return html
    except Exception:
        pass

    # 3) Python-Markdown (markdown)
    try:
        import markdown as _md

        exts = [
            "markdown.extensions.extra",  # includes tables in some dists
            "markdown.extensions.tables",
            "markdown.extensions.fenced_code",
            "markdown.extensions.codehilite",
            "markdown.extensions.footnotes",
            "markdown.extensions.sane_lists",
        ]
        # Try linkify if available
        try:
            import linkify_it  # type: ignore  # noqa: F401

            exts.append("markdown.extensions.linkify")
        except Exception:
            pass

        html = _md.markdown(markdown_text, extensions=exts)
        labels = _collect_footnote_labels(markdown_text)
        html = _normalize_footnote_ids(html, labels)
        html = html.replace("<s>", "<del>").replace("</s>", "</del>")
        html = _ensure_footnotes_heading(html)
        html = _inject_footnote_aliases(html, labels)

        # Minimal post-processing: autolink if linkify not present
        if "markdown.extensions.linkify" not in exts:
            html = _naive_linkify_html(html)

        # Minimal strikethrough fallback if not handled
        if "<del>" not in html and "~~" in markdown_text:
            html = re.sub(r"~~(.*?)~~", r"<del>\1</del>", html)

        return html
    except Exception:
        # Absolute last resort: escape
        return "<pre><code>" + escape(markdown_text) + "</code></pre>"


def _naive_linkify_html(html: str) -> str:
    # Replace bare URLs with anchors; avoids touching existing links
    def _repl(m: re.Match[str]) -> str:
        url = m.group(0)
        return f'<a href="{escape(url)}">{escape(url)}</a>'

    # Only operate in text nodes is complex; we approximate on the full HTML
    return re.sub(r"(?P<url>https?://[^\s<]+)", _repl, html)


def _ensure_footnotes_heading(html: str) -> str:
    # Insert an H2 heading for footnotes if a standard section exists without a title
    if ('class="footnotes"' in html or "class='footnotes'" in html) and ("Footnotes" not in html):
        html = re.sub(
            r"<(div|section)(\s+class=\"footnotes\"[^>]*)>",
            r"<h2>Footnotes</h2><\1\2>",
            html,
            count=1,
        )
    return html


def _collect_footnote_labels(markdown_text: str) -> list[str]:
    # Collect unique footnote labels in order of first reference appearance
    labels: list[str] = []
    for m in re.finditer(r"\[\^([^\]]+)\]", markdown_text):
        label = m.group(1)
        if label not in labels:
            labels.append(label)
    return labels


def _normalize_footnote_ids(html: str, labels: list[str]) -> str:
    if not labels:
        return html
    pattern = re.compile(r"(id|href)=([\"'])(#?)(fnref|fn)[:\-]?(\d+)\2")

    def _sub(m: re.Match[str]) -> str:
        attr, quote, hashmark, kind, num_s = m.groups()
        try:
            idx = int(num_s) - 1
        except ValueError:
            return m.group(0)
        if 0 <= idx < len(labels):
            label = labels[idx]
            return f"{attr}={quote}{hashmark}{kind}:{label}{quote}"
        return m.group(0)

    return pattern.sub(_sub, html)


def _inject_footnote_aliases(html: str, labels: list[str]) -> str:
    if not labels:
        return html
    alias = "".join(
        f'<span id="fn:{escape(label)}"></span><span id="fnref:{escape(label)}"></span>'
        for label in labels
    )
    return html + "\n" + alias


def _indent_level(line: str) -> int:
    # Count leading spaces in multiples of 2; tabs count as 4 spaces
    spaces = 0
    for ch in line:
        if ch == " ":
            spaces += 1
        elif ch == "\t":
            spaces += 4
        else:
            break
    return spaces // 2


def _ensure_list_stack(
    stack: list[tuple[Literal["ul", "ol"], list[str]]], tag: Literal["ul", "ol"], level: int
) -> None:
    # Ensure stack depth equals level+1 (top-level list is level 0)
    # Adjust by popping or pushing new lists as needed
    while len(stack) > level + 1:
        # pop and attach to parent as nested list inside last <li>
        sub_tag, sub_items = stack.pop()
        nested_html = f"<{sub_tag}>" + "".join(sub_items) + f"</{sub_tag}>"
        # append as part of previous li (wrap into last li if needed)
        if stack and stack[-1][1]:
            # inject nested into the previous li
            last = stack[-1][1].pop()
            if last.endswith("</li>"):
                last = last[:-5] + nested_html + "</li>"
            else:
                last = last + nested_html
            stack[-1][1].append(last)
        else:
            # if no parent, create a container li
            stack.append((tag, [f"<li>{nested_html}</li>"]))

    while len(stack) < level + 1:
        stack.append((tag, []))

    # If top tag mismatches, close current and open new
    if stack and stack[-1][0] != tag:
        # Close current level first
        sub_tag, sub_items = stack.pop()
        nested_html = f"<{sub_tag}>" + "".join(sub_items) + f"</{sub_tag}>"
        if stack and stack[-1][1]:
            last = stack[-1][1].pop()
            if last.endswith("</li>"):
                last = last[:-5] + nested_html + "</li>"
            else:
                last = last + nested_html
            stack[-1][1].append(last)
        else:
            stack.append((tag, [f"<li>{nested_html}</li>"]))
        stack.append((tag, []))


def _rebuild_nested_list_html(stack: list[tuple[Literal["ul", "ol"], list[str]]]) -> str:
    # Build nested list HTML from a stack of (tag, items), nesting each deeper level
    if not stack:
        return ""
    html = ""

    # Start from the root
    def build(level: int) -> str:
        tag, items = stack[level]
        content = "".join(items)
        if level + 1 < len(stack):
            # nest the remainder inside the last item
            nested = build(level + 1)
            if content:
                # inject nested into last li
                last_end = content.rfind("</li>")
                if last_end != -1:
                    content = content[:last_end] + nested + content[last_end:]
                else:
                    content += nested
            else:
                content = f"<li>{nested}</li>"
        return f"<{tag}>" + content + f"</{tag}>"

    html = build(0)
    return html


_RE_LINK = re.compile(r"\[(?P<text>[^\]]+)\]\((?P<href>[^\)\s]+)(?:\s+\"(?P<title>[^\"]+)\")?\)")
_RE_CODE_SPAN = re.compile(r"`([^`]+)`")
_RE_IMAGE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^\)\s]+)(?:\s+\"(?P<title>[^\"]+)\")?\)")
_RE_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_RE_ITALIC = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
_RE_STRIKE = re.compile(r"~~([^~]+)~~")
_RE_FOOTNOTE_REF = re.compile(r"\[\^([^\]]+)\]")


def _inline_markup(text: str) -> str:
    """Apply inline Markdown conversions: links and code spans.

    Parameters
    ----------
    text : str
        Input inline text.

    Returns
    -------
    str
        HTML with inline elements converted.
    """
    # Escape first, then re-insert allowed HTML through replacements
    escaped = escape(text)

    # Images ![alt](src "title")
    def _img_sub(m: re.Match[str]) -> str:
        alt = m.group("alt") or ""
        src = m.group("src")
        title = m.group("title")
        title_attr = f' title="{escape(title)}"' if title else ""
        return f'<img src="{escape(src)}" alt="{escape(alt)}"{title_attr} />'

    escaped = _RE_IMAGE.sub(_img_sub, escaped)

    # Links [text](href "title")
    def _link_sub(m: re.Match[str]) -> str:
        label = m.group("text")
        href = m.group("href")
        title = m.group("title")
        title_attr = f' title="{escape(title)}"' if title else ""
        return f'<a href="{escape(href)}"{title_attr}>{escape(label)}</a>'

    escaped = _RE_LINK.sub(_link_sub, escaped)

    # Inline code spans
    escaped = _RE_CODE_SPAN.sub(lambda m: f"<code>{escape(m.group(1))}</code>", escaped)

    # Emphasis: bold then italic
    escaped = _RE_BOLD.sub(lambda m: f"<strong>{m.group(1)}</strong>", escaped)
    escaped = _RE_ITALIC.sub(lambda m: f"<em>{m.group(1)}</em>", escaped)

    # Strikethrough
    escaped = _RE_STRIKE.sub(lambda m: f"<del>{m.group(1)}</del>", escaped)

    # Footnote references
    escaped = _RE_FOOTNOTE_REF.sub(
        lambda m: f'<sup id="fnref:{escape(m.group(1))}"><a href="#fn:{escape(m.group(1))}">{escape(m.group(1))}</a></sup>',
        escaped,
    )
    return escaped


def _looks_like_table_header(line: str) -> bool:
    return bool(re.match(r"^\s*\|.*\|\s*$", line))


def _looks_like_table_sep(line: str) -> bool:
    # e.g. |:---|---:|:---:|
    # accept without leading/trailing pipes too
    line = line.strip()
    if not line:
        return False
    # Remove leading/trailing pipes for parsing
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    parts = [p.strip() for p in line.split("|")]
    if not parts:
        return False
    return all(re.fullmatch(r":?-{3,}:?", p) is not None for p in parts)


def _looks_like_table_row(line: str) -> bool:
    return bool(re.match(r"^\s*\|.*\|\s*$", line))


def _render_table(header_line: str, sep_line: str, row_lines: list[str]) -> str:
    headers = _split_table_row(header_line)
    aligns = _parse_alignments(sep_line)
    # normalize alignments length
    if len(aligns) < len(headers):
        aligns.extend(["left"] * (len(headers) - len(aligns)))

    thead_cells = []
    for i, h in enumerate(headers):
        align = aligns[i] if i < len(aligns) else "left"
        thead_cells.append(f'<th style="text-align:{align}">{_inline_markup(h)}</th>')
    thead_html = "<thead><tr>" + "".join(thead_cells) + "</tr></thead>"

    tbody_rows: list[str] = []
    for row in row_lines:
        cols = _split_table_row(row)
        tds = []
        for i, c in enumerate(cols):
            align = aligns[i] if i < len(aligns) else "left"
            tds.append(f'<td style="text-align:{align}">{_inline_markup(c)}</td>')
        tbody_rows.append("<tr>" + "".join(tds) + "</tr>")
    tbody_html = "<tbody>" + "".join(tbody_rows) + "</tbody>"

    return "<table>" + thead_html + tbody_html + "</table>"


def _split_table_row(line: str) -> list[str]:
    # Strip and remove boundary pipes
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    # Split on unescaped pipes; preserve escaped pipes and backslashes
    cols: list[str] = []
    buf: list[str] = []
    escaped = False
    for ch in s:
        if escaped:
            buf.append(ch)
            escaped = False
        elif ch == "\\":
            escaped = True
            buf.append("\\")  # keep the backslash for later escaping
        elif ch == "|":
            cols.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    cols.append("".join(buf).strip())
    # Unescape \| to |; keep \\ as \\ (rendered as \)
    cols = [c.replace("\\|", "|") for c in cols]
    return cols


def _parse_alignments(sep_line: str) -> list[str]:
    s = sep_line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    out: list[str] = []
    for seg in [p.strip() for p in s.split("|")]:
        left = seg.startswith(":")
        right = seg.endswith(":")
        if left and right:
            out.append("center")
        elif right:
            out.append("right")
        else:
            out.append("left")
    return out


def _page_template(content_html: str, title: str = "Automated Farming System API") -> str:
    """Wrap HTML fragment in the project’s styled HTML page.

    Parameters
    ----------
    content_html : str
        Body content HTML.
    title : str, optional
        Title for the page, by default "Automated Farming System API".

    Returns
    -------
    str
        Complete HTML document.
    """
    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{escape(title)}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #2c5530; border-bottom: 3px solid #4a7c59; padding-bottom: 10px; margin-bottom: 30px; }}
        h2 {{ color: #4a7c59; border-bottom: 2px solid #6fa777; padding-bottom: 8px; margin-top: 40px; }}
        h3 {{ color: #5d8a6b; margin-top: 30px; }}
        .codehilite {{ background-color: #f8f8f8; border: 1px solid #e1e1e1; border-radius: 4px; padding: 15px; overflow-x: auto; margin: 20px 0; }}
        .codehilite pre {{ margin: 0; font-family: 'Courier New', monospace; font-size: 14px; }}
        ul, ol {{ margin: 15px 0; padding-left: 30px; }}
        li {{ margin: 8px 0; }}
        a {{ color: #4a7c59; text-decoration: none; }}
        a:hover {{ color: #2c5530; text-decoration: underline; }}
        hr {{ border: none; height: 2px; background: linear-gradient(90deg, #4a7c59, #6fa777, #4a7c59); margin: 40px 0; }}
    </style>
    
</head>
<body>
    <div class=\"container\">
        {content_html}
    </div>
</body>
</html>
"""


def convert_md_to_html(md_file_path: str, output_html_path: str) -> None:
    """Convert Markdown file into a styled HTML document.

    The converter maps common Markdown constructs to a predictable HTML
    structure and wraps it in the project’s standard page template for an
    identical visual style to the existing docs site.

    Parameters
    ----------
    md_file_path : str
        Path to the input Markdown file.
    output_html_path : str
        Path where the output HTML file will be written.
    """
    if not os.path.isfile(md_file_path):
        raise FileNotFoundError(f"The file {md_file_path} does not exist.")

    md_text = Path(md_file_path).read_text(encoding="utf-8")
    content_html = _render_markdown_to_html_fragment(md_text)
    full_html = _page_template(content_html)
    # Inject task list inputs if renderer emitted raw [ ]/[x] labels
    full_html = _inject_tasklist_inputs(full_html)
    # Final normalization to guarantee consistent strikethrough markup
    full_html = re.sub(r"~~(.*?)~~", r"<del>\1</del>", full_html)
    full_html = full_html.replace("<s>", "<del>").replace("</s>", "</del>")
    # Normalize task list checkbox input attributes for deterministic tests
    full_html = _normalize_tasklist_inputs(full_html)

    out_path = Path(output_html_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(full_html, encoding="utf-8")


def _normalize_tasklist_inputs(html: str) -> str:
    pattern = re.compile(r"<input[^>]*type=\"checkbox\"[^>]*?/?>", re.IGNORECASE)

    def repl(m: re.Match[str]) -> str:
        tag = m.group(0)
        # detect if tag had checked in any form
        had_checked = re.search(r"\schecked(=\"[^\"]*\")?", tag, flags=re.IGNORECASE) is not None
        # Always return normalized, ordered attributes
        return (
            '<input type="checkbox" disabled checked />'
            if had_checked
            else '<input type="checkbox" disabled />'
        )

    return pattern.sub(repl, html)


def _inject_tasklist_inputs(html: str) -> str:
    # Convert list items starting with [ ] / [x] into checkbox inputs
    pattern = re.compile(r"(<li>)(\s*\[(?P<mark>[ xX])\]\s*)(?P<label>.*?)(</li>)", re.DOTALL)

    def repl(m: re.Match[str]) -> str:
        mark = m.group("mark").lower()
        label = m.group("label")
        checked = " checked" if mark == "x" else ""
        return f'<li><input type="checkbox" disabled{checked} /> {label}</li>'

    return pattern.sub(repl, html)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert Markdown to styled HTML index page.")
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
