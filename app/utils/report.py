from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import os
from datetime import datetime

def generate_pdf(prompt, status, details):
    filename = f"report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join("static", filename)

    doc = SimpleDocTemplate(filepath)
    elements = []

    styles = getSampleStyleSheet()

    elements.append(Paragraph("<b>AI Testing Report</b>", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(f"<b>Prompt:</b> {prompt}", styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(f"<b>Status:</b> {status}", styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(f"<b>Details:</b> {details}", styles["Normal"]))

    doc.build(elements)

    return filename
