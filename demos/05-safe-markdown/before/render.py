"""Chat UI: the model's reply is markdown, converted to HTML and shown as-is."""

import re


def render(markdown: str) -> str:
    html = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", r'<img alt="\1" src="\2">', markdown)
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', html)
