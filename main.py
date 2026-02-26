from parser.pcap_loader import load_pcap
from parser.form_parser import parse_form_data
from parser.http_post import extract_http_post
from parser.http_get import extract_http_get
from parser.http_basic_auth import extract_http_basic_auth
from parser.http_token import extract_http_token
from parser.http_cookies import extract_http_cookies
from reporting.report_generator import generate_report

def main():
    extracted_forms = []

    captures = load_pcap(
        r"C:\Users\ACA_PC\Desktop\Digitalna Forenzika\network_evidence",
        display_filter="http.request"
    )
    for file_name, capture in captures:

        for pkt in capture:
            form = extract_http_post(pkt)
            if form:            
                parsed_body = parse_form_data(
                form["content_type"],
                form["body"]
                )
                extracted_forms.append({
                "file_name": file_name,
                "method":"POST",
                "host": form["host"],
                "uri": form["uri"],
                "content_type": form["content_type"],
                "form_data": parsed_body
                })
                continue

            get = extract_http_get(pkt,file_name)
            if get:
                extracted_forms.append(get)
                continue
            basic_auth = extract_http_basic_auth(pkt,file_name)
            if basic_auth:
                extracted_forms.append(basic_auth)
                continue
            token = extract_http_token(pkt,file_name)
            if token:
                extracted_forms.append(token)
                continue
            cookie_data = extract_http_cookies(pkt,file_name)
            if cookie_data:
                extracted_forms.append(cookie_data)
        capture.close()

    generate_report(extracted_forms)

if __name__ == "__main__":
    main()