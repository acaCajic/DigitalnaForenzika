import json

def generate_report(results):
    report = {
        "extracted_credentials": results,
    }

    with open("forensic_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)