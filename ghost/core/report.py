import os
from datetime import datetime

def generate_html_report(url, results):
    report_dir = "results"
    os.makedirs(report_dir, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(report_dir, f"report_{now}.html")

    with open(filename, "w") as f:
        f.write(f"<h1>Scan Report for {url}</h1>")
        for key, value in results.items():
            f.write(f"<h2>{key.title()}</h2><pre>{value}</pre>")
    print(f"[+] Report saved to: {filename}")
