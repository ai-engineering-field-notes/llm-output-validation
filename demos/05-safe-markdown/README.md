# Model-written links and images

## Problem

`before/render.py` turns the model's markdown into HTML. A prompt-injected model can write a link whose text says one thing and whose URL goes somewhere else, or an image whose URL carries data in its query string. The image needs no click: the browser fetches it as soon as the reply renders.

## Business pain

Phishing and data exfiltration through the assistant your staff already trust. In August 2024 PromptArmor showed Slack AI could be steered into rendering a "click here to reauthenticate" link carrying a private API key (vendor research; Slack patched it).

## Fix

`after/render.py` escapes raw HTML, loads images only from allowlisted hosts and drops the rest, and renders links only to allowlisted hosts over HTTPS. Any other link becomes plain text with its full URL beside the label. Host checks parse the URL, so `docs.example.com.attacker.net` and `example.com@attacker.net` do not pass.

Pair it with a Content Security Policy `img-src` that matches the image allowlist, so a renderer bug elsewhere cannot load an attacker's image either.

## Proof

```
uv run pytest demos/05-safe-markdown
```

Before: the phishing link, the exfiltrating image and a script tag all render. After: the link shows its real destination as text, the image is removed, the script is text, allowed links and images still work, and three lookalike URLs are rejected.
