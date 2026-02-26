def extract_http_cookies(pkt,file_name):
    try:
        if not hasattr(pkt, "http"):
            return None

        http = pkt.http
        cookies = []

        if hasattr(http, "cookie"):
            cookie_header = http.cookie
            pairs = cookie_header.split(";")
            for p in pairs:
                if "=" in p:
                    name, value = p.strip().split("=", 1)
                    cookies.append({
                        "name": name,
                        "value": value,
                        "direction": "request"
                    })

        if hasattr(http, "set_cookie"):
            set_cookie_headers = http.set_cookie
            if isinstance(set_cookie_headers, list):
                headers = set_cookie_headers
            else:
                headers = [set_cookie_headers]

            for sc in headers:
                main_part = sc.split(";", 1)[0]
                if "=" in main_part:
                    name, value = main_part.split("=", 1)
                    cookies.append({
                        "name": name,
                        "value": value,
                        "direction": "response"
                    })

        if not cookies:
            return None

        return {
            "file_name":file_name,
            "method": getattr(http, "request_method", ""),
            "host": getattr(http, "host", ""),
            "uri": getattr(http, "request_uri", ""),
            "cookies": cookies
        }

    except Exception as e:
        print("COOKIE GRESKA:", e)
        return None