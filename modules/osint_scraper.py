import requests
from bs4 import BeautifulSoup
import urllib.robotparser
from urllib.parse import urlparse, urljoin
import re
import tldextract

class EthicalOSINT:
    def __init__(self, target_domain):
        self.domain = target_domain
        self.parsed = urlparse(f"http://{target_domain}")
        self.base_url = f"{self.parsed.scheme or 'https'}://{self.parsed.netloc or self.domain}"
        self.results = {
            "emails": set(),
            "subdomains": set(),
            "urls": set(),
            "social_links": set(),
            "technologies": []
        }
        self.check_robots()
    
    def check_robots(self):
        robots_url = f"{self.base_url}/robots.txt"
        self.rp = urllib.robotparser.RobotFileParser()
        self.rp.set_url(robots_url)
        try:
            self.rp.read()
            print(f"[✓] Robots.txt respetado: {robots_url}")
        except:
            print("[!] No se pudo leer robots.txt, asumiendo permisivo")
            self.rp = None
    
    def can_scrape(self, url):
        if self.rp:
            return self.rp.can_fetch("*", url)
        return True
    
    def scrape_emails(self, url):
        if not self.can_scrape(url):
            print(f"[!] Saltando {url} por robots.txt")
            return
        try:
            resp = requests.get(url, timeout=5, headers={"User-Agent": "SocialAI-Ethical-Bot/1.0"})
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.' + re.escape(tldextract.extract(self.domain).suffix), resp.text)
            self.results["emails"].update(emails)
        except:
            pass
    
    def get_subdomains(self):
        # Usa crt.sh (certificate transparency, público y ético)
        try:
            url = f"https://crt.sh/?q=%.{self.domain}&output=json"
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                for entry in resp.json():
                    name = entry.get('name_value', '')
                    if name and self.domain in name:
                        self.results["subdomains"].add(name)
        except:
            pass
    
    def run(self):
        print(f"[*] Escaneando {self.domain} éticamente...")
        self.get_subdomains()
        # Escanea homepage por emails
        self.scrape_emails(self.base_url)
        # Busca redes sociales
        try:
            resp = requests.get(self.base_url, timeout=5)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                if 'twitter.com' in a['href'] or 'linkedin.com' in a['href'] or 'facebook.com' in a['href']:
                    self.results["social_links"].add(a['href'])
        except:
            pass
        
        return {
            "domain": self.domain,
            "emails": list(self.results["emails"])[:10],
            "subdominios": list(self.results["subdomains"])[:10],
            "redes_sociales": list(self.results["social_links"]),
            "urls_encontradas": list(self.results["urls"])[:20]
        }
