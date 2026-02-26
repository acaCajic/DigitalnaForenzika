def extract_http_token(pkt,file_name):
    try:
        if not hasattr(pkt, "http"):
            return None

        http = pkt.http
 
        if hasattr(http, "authorization"):
            auth = http.authorization
            print(auth)
            if auth.lower().startswith("bearer "):
                token = auth.split(" ", 1)[1]

                return {
                    "file_name":file_name,
                    "source": "Authorization header",
                    "auth_type": "Bearer",
                    "method": getattr(http, "request_method", ""),
                    "host": getattr(http, "host", ""),
                    "uri": getattr(http, "request_uri", ""),
                    "token": token
                }

        if hasattr(http, "file_data"):
            body = http.file_data.lower()
            token_keys = ["access_token", "token", "jwt"]

            for key in token_keys:
                if key in body:
                    parts = body.split("&")
                    for p in parts:
                        if p.startswith(key + "="):
                            token = p.split("=", 1)[1]

                            return {
                                "file_name": file_name,
                                "source": "HTTP body",
                                "auth_type": "Token",
                                "method": getattr(http, "request_method", ""),
                                "host": getattr(http, "host", ""),
                                "uri": getattr(http, "request_uri", ""),
                                "token": token
                            }

        return None

    except Exception as e:
        print("GRESKA TOKEN:", e)
        return None