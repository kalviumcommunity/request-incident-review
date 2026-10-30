"""Editable Task 1: event context is already generated once per request."""
import json


def format_event(event):
    return json.dumps({
        "time": event["timestamp"],
        "severity": event["level"],
        "id": event["request_id"],
        "text": event["message"],
    }, separators=(",", ":"))
