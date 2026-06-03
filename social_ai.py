#!/usr/bin/env python3
import argparse
import sys
from utils.banner import show_tortuga
from modules.osint_scraper import EthicalOSINT
from modules.pretext_ai import PretextGenerator
from modules.pdf_report import crear_pdf_bonito
from modules.gophish_api import GophishController

def main():
    parser = argparse.ArgumentParser(description="Social AI - Herramienta Ética")
    parser.add_argument("--target", help="Dominio objetivo (ej: empresa.com)")
    parser.add_argument("--mode", choices=["audit", "training", "phish"], default="audit")
    parser.add_argument("--ethical", action="store_true", required=True, help="Modo ético OBLIGATORIO")
    parser.add_argument("--generate-training", action="store_true", help="Genera guía de entrenamiento")
    
    args = parser.parse_args()
    show_tortuga()
    
    if not args.ethical:
        print("[❌] ERROR: Debes usar --ethical. El mal uso es ILEGAL.")
        sys.exit(1)
    
    if args.generate_training:
        print("[*] Generando guía de concienciación...")
        crear_pdf_bonito({"domain": "training"}, "Guía anti-phishing para empleados", "training_guide.pdf")
        return
    
    if not args.target:
        print("[!] Usa --target dominio.com")
        return
    
    # Fase 1: OSINT real
    print(f"\n[🐢] Fase 1: OSINT ético en {args.target}")
    osint = EthicalOSINT(args.target)
    target_data = osint.run()
    
    # Fase 2: IA genera pretexto
    print(f"\n[🤖] Fase 2: IA generando pretexto (Ollama + Llama3)")
    ai = PretextGenerator()
    pretext = ai.generate(target_data, "phishing" if args.mode == "phish" else "audit")
    
    # Fase 3: Reporte PDF bonito
    print(f"\n[📄] Fase 3: Generando reporte PDF")
    crear_pdf_bonito(target_data, pretext, f"reporte_{args.target}.pdf")
    
    # Fase 4: (Opcional) Enviar campaña controlada con Gophish
    if args.mode == "phish" and target_data["emails"]:
        print(f"\n[🎣] Fase 4: Creando simulación de phishing (Gophish)")
        gophish = GophishController()
        gophish.crear_campaign(args.target, target_data["emails"], pretext)
    
    print("\n[✅] Auditoría completada éticamente. Revisa el PDF generado.")

if __name__ == "__main__":
    main()
