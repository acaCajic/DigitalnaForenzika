import base64

def extract_http_basic_auth(pkt,file_name):
    try:
        if not hasattr(pkt, "http"):
            return None

        http = pkt.http

        if hasattr(http, "credentials"):
            creds = http.credentials

            if ":" in creds:
                username, password = creds.split(":", 1)
                return {
                    "file_name":file_name,
                    "method": getattr(http, "request_method", ""),
                    "host": getattr(http, "host", ""),
                    "uri": getattr(http, "request_uri", ""),
                    "auth_type": "Basic",
                    "username": username,
                    "password": password
                }

        if hasattr(http, "authorization"):
            auth_header = http.authorization

            if not auth_header.startswith("Basic "):
                return None

            encoded_creds = auth_header.split(" ", 1)[1]

            decoded = base64.b64decode(encoded_creds).decode("utf-8")

            if ":" not in decoded:
                return None

            username, password = decoded.split(":", 1)

            return {
                "file_name":file_name,
                "method": getattr(http, "request_method", ""),
                "host": getattr(http, "host", ""),
                "uri": getattr(http, "request_uri", ""),
                "auth_type": "Basic",
                "username": username,
                "password": password
            }

        return None

    except Exception as e:
        print("GRESKA U BASIC AUTH:", e)
        return None