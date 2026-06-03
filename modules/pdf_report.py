from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import datetime

def crear_pdf_bonito(data, pretexto, filename="social_ai_report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           title="Social AI - Reporte Ético")
    styles = getSampleStyleSheet()
    story = []
    
    # Título principal
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'],
                                 fontSize=24, textColor=colors.darkgreen, alignment=TA_CENTER, spaceAfter=30)
    story.append(Paragraph("🐢 Social AI - Auditoría de Ingeniería Social", title_style))
    
    # Fecha
    story.append(Paragraph(f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
    story.append(Spacer(1, 0.2*inch))
    
    # Datos del objetivo
    story.append(Paragraph("<b>Datos del objetivo</b>", styles["Heading2"]))
    data_text = f"""
    <b>Dominio:</b> {data['domain']}<br/>
    <b>Emails encontrados:</b> {', '.join(data['emails'][:5])}<br/>
    <b>Subdominios:</b> {', '.join(data['subdominios'][:5])}<br/>
    <b>Redes sociales:</b> {', '.join(data['redes_sociales'][:3])}
    """
    story.append(Paragraph(data_text, styles["Normal"]))
    story.append(Spacer(1, 0.2*inch))
    
    # Pretexto generado por IA
    story.append(Paragraph("<b>Pretexto generado por IA (Ollama + Llama3)</b>", styles["Heading2"]))
    story.append(Paragraph(pretexto.replace('\n', '<br/>'), styles["Normal"]))
    story.append(Spacer(1, 0.2*inch))
    
    # Tabla de riesgos
    story.append(Paragraph("<b>Análisis de riesgo humano</b>", styles["Heading2"]))
    data_riesgos = [
        ["Factor", "Riesgo", "Recomendación"],
        ["Emails expuestos", "Alto", "Implementar alias corporativos"],
        ["Subdominios públicos", "Medio", "Reducir superficie de ataque"],
        ["Redes sociales", "Alto", "Política de publicación"]
    ]
    table = Table(data_riesgos, colWidths=[1.5*inch, 1.2*inch, 2.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkgreen),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(table)
    story.append(Spacer(1, 0.3*inch))
    
    # Conclusión ética
    ethical_note = """
    <font color="darkred"><b>⚠️ NOTA ÉTICA IMPORTANTE ⚠️</b></font><br/>
    Este reporte fue generado en un entorno controlado y autorizado.<br/>
    Toda la información debe usarse SOLO para mejorar la postura de seguridad.<br/>
    No se realizaron acciones maliciosas reales contra el objetivo.
    """
    story.append(Paragraph(ethical_note, styles["Normal"]))
    
    # Generar PDF
    doc.build(story)
    print(f"[✓] PDF generado: {filename}")
    return filename
