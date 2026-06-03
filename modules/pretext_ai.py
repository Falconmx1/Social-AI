import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class PretextGenerator:
    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = "llama3"  # o "mistral", "phi3", etc.
        self.check_ollama()
    
    def check_ollama(self):
        try:
            resp = requests.get(f"{self.ollama_url}/api/tags")
            if resp.status_code == 200:
                print("[✓] Ollama conectado")
            else:
                print("[!] Ollama no disponible, usando modo offline")
                self.ollama_available = False
        except:
            print("[!] Ollama no instalado. Instálalo con: curl -fsSL https://ollama.com/install.sh | sh")
            print("[!] Luego: ollama pull llama3")
            self.ollama_available = False
    
    def generate(self, target_data, pretext_type="phishing"):
        if self.ollama_available:
            prompt = f"""
            Eres un experto en seguridad ofensiva ética. Genera un pretexto REALISTA para {pretext_type}.
            Datos del objetivo: {json.dumps(target_data, indent=2)}
            
            El pretexto debe:
            1. Ser creíble y profesional
            2. Usar ingeniería social
            3. Incluir un llamado a la acción (ej. hacer clic, llamar, dar info)
            4. Tener advertencia de que es simulación autorizada
            
            Devuelve SOLO el texto del pretexto.
            """
            
            try:
                resp = requests.post(f"{self.ollama_url}/api/generate", 
                                   json={"model": self.model, "prompt": prompt, "stream": False})
                if resp.status_code == 200:
                    return resp.json()["response"]
            except:
                pass
        
        # Fallback offline
        return f"""=== PRETEXTO SIMULADO (IA offline) ===
Asunto: Actualización de seguridad requerida
Hola {target_data.get('emails', ['usuario'])[0].split('@')[0]},

Soy del equipo de TI. Hemos detectado actividad inusual en tu cuenta.
Por favor, verifica tu identidad en: https://portal-seguro-{target_data['domain']}/verify

Esta es una SIMULACIÓN AUTORIZADA de ingeniería social.
=== FIN DEL PRETEXTO ===
"""
