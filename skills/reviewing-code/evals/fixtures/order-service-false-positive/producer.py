import json

ALLOWED_EVENTS = {"page_view", "click", "purchase"}


def build_payload(event):
    if event.get("type") not in ALLOWED_EVENTS:
        raise ValueError("unknown event type")
    if not isinstance(event.get("data"), dict):
        raise ValueError("data must be an object")
    return json.dumps(event)
