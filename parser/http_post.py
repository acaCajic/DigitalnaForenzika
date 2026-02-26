import binascii

def extract_http_post(packet):
    if not hasattr(packet, "http"):
        return None

    http = packet.http

    if not hasattr(http, "request_method"):
        return None

    if http.request_method != "POST":
        return None

    if not hasattr(http, "file_data"):
        return None
    
    hex_data = http.file_data.replace(":", "")
    raw = binascii.unhexlify(hex_data)
    body = raw.decode("utf-8")

    content_type = getattr(http,"content_type","unknown")

    return {
        "method":"POST",
        "host": getattr(http, "host", ""),
        "uri": getattr(http, "request_uri", ""),
        "content_type":content_type,
        "body": body
    }