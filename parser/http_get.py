from urllib.parse import urlparse, parse_qs

def extract_http_get(packet,file_name):
    if not hasattr(packet, "http"):
        return None

    http = packet.http

    if not hasattr(http, "request_method"):
        return None

    if http.request_method != "GET":
        return None

    uri = getattr(http, "request_uri", "")
    parsed = urlparse(uri)
    params = parse_qs(parsed.query)

    if not params:
        return None
    
    return {
        "file_name":file_name,
        "method": "GET",
        "host": getattr(http, "host", ""),
        "uri": uri,
        "form_data": params
    }