"""Render model markdown with the same suspicion as user input.

- Raw HTML in the reply is escaped, never rendered.
- Images load only from allowlisted hosts. Others are dropped: an image request needs no
  click, so a query string on it is data leaving silently.
- Links to allowlisted hosts render normally. Others render as plain text showing the real
  URL, so "click here to reauthenticate" cannot hide where it goes.
"""

import html
import re
from urllib.parse import urlsplit

IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def host_ok(url: str, allowed: set[str]) -> bool:
    parts = urlsplit(url)
    return parts.scheme == "https" and (parts.hostname or "") in allowed


def render(markdown: str, allowed_links: set[str], allowed_images: set[str]) -> str:
    text = html.escape(markdown, quote=True)

    def image(m):
        alt, url = m.group(1), html.unescape(m.group(2))
        return f'<img alt="{alt}" src="{html.escape(url)}">' if host_ok(url, allowed_images) else f"[image removed: {alt}]"

    def link(m):
        label, url = m.group(1), html.unescape(m.group(2))
        if host_ok(url, allowed_links):
            return f'<a href="{html.escape(url)}" rel="noopener noreferrer">{label}</a>'
        return f"{label} ({html.escape(url)})"

    return LINK.sub(link, IMAGE.sub(image, text))
