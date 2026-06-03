#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from utils.banner import show_tortuga
from modules.recon import osint_scan
from modules.pretext_gen import generate_pretext
from modules.report import create_report

def main():
    parser = argparse.ArgumentParser(description="Social AI - Ingeniería Social con IA")
    parser.add_argument("--target", help="Dominio, email o empresa objetivo")
    parser.add_argument("--mode", choices=["audit", "training"], default="audit")
    parser.add_argument("--ethical", action="store_true", help="Modo ético (solo simulación)")
    parser.add_argument("--generate-training", action="store_true", help="Genera reporte de entrenamiento")
    
    args = parser.parse_args()
    
    # Banner siempre presente
    show_tortuga()
    
    if args.generate_training:
        create_report(training=True)
        return
    
    if not args.target:
        print("[!] Usa --target o --generate-training")
        return
    
    if not args.ethical:
        print("[⚠] Modo NO ético no permitido. Usa --ethical para simulación autorizada.")
        return
    
    print(f"[+] Iniciando auditoría ética en: {args.target}")
    data = osint_scan(args.target)
    pretext = generate_pretext(data)
    create_report(data, pretext, training=False)
    print("[✓] Reporte generado: reporte_etica.pdf")

if __name__ == "__main__":
    main()
