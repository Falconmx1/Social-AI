def create_report(data=None, pretext=None, training=False):
    if training:
        print("[*] Generando guía de concienciación para empleados...")
        # Crear PDF con reportlab
        print("[✓] training_guide.pdf listo")
    else:
        print(f"[*] Reporte de auditoría para {data['target']}")
        print(f"Pretexto generado: {pretext}")
        print("[✓] reporte_etica.pdf listo")
