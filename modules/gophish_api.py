import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class GophishController:
    def __init__(self):
        self.url = os.getenv("GOPHISH_URL", "https://localhost:3333")
        self.api_key = os.getenv("GOPHISH_API_KEY")
        self.verify_ssl = False  # Solo para pruebas locales
    
    def crear_campaign(self, name, target_emails, pretexto):
        if not self.api_key:
            print("[!] GOPHISH_API_KEY no configurada en .env")
            return None
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Crear grupo de objetivos
        group_data = {
            "name": f"Grupo_{name}",
            "targets": [{"email": email} for email in target_emails[:5]]
        }
        group_resp = requests.post(f"{self.url}/api/groups/", json=group_data, headers=headers, verify=self.verify_ssl)
        
        if group_resp.status_code == 201:
            group_id = group_resp.json()["id"]
            # Crear campaña
            campaign_data = {
                "name": f"Simulación_{name}",
                "group_id": group_id,
                "page": {"name": "Página de prueba", "html": f"<html><body><h1>{pretexto[:200]}</h1></body></html>"},
                "smtp": {"name": "Servidor local"},
                "url": "http://localhost:8080",
                "send_by_date": "2025-12-31T23:59:59Z"
            }
            camp_resp = requests.post(f"{self.url}/api/campaigns/", json=campaign_data, headers=headers, verify=self.verify_ssl)
            if camp_resp.status_code == 201:
                print(f"[✓] Campaña creada con ID: {camp_resp.json()['id']}")
                return camp_resp.json()
        return None
