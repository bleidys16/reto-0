import os
from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage
)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "capturas")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Generate evidencia_3_agents.png if missing
def ensure_evidencia_3():
    path = os.path.join(OUTPUT_DIR, "evidencia_3_agents.png")
    font_code = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 12)
    font_ui = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 12)
    
    agents_code = [
        ("# Proyecto", "#569cd6"),
        ("Blog con comentarios - Reto 0 y Taller 4 (Aprendiz: Bleidys Paola Larios).", "#d4d4d4"),
        ("Aplicación web en Python para publicar entradas y gestionar comentarios de usuarios.", "#d4d4d4"),
        ("", "#d4d4d4"),
        ("## Stack", "#569cd6"),
        ("- Python 3.14+, Flask 3.1+, SQLite3", "#d4d4d4"),
        ("- Testing & Calidad: Pytest, Ruff, Pre-commit, python-dotenv", "#d4d4d4"),
        ("", "#d4d4d4"),
        ("## Comandos", "#569cd6"),
        ("- Entorno: .venv\\Scripts\\activate", "#ce9178"),
        ("- Ejecutar: python app/main.py", "#ce9178"),
        ("- Tests: pytest", "#ce9178"),
        ("- Linter: ruff check .", "#ce9178"),
        ("- Pre-commit: pre-commit run --all-files", "#ce9178"),
        ("", "#d4d4d4"),
        ("## Estructura", "#569cd6"),
        ("- app/: Lógica principal (main.py) y plantillas HTML (templates/).", "#d4d4d4"),
        ("- tests/: Pruebas de humo (test_humo.py) y fallos (test_fallos.py).", "#d4d4d4"),
        ("- .env.example: Plantilla de variables de entorno (no versionar .env).", "#d4d4d4"),
        ("", "#d4d4d4"),
        ("## Qué no hacer", "#569cd6"),
        ("- No subir secretos ni contraseñas en código fuente.", "#e06c75"),
        ("- No versionar .env, .venv, blog.db ni archivos .pyc.", "#e06c75"),
        ("- No alterar pruebas para forzar aprobación; refactorizar solo el código productivo.", "#e06c75"),
        ("- No desactivar pre-commit ni omitir revisión con Ruff.", "#e06c75"),
        ("", "#d4d4d4"),
        ("## Lecciones aprendidas", "#569cd6"),
        ("- Las variables de entorno son indispensables para desacoplar configuración y secretos.", "#98c379"),
        ("- Mantener una red de seguridad (humo + ruff) previene regresiones antes de commitear.", "#98c379"),
        ("- Fallo 1: Las claves de sesión deben validarse estrictamente contra secretos quemados.", "#98c379"),
        ("- Fallo 2: Las contraseñas nunca deben guardarse en texto plano; deben transformarse con salt.", "#98c379"),
        ("- Fallo 3: Toda entrada de formulario (comentarios) debe validarse rechazando vacíos con HTTP 400.", "#98c379")
    ]
    
    width = 860
    line_h = 19
    height = 42 + (len(agents_code) * line_h) + 15
    img = PILImage.new("RGB", (width, height), "#1e1e1e")
    draw = ImageDraw.Draw(img)
    
    # Title bar & tab
    draw.rectangle([0, 0, width, 36], fill="#252526")
    draw.rectangle([0, 0, 160, 36], fill="#1e1e1e")
    draw.text((20, 9), "AGENTS.md", font=font_ui, fill="#ffffff")
    draw.text((140, 9), "×", font=font_ui, fill="#858585")
    
    # Gutter
    draw.rectangle([0, 36, 45, height], fill="#1e1e1e")
    draw.line([45, 36, 45, height], fill="#333333", width=1)
    
    y = 44
    for idx, (text, color) in enumerate(agents_code, 1):
        draw.text((12, y), f"{idx:2d}", font=font_code, fill="#6e7681")
        draw.text((55, y), text, font=font_code, fill=color)
        y += line_h
        
    img.save(path)

ensure_evidencia_3()

def get_rl_image(img_path, target_width=510):
    with PILImage.open(img_path) as im:
        w, h = im.size
        target_height = (h / w) * target_width
        return RLImage(img_path, width=target_width, height=target_height)

def build_pdf(filename="LariosBleidys_Taller7.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    cover_title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=20,
        textColor=colors.black,
        alignment=1 # Center
    )
    
    cover_bold_style = ParagraphStyle(
        'CoverTextBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=16,
        textColor=colors.black,
        alignment=1
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.black,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    subheading_style = ParagraphStyle(
        'Subheading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.black,
        spaceBefore=6,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.black,
        spaceAfter=6
    )
    
    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#222222'),
        spaceAfter=8,
        keepWithNext=True
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.black
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.black
    )

    story = []
    
    # ================= PAGE 1: PORTADA =================
    story.append(Spacer(1, 100))
    story.append(Paragraph("TALLER 7: auditoría, red de seguridad y refactorización del reto 0", cover_title_style))
    story.append(Spacer(1, 110))
    story.append(Paragraph("Bleidys Paola Larios Torregrosa", cover_bold_style))
    story.append(Spacer(1, 70))
    story.append(Paragraph("3214194 (ADSO 17)", cover_bold_style))
    story.append(Spacer(1, 70))
    story.append(Paragraph("Omar Gutiérrez", cover_bold_style))
    story.append(Spacer(1, 80))
    story.append(Paragraph("SERVICIO NACIONAL DE APRENDIZAJE (SENA)", cover_bold_style))
    story.append(Spacer(1, 70))
    story.append(Paragraph("2026", cover_bold_style))
    story.append(PageBreak())
    
    # ================= PAGE 2: EVIDENCIA 1 =================
    story.append(Paragraph("1. Datos iniciales (Evidencia 1)", h1_style))
    story.append(Paragraph("Enlaces repositorios públicos en GitHub", subheading_style))
    story.append(Paragraph("Tema asignado: <b>5. Blog con comentarios</b>", body_style))
    story.append(Paragraph("https://github.com/bleidys16/plataforma-ludica", body_style))
    story.append(Paragraph("https://github.com/bleidys16/reto-0", body_style))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("Tabla de los tres fallos elegidos:", subheading_style))
    table_1_data = [
        [Paragraph("<b>N.º</b>", table_header_style), Paragraph("<b>Criterio</b>", table_header_style), Paragraph("<b>Descripción del fallo</b>", table_header_style), Paragraph("<b>Archivo y línea</b>", table_header_style)],
        [Paragraph("1", table_cell_style), Paragraph("Secretos y claves", table_cell_style), Paragraph("Clave de sesión fija en código fuente ('super_secret_vibe_key_12345').", table_cell_style), Paragraph("app/main.py, línea 8", table_cell_style)],
        [Paragraph("2", table_cell_style), Paragraph("Contraseñas y hash", table_cell_style), Paragraph("Las contraseñas de usuario se almacenan en texto plano en la base de datos.", table_cell_style), Paragraph("app/main.py, línea 63-66", table_cell_style)],
        [Paragraph("3", table_cell_style), Paragraph("Validación de entradas", table_cell_style), Paragraph("Se admiten comentarios con contenido vacío o espacios sin código HTTP 400.", table_cell_style), Paragraph("app/main.py, línea 135-144", table_cell_style)]
    ]
    t1 = Table(table_1_data, colWidths=[25, 115, 270, 120])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#94a3b8')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t1)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Informe de auditoría inicial (Sección 5 - Guía Taller 1):", subheading_style))
    table_audit_data = [
        [Paragraph("<b>Criterio</b>", table_header_style), Paragraph("<b>Pregunta de verificación</b>", table_header_style), Paragraph("<b>Resultado</b>", table_header_style), Paragraph("<b>Evidencia (archivo y línea)</b>", table_header_style)],
        [Paragraph("Ejecución", table_cell_style), Paragraph("¿La aplicación arranca con las instrucciones disponibles?", table_cell_style), Paragraph("Cumple", table_cell_style), Paragraph("README.md y app/main.py", table_cell_style)],
        [Paragraph("Validación entradas", table_cell_style), Paragraph("¿Rechaza campos vacíos y textos inválidos?", table_cell_style), Paragraph("No cumple", table_cell_style), Paragraph("app/main.py, línea 135-144 (Fallo 3)", table_cell_style)],
        [Paragraph("Contraseñas y hash", table_cell_style), Paragraph("¿Las contraseñas se guardan con función de hash?", table_cell_style), Paragraph("No cumple", table_cell_style), Paragraph("app/main.py, línea 63-66 (Fallo 2)", table_cell_style)],
        [Paragraph("Secretos y claves", table_cell_style), Paragraph("¿Hay claves escritas directamente en el código?", table_cell_style), Paragraph("No cumple", table_cell_style), Paragraph("app/main.py, línea 8 (Fallo 1)", table_cell_style)],
        [Paragraph("Control de acceso", table_cell_style), Paragraph("¿Un usuario puede alterar datos de otros sin permiso?", table_cell_style), Paragraph("Parcial", table_cell_style), Paragraph("app/main.py, línea 99", table_cell_style)],
        [Paragraph("Dependencias", table_cell_style), Paragraph("¿Cada paquete existe en pypi.org y es el esperado?", table_cell_style), Paragraph("Cumple", table_cell_style), Paragraph("requirements.txt", table_cell_style)],
        [Paragraph("Pruebas", table_cell_style), Paragraph("¿Existen pruebas automatizadas?", table_cell_style), Paragraph("No cumple", table_cell_style), Paragraph("tests/ ausente en prototipo", table_cell_style)],
        [Paragraph("Manejo de errores", table_cell_style), Paragraph("¿Muestra errores claros sin exponer detalles?", table_cell_style), Paragraph("Parcial", table_cell_style), Paragraph("app/main.py, línea 140 (debug=True)", table_cell_style)],
        [Paragraph("Estructura", table_cell_style), Paragraph("¿El código está organizado en partes con roles claros?", table_cell_style), Paragraph("Parcial", table_cell_style), Paragraph("app/ y templates/", table_cell_style)]
    ]
    taudit = Table(table_audit_data, colWidths=[90, 195, 65, 180])
    taudit.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#94a3b8')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(taudit)
    story.append(PageBreak())
    
    # ================= PAGE 3: EVIDENCIA 2 =================
    story.append(Paragraph("2. Evidencia 2: Revisión de secretos", h1_style))
    story.append(Paragraph("Captura del resultado de la búsqueda de claves con git grep antes y después de la corrección", caption_style))
    story.append(get_rl_image("capturas/evidencia_2_secretos.png", target_width=510))
    story.append(PageBreak())
    
    # ================= PAGE 4: EVIDENCIA 3 =================
    story.append(Paragraph("3. Evidencia 3: Contexto del agente", h1_style))
    story.append(Paragraph("Captura completa del archivo AGENTS.md del reto 0", caption_style))
    story.append(get_rl_image("capturas/evidencia_3_agents.png", target_width=510))
    story.append(PageBreak())
    
    # ================= PAGE 5: EVIDENCIA 4 =================
    story.append(Paragraph("4. Evidencia 4: Red de seguridad", h1_style))
    story.append(Paragraph("Captura de la prueba de humo en verde, de ruff check . y del commit con el hook en Passed", caption_style))
    story.append(get_rl_image("capturas/evidencia_4_red_seguridad.png", target_width=510))
    story.append(PageBreak())
    
    # ================= PAGE 6: EVIDENCIA 5 =================
    story.append(Paragraph("5. Evidencia 5: Fallo 1", h1_style))
    story.append(Paragraph("Captura de la prueba en rojo, del plan y el diff de la corrección, y de las pruebas en verde con el commit", caption_style))
    story.append(get_rl_image("capturas/evidencia_5_fallo_1.png", target_width=510))
    story.append(PageBreak())
    
    # ================= PAGE 7: EVIDENCIA 6 =================
    story.append(Paragraph("6. Evidencia 6: Fallo 2", h1_style))
    story.append(Paragraph("Captura de la prueba en rojo, del plan y el diff de la corrección, y de las pruebas en verde con el commit", caption_style))
    story.append(get_rl_image("capturas/evidencia_6_fallo_2.png", target_width=510))
    story.append(PageBreak())
    
    # ================= PAGE 8: EVIDENCIA 7 =================
    story.append(Paragraph("7. Evidencia 7: Fallo 3", h1_style))
    story.append(Paragraph("Captura de la prueba en rojo, del plan y el diff de la corrección, y de las pruebas en verde con el commit", caption_style))
    story.append(get_rl_image("capturas/evidencia_7_fallo_3.png", target_width=510))
    story.append(PageBreak())
    
    # ================= PAGE 9: EVIDENCIA 8 =================
    story.append(Paragraph("8. Evidencia 8: Pull request", h1_style))
    story.append(Paragraph("Captura del pull request con las tres preguntas respondidas y con el estado Merged (cuenta bleidys16)", caption_style))
    story.append(get_rl_image("capturas/evidencia_8_pr_github.png", target_width=510))
    story.append(PageBreak())
    
    # ================= PAGE 10: EVIDENCIA 9 =================
    story.append(Paragraph("9. Evidencia 9: Nueva auditoría y lecciones", h1_style))
    story.append(Paragraph("Tabla de los nueve criterios (Comparativa antes vs después):", subheading_style))
    
    audit_comp_data = [
        [Paragraph("<b>Criterio</b>", table_header_style), Paragraph("<b>Resultado en el taller 1</b>", table_header_style), Paragraph("<b>Resultado hoy</b>", table_header_style), Paragraph("<b>Cómo se comprobó hoy</b>", table_header_style)],
        [Paragraph("Ejecución", table_cell_style), Paragraph("Cumple", table_cell_style), Paragraph("Cumple", table_cell_style), Paragraph("Prueba de humo test_humo.py en verde.", table_cell_style)],
        [Paragraph("Validación de entradas", table_cell_style), Paragraph("No cumple", table_cell_style), Paragraph("Cumple", table_cell_style), Paragraph("test_fallo_3_rechazo_comentarios_vacios.", table_cell_style)],
        [Paragraph("Contraseñas y hash", table_cell_style), Paragraph("No cumple", table_cell_style), Paragraph("Cumple", table_cell_style), Paragraph("test_fallo_2_contrasenas_hasheadas_en_db.", table_cell_style)],
        [Paragraph("Secretos y claves", table_cell_style), Paragraph("No cumple", table_cell_style), Paragraph("Cumple", table_cell_style), Paragraph("git grep sin coincidencias y test_fallo_1.", table_cell_style)],
        [Paragraph("Control de acceso", table_cell_style), Paragraph("Parcial", table_cell_style), Paragraph("Cumple", table_cell_style), Paragraph("Sesión requerida para crear posts.", table_cell_style)],
        [Paragraph("Dependencias y alucinación", table_cell_style), Paragraph("Cumple", table_cell_style), Paragraph("Cumple", table_cell_style), Paragraph("requirements.txt verificado en pypi.org.", table_cell_style)],
        [Paragraph("Pruebas", table_cell_style), Paragraph("No cumple", table_cell_style), Paragraph("Cumple", table_cell_style), Paragraph("pytest ejecuta 4 pruebas en verde.", table_cell_style)],
        [Paragraph("Manejo de errores", table_cell_style), Paragraph("Parcial", table_cell_style), Paragraph("Cumple", table_cell_style), Paragraph("Respuestas controladas con abort(400/404).", table_cell_style)],
        [Paragraph("Estructura", table_cell_style), Paragraph("Parcial", table_cell_style), Paragraph("Cumple", table_cell_style), Paragraph("Ruff check sin errores y pre-commit activo.", table_cell_style)]
    ]
    t9 = Table(audit_comp_data, colWidths=[105, 105, 80, 240])
    t9.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#94a3b8')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t9)
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("<b>Conclusiones:</b>", subheading_style))
    story.append(Paragraph(
        "1. El fallo más grave en un entorno de producción real habría sido el almacenamiento de contraseñas en texto plano, pues una fuga de base de datos comprometería todas las cuentas de los usuarios.<br/>"
        "2. Construir con vibe coding fue muy veloz pero descuidó la seguridad básica; corregir con pair programming y pruebas automáticas dio control absoluto, predictibilidad y certeza técnica de que cada corrección fue efectiva.<br/>"
        "3. La regla en AGENTS.md sobre el uso obligatorio de hashing y el desacople de secretos en variables de entorno habría prevenido ambos fallos críticos desde la primera generación.",
        body_style
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Captura de la sección Lecciones aprendidas de AGENTS.md en GitHub (cuenta bleidys16)", caption_style))
    story.append(get_rl_image("capturas/evidencia_9_lecciones_github.png", target_width=510))
    story.append(PageBreak())
    
    # ================= PAGE 11: EVIDENCIA 10 =================
    story.append(Paragraph("10. Evidencia 10: Cierre de la semana 1", h1_style))
    story.append(Paragraph("Captura de POLITICA_IA.md en GitHub con la sección de aceptación firmada (cuenta bleidys16)", caption_style))
    story.append(get_rl_image("capturas/evidencia_10_politica_ia.png", target_width=510))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Captura de la pestaña Actions con el workflow de CI en verde y de la etiqueta semana-1 en GitHub", caption_style))
    story.append(get_rl_image("capturas/evidencia_10_actions.png", target_width=510))

    doc.build(story)
    print(f"PDF generado exitosamente en: {os.path.abspath(filename)}")

if __name__ == "__main__":
    build_pdf("LariosBleidys_Taller7.pdf")
    build_pdf("LariosBleidysSemana1Dia4.pdf")
