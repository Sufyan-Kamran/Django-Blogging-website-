import json


def handle_tags(data):
    if "tags" in data:
        try:
            tags_data = json.loads(data["tags"])
            data["tags"] = tags_data
        except (json.JSONDecodeError, TypeError):
            pass
    return data
