import requests
from rich.console import Console

console = Console()

class Scanner:
    def __init__(self, url):
        self.url = url.rstrip('/')

    def check_headers(self):
        console.print("[*] Checking security headers...", style="bold cyan")
        try:
            r = requests.get(self.url)
            headers = r.headers
            expected = ["X-Frame-Options", "X-XSS-Protection", "Strict-Transport-Security", "Content-Security-Policy"]
            result = {h: (h in headers) for h in expected}
            return result
        except Exception as e:
            console.print(f"[!] Error: {e}", style="bold red")
            return {}

    def check_csrf(self):
        console.print("[*] Checking for CSRF token on forms...", style="bold cyan")
        try:
            r = requests.get(self.url)
            return "csrfmiddlewaretoken" in r.text
        except:
            return False

    def check_xss(self):
        console.print("[*] Checking for reflected XSS...", style="bold cyan")
        try:
            payload = "<script>alert(1)</script>"
            test_url = f"{self.url}?q={payload}"
            r = requests.get(test_url)
            return payload in r.text
        except:
            return False

    def check_sql_injection(self):
        console.print("[*] Checking for SQL injection signs...", style="bold cyan")
        payloads = ["' OR '1'='1", "'; DROP TABLE users; --"]
        for p in payloads:
            try:
                r = requests.get(f"{self.url}?id={p}")
                if "sql" in r.text.lower() or "error" in r.text.lower():
                    return True
            except:
                continue
        return False

    def run_all_checks(self):
        return {
            "headers": self.check_headers(),
            "csrf": self.check_csrf(),
            "xss": self.check_xss(),
            "sql_injection": self.check_sql_injection()
        }
