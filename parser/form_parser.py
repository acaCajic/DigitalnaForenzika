import json
import urllib.parse
import re

def parse_form_data(content_type, body):
    if "application/json" in content_type:
        try:
            return json.loads(body)
        except:
            return {}

    if "application/x-www-form-urlencoded" in content_type:
        return urllib.parse.parse_qs(body)

    
    if "multipart/form-data" in content_type:
        form_data = {}

        match = re.search(r"boundary=(.+)", content_type)
        if not match:
            return {}

        boundary = "--" + match.group(1)

        parts = body.split(boundary)

        for part in parts:
            part = part.strip()

            if not part or part == "--":
                continue

            if "\r\n\r\n" not in part:
                continue

            headers, value = part.split("\r\n\r\n", 1)

            name_match = re.search(r'name="([^"]+)"', headers)
            if not name_match:
                continue

            name = name_match.group(1)
            value = value.strip().rstrip("\r\n")

            form_data[name] = value

        return form_data

    return {"raw": body}