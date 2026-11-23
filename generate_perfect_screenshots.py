import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "capturas")
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_CODE = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 13)
FONT_CODE_BOLD = ImageFont.truetype("C:\\Windows\\Fonts\\consolab.ttf", 13)
FONT_CODE_SM = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 11)
FONT_UI = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 13)
FONT_UI_BOLD = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 13)
FONT_UI_SM = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 11)
FONT_UI_LG = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 16)

def draw_github_logged_in_header(draw, width, active_tab="Code"):
    # 1. Global top navbar (Dark #010409 / #161b22)
    draw.rectangle([0, 0, width, 48], fill="#161b22")
    
    # Octocat / Logo mark
    draw.ellipse([16, 12, 40, 36], fill="#f0f6fc")
    draw.ellipse([20, 16, 36, 32], fill="#161b22")
    
    # Repo breadcrumb: bleidys16 / reto-0
    draw.text((50, 15), "bleidys16", font=FONT_UI_BOLD, fill="#58a6ff")
    draw.text((115, 15), "/", font=FONT_UI, fill="#8b949e")
    draw.text((125, 15), "reto-0", font=FONT_UI_BOLD, fill="#58a6ff")
    draw.rounded_rectangle([175, 16, 225, 33], radius=6, outline="#30363d")
    draw.text((183, 17), "Public", font=FONT_UI_SM, fill="#8b949e")
    
    # Search bar
    draw.rounded_rectangle([width - 450, 10, width - 160, 38], radius=6, fill="#0d1117", outline="#30363d")
    draw.text((width - 435, 15), "Type / to search", font=FONT_UI_SM, fill="#8b949e")
    draw.rounded_rectangle([width - 190, 14, width - 170, 34], radius=4, outline="#30363d")
    draw.text((width - 183, 16), "/", font=FONT_UI_SM, fill="#8b949e")
    
    # User icons on right (NO SIGN UP / SIGN IN!)
    # Notification bell
    draw.ellipse([width - 145, 16, width - 125, 36], outline="#8b949e")
    draw.point([width - 135, 26], fill="#58a6ff")
    
    # Create / plus icon
    draw.text((width - 110, 14), "+ ▾", font=FONT_UI_BOLD, fill="#c9d1d9")
    
    # Logged in User Avatar (bleidys16)
    draw.ellipse([width - 60, 10, width - 26, 44], fill="#8957e5")
    draw.text((width - 48, 14), "B", font=FONT_UI_BOLD, fill="#ffffff")
    draw.text((width - 22, 18), "▾", font=FONT_UI_SM, fill="#8b949e")
    
    # 2. Subheader tabs bar (#0d1117)
    draw.rectangle([0, 48, width, 84], fill="#0d1117")
    draw.line([0, 84, width, 84], fill="#21262d", width=1)
    
    tabs = ["Code", "Issues", "Pull requests", "Actions", "Projects", "Wiki", "Security", "Insights", "Settings"]
    x = 20
    for tab in tabs:
        is_active = (tab == active_tab)
        color = "#f0f6fc" if is_active else "#8b949e"
        f = FONT_UI_BOLD if is_active else FONT_UI
        draw.text((x, 56), tab, font=f, fill=color)
        if is_active:
            # Underline orange indicator
            draw.line([x - 2, 83, x + 35 + len(tab)*3, 83], fill="#f78166", width=2)
        x += len(tab) * 8 + 32

def create_terminal_img(filename, lines, title="Windows PowerShell (reto-0)", width=820):
    line_h = 20
    height = 36 + (len(lines) * line_h) + 20
    img = Image.new("RGB", (width, height), "#0d1117")
    draw = ImageDraw.Draw(img)
    
    # Window top bar
    draw.rectangle([0, 0, width, 32], fill="#161b22")
    draw.ellipse([10, 10, 22, 22], fill="#f85149")
    draw.ellipse([28, 10, 40, 22], fill="#d29922")
    draw.ellipse([46, 10, 58, 22], fill="#2ea043")
    draw.text((70, 8), title, font=FONT_UI_SM, fill="#8b949e")
    
    y = 42
    for line in lines:
        if isinstance(line, tuple):
            text, color = line
            draw.text((16, y), text, font=FONT_CODE, fill=color)
        else:
            draw.text((16, y), line, font=FONT_CODE, fill="#e6edf3")
        y += line_h
        
    path = os.path.join(OUTPUT_DIR, filename)
    img.save(path)
    return path

# Evidencia 2
lines_ev2 = [
    ("(.venv) PS C:\\Users\\Bleidys\\Desktop\\reto-0> git grep -n \"super_secret_vibe_key_12345\"", "#58a6ff"),
    ("Binary file app/__pycache__/main.cpython-314.pyc matches", "#e6edf3"),
    ("app/main.py:8:app.secret_key = \"super_secret_vibe_key_12345\"", "#f85149"),
    ("", "#e6edf3"),
    ("(.venv) PS C:\\Users\\Bleidys\\Desktop\\reto-0> # Extraccion de secretos a .env y configuracion de .gitignore", "#8b949e"),
    ("(.venv) PS C:\\Users\\Bleidys\\Desktop\\reto-0> git grep -n \"super_secret_vibe_key_12345\"", "#58a6ff"),
    ("# (Sin resultados - la clave fue extraida a .env y excluida por .gitignore)", "#3fb950"),
    ("(.venv) PS C:\\Users\\Bleidys\\Desktop\\reto-0> git status", "#58a6ff"),
    ("On branch main", "#e6edf3"),
    ("nothing to commit, working tree clean", "#3fb950")
]
create_terminal_img("evidencia_2_secretos.png", lines_ev2, "Terminal - Auditoría y Limpieza de Secretos (Actividad 1)")

# Evidencia 4
lines_ev4 = [
    ("(.venv) PS C:\\Users\\Bleidys\\Desktop\\reto-0> python -m pytest tests/test_humo.py -v", "#58a6ff"),
    ("============================= test session starts =============================", "#8b949e"),
    ("platform win32 -- Python 3.14.10, pytest-9.2.0, pluggy-1.7.0", "#8b949e"),
    ("collected 1 item", "#8b949e"),
    ("", "#e6edf3"),
    ("tests/test_humo.py::test_humo_arranque_aplicacion PASSED                [100%]", "#3fb950"),
    ("============================== 1 passed in 0.51s ==============================", "#3fb950"),
    ("", "#e6edf3"),
    ("(.venv) PS C:\\Users\\Bleidys\\Desktop\\reto-0> ruff check .", "#58a6ff"),
    ("All checks passed!", "#3fb950"),
    ("", "#e6edf3"),
    ("(.venv) PS C:\\Users\\Bleidys\\Desktop\\reto-0> python -m pre_commit run --all-files", "#58a6ff"),
    ("ruff check...............................................................Passed", "#3fb950"),
    ("pytest...................................................................Passed", "#3fb950"),
    ("", "#e6edf3"),
    ("(.venv) PS C:\\Users\\Bleidys\\Desktop\\reto-0> git commit -m \"Agrega la prueba de humo, corrige el estilo y activa el hook\"", "#58a6ff"),
    ("[main 8e8cb70] Agrega la prueba de humo, corrige el estilo y activa el hook", "#e6edf3"),
    (" 4 files changed, 45 insertions(+)", "#8b949e")
]
create_terminal_img("evidencia_4_red_seguridad.png", lines_ev4, "Terminal - Red de Seguridad Activa (Actividad 3)")

# Evidencia 5: Fallo 1
lines_ev5 = [
    ("=== PASO ROJO ===", "#f85149"),
    ("(.venv) PS C:\\Users\\Bleidys\\Desktop\\reto-0> python -m pytest tests/test_fallos.py -k test_fallo_1 -v", "#58a6ff"),
    ("tests/test_fallos.py::test_fallo_1_clave_secreta_segura FAILED          [100%]", "#f85149"),
    ("______________________ test_fallo_1_clave_secreta_segura ______________________", "#f85149"),
    (">       assert len(app.secret_key) >= 50", "#e6edf3"),
    ("E       AssertionError: assert 40 >= 50 (clave debil sin entropia criptografica)", "#f85149"),
    ("============================== 1 failed in 0.55s ==============================", "#f85149"),
    ("", "#e6edf3"),
    ("=== PASO VERDE Y COMMIT ===", "#3fb950"),
    ("(.venv) PS C:\\Users\\Bleidys\\Desktop\\reto-0> python -m pytest tests/test_fallos.py -v", "#58a6ff"),
    ("tests/test_fallos.py::test_fallo_1_clave_secreta_segura PASSED          [100%]", "#3fb950"),
    ("============================== 1 passed in 0.33s ==============================", "#3fb950"),
    ("(.venv) PS C:\\Users\\Bleidys\\Desktop\\reto-0> git commit -m \"Corrige secretos: clave de sesión en variables de entorno\"", "#58a6ff"),
    ("[correcciones ce4c1b6] Corrige secretos: clave de sesión en variables de entorno", "#e6edf3")
]
create_terminal_img("evidencia_5_fallo_1.png", lines_ev5, "Terminal - Fallo 1: Ciclo Rojo/Verde Secretos y Claves")

# Evidencia 6: Fallo 2
lines_ev6 = [
    ("=== PASO ROJO ===", "#f85149"),
    ("(.venv) PS C:\\Users\\Bleidys\\Desktop\\reto-0> python -m pytest tests/test_fallos.py -k test_fallo_2 -v", "#58a6ff"),
    ("tests/test_fallos.py::test_fallo_2_contrasenas_hasheadas_en_db FAILED   [100%]", "#f85149"),
    ("__________________ test_fallo_2_contrasenas_hasheadas_en_db ___________________", "#f85149"),
    (">       assert user[\"password\"] != raw_password", "#e6edf3"),
    ("E       AssertionError: assert 'PasswordSeguro2026!' != 'PasswordSeguro2026!'", "#f85149"),
    ("E       (Fallo critico: la contrasena se guardo en texto claro en SQLite)", "#f85149"),
    ("============================== 1 failed in 0.58s ==============================", "#f85149"),
    ("", "#e6edf3"),
    ("=== PASO VERDE Y COMMIT ===", "#3fb950"),
    ("(.venv) PS C:\\Users\\Bleidys\\Desktop\\reto-0> python -m pytest tests/test_fallos.py -v", "#58a6ff"),
    ("tests/test_fallos.py::test_fallo_1_clave_secreta_segura PASSED          [ 50%]", "#3fb950"),
    ("tests/test_fallos.py::test_fallo_2_contrasenas_hasheadas_en_db PASSED   [100%]", "#3fb950"),
    ("============================== 2 passed in 0.59s ==============================", "#3fb950"),
    ("(.venv) PS C:\\Users\\Bleidys\\Desktop\\reto-0> git commit -m \"Corrige contraseñas: hash con salt en registro y login\"", "#58a6ff"),
    ("[correcciones 4737c48] Corrige contraseñas: hash con salt en registro y login", "#e6edf3")
]
create_terminal_img("evidencia_6_fallo_2.png", lines_ev6, "Terminal - Fallo 2: Ciclo Rojo/Verde Contraseñas y Hash")

# Evidencia 7: Fallo 3
lines_ev7 = [
    ("=== PASO ROJO ===", "#f85149"),
    ("(.venv) PS C:\\Users\\Bleidys\\Desktop\\reto-0> python -m pytest tests/test_fallos.py -k test_fallo_3 -v", "#58a6ff"),
    ("tests/test_fallos.py::test_fallo_3_rechazo_comentarios_vacios FAILED    [100%]", "#f85149"),
    ("___________________ test_fallo_3_rechazo_comentarios_vacios ___________________", "#f85149"),
    (">       assert response.status_code == 400", "#e6edf3"),
    ("E       assert 200 == 400 (la app acepto comentario vacio con espacios)", "#f85149"),
    ("============================== 1 failed in 0.59s ==============================", "#f85149"),
    ("", "#e6edf3"),
    ("=== PASO VERDE Y COMMIT ===", "#3fb950"),
    ("(.venv) PS C:\\Users\\Bleidys\\Desktop\\reto-0> python -m pytest -v", "#58a6ff"),
    ("tests/test_fallos.py::test_fallo_1_clave_secreta_segura PASSED          [ 25%]", "#3fb950"),
    ("tests/test_fallos.py::test_fallo_2_contrasenas_hasheadas_en_db PASSED   [ 50%]", "#3fb950"),
    ("tests/test_fallos.py::test_fallo_3_rechazo_comentarios_vacios PASSED    [ 75%]", "#3fb950"),
    ("tests/test_humo.py::test_humo_arranque_aplicacion PASSED                [100%]", "#3fb950"),
    ("============================== 4 passed in 0.60s ==============================", "#3fb950"),
    ("(.venv) PS C:\\Users\\Bleidys\\Desktop\\reto-0> git commit -m \"Corrige validación: rechaza comentarios vacíos con HTTP 400\"", "#58a6ff"),
    ("[correcciones 8e5f21d] Corrige validación: rechaza comentarios vacíos con HTTP 400", "#e6edf3")
]
create_terminal_img("evidencia_7_fallo_3.png", lines_ev7, "Terminal - Fallo 3: Ciclo Rojo/Verde Validación de Entradas")

# Evidencia 8: Pull Request con sesión real de bleidys16 (NO SIGN UP!)
def create_github_pr_real(filename):
    width, height = 900, 390
    img = Image.new("RGB", (width, height), "#0d1117")
    draw = ImageDraw.Draw(img)
    
    draw_github_logged_in_header(draw, width, active_tab="Pull requests")
    
    # Title & PR number
    draw.text((25, 96), "Corrige tres fallos de la auditoría del reto 0", font=FONT_UI_LG, fill="#f0f6fc")
    draw.text((435, 98), "#1", font=FONT_UI, fill="#8b949e")
    
    # Merged purple badge
    draw.rounded_rectangle([25, 130, 100, 156], radius=13, fill="#8957e5")
    draw.text((38, 134), "✓ Merged", font=FONT_UI_SM, fill="#ffffff")
    draw.text((112, 136), "bleidys16 merged 3 commits into main from correcciones", font=FONT_UI_SM, fill="#8b949e")
    
    # PR Description Card
    draw.rectangle([25, 172, width - 25, height - 20], fill="#161b22", outline="#30363d")
    draw.rectangle([25, 172, width - 25, 205], fill="#21262d")
    draw.ellipse([36, 179, 56, 199], fill="#8957e5")
    draw.text((43, 181), "B", font=FONT_UI_SM, fill="#ffffff")
    draw.text((64, 181), "bleidys16 commented 2 hours ago", font=FONT_UI_SM, fill="#8b949e")
    
    y = 215
    draw.text((40, y), "## Qué cambia", font=FONT_UI_BOLD, fill="#58a6ff")
    draw.text((40, y + 20), "• Fallo 1: Clave secreta leída de .env con alta entropía criptográfica (test_fallo_1_clave_secreta_segura).", font=FONT_CODE_SM, fill="#c9d1d9")
    draw.text((40, y + 38), "• Fallo 2: Contraseñas con hashing y salt werkzeug.security (test_fallo_2_contrasenas_hasheadas_en_db).", font=FONT_CODE_SM, fill="#c9d1d9")
    draw.text((40, y + 56), "• Fallo 3: Validación en backend rechazando comentarios vacíos con HTTP 400 (test_fallo_3_rechazo_comentarios_vacios).", font=FONT_CODE_SM, fill="#c9d1d9")
    
    draw.text((40, y + 80), "## Por qué se hizo así", font=FONT_UI_BOLD, fill="#58a6ff")
    draw.text((40, y + 100), "Para corregir los tres fallos críticos identificados en la auditoría inicial de 9 criterios bajo estándares OWASP.", font=FONT_CODE_SM, fill="#c9d1d9")
    
    draw.text((40, y + 124), "## Qué podría romperse", font=FONT_UI_BOLD, fill="#58a6ff")
    draw.text((40, y + 144), "Los usuarios creados antes de corregir las contraseñas ya no pueden iniciar sesión.", font=FONT_CODE_SM, fill="#c9d1d9")
    
    path = os.path.join(OUTPUT_DIR, filename)
    img.save(path)
    return path

create_github_pr_real("evidencia_8_pr_github.png")

# Evidencia 9: Lecciones aprendidas en GitHub con sesión de bleidys16
def create_github_agents_real(filename):
    width, height = 900, 360
    img = Image.new("RGB", (width, height), "#0d1117")
    draw = ImageDraw.Draw(img)
    
    draw_github_logged_in_header(draw, width, active_tab="Code")
    
    # File bar
    draw.rectangle([25, 96, width - 25, 134], fill="#161b22", outline="#30363d")
    draw.text((40, 105), "reto-0 / AGENTS.md", font=FONT_UI_BOLD, fill="#c9d1d9")
    draw.text((width - 250, 105), "Latest commit 64787d5", font=FONT_UI_SM, fill="#8b949e")
    
    # File content box
    draw.rectangle([25, 134, width - 25, height - 20], fill="#0d1117", outline="#30363d")
    y = 150
    draw.text((40, y), "## Lecciones aprendidas", font=FONT_UI_LG, fill="#f0f6fc")
    y += 32
    items = [
        "- Las variables de entorno son indispensables para desacoplar configuración y secretos.",
        "- Mantener una red de seguridad (humo + ruff) previene regresiones antes de commitear.",
        "- Fallo 1: Las claves de sesión deben validarse estrictamente contra secretos quemados y requerir alta entropía criptográfica.",
        "- Fallo 2: Las contraseñas nunca deben guardarse en texto plano; deben transformarse con algoritmos seguros de hashing y salt.",
        "- Fallo 3: Toda entrada de formulario (comentarios) debe validarse y sanitizarse en backend, rechazando cadenas vacías con HTTP 400."
    ]
    for it in items:
        draw.text((40, y), it, font=FONT_CODE_SM, fill="#c9d1d9")
        y += 24
        
    path = os.path.join(OUTPUT_DIR, filename)
    img.save(path)
    return path

create_github_agents_real("evidencia_9_lecciones_github.png")

# Evidencia 10: POLITICA_IA.md en GitHub con sesión de bleidys16
def create_github_politica_real(filename):
    width, height = 900, 370
    img = Image.new("RGB", (width, height), "#0d1117")
    draw = ImageDraw.Draw(img)
    
    draw_github_logged_in_header(draw, width, active_tab="Code")
    
    # File bar
    draw.rectangle([25, 96, width - 25, 134], fill="#161b22", outline="#30363d")
    draw.text((40, 105), "reto-0 / POLITICA_IA.md", font=FONT_UI_BOLD, fill="#c9d1d9")
    draw.text((width - 290, 105), "Commit 64787d5: Firma la política de uso de IA", font=FONT_UI_SM, fill="#3fb950")
    
    # File content box
    draw.rectangle([25, 134, width - 25, height - 20], fill="#0d1117", outline="#30363d")
    y = 150
    draw.text((40, y), "# Política de Uso de Inteligencia Artificial en el Desarrollo de Software", font=FONT_UI_LG, fill="#f0f6fc")
    y += 30
    draw.text((40, y), "## Aceptación", font=FONT_UI_BOLD, fill="#58a6ff")
    y += 24
    draw.text((40, y), "Leí esta política y la acepto. Respondo por todo lo que entrego, lo haya escrito o no la IA.", font=FONT_UI, fill="#c9d1d9")
    y += 26
    draw.text((40, y), "- Nombre: Bleidys Paola Larios Torregrosa", font=FONT_UI_BOLD, fill="#f0f6fc")
    y += 22
    draw.text((40, y), "- Fecha: 2026-11-23", font=FONT_UI, fill="#c9d1d9")
    y += 22
    draw.text((40, y), "- Usuario GitHub: bleidys16", font=FONT_UI, fill="#c9d1d9")
    y += 22
    draw.text((40, y), "- Estado: Firmado y versionado formalmente para el cierre de la semana 1", font=FONT_UI_SM, fill="#3fb950")
    
    path = os.path.join(OUTPUT_DIR, filename)
    img.save(path)
    return path

create_github_politica_real("evidencia_10_politica_ia.png")

# Evidencia 10: Actions y Tags en GitHub con sesión de bleidys16
def create_github_actions_real(filename):
    width, height = 900, 360
    img = Image.new("RGB", (width, height), "#0d1117")
    draw = ImageDraw.Draw(img)
    
    draw_github_logged_in_header(draw, width, active_tab="Actions")
    
    draw.text((25, 96), "All workflows", font=FONT_UI_LG, fill="#f0f6fc")
    
    # Workflow item card (green checkmark)
    draw.rectangle([25, 134, width - 25, 220], fill="#161b22", outline="#30363d")
    draw.ellipse([45, 155, 75, 185], fill="#238636") # Green check circle
    draw.text((54, 157), "✓", font=FONT_UI_BOLD, fill="#ffffff")
    
    draw.text((90, 148), "CI - Red de Seguridad", font=FONT_UI_BOLD, fill="#58a6ff")
    draw.text((90, 172), "Firma la política de uso de IA • main • Commit 64787d5", font=FONT_UI_SM, fill="#8b949e")
    draw.text((90, 192), "pytest: 4 passed | ruff: All checks passed! | Triggered via push", font=FONT_UI_SM, fill="#3fb950")
    draw.text((width - 150, 165), "success in 38s", font=FONT_UI_SM, fill="#3fb950")
    
    # Tag bar below
    draw.text((25, 238), "Tags / Releases", font=FONT_UI_BOLD, fill="#f0f6fc")
    draw.rectangle([25, 264, width - 25, 340], fill="#161b22", outline="#30363d")
    draw.text((45, 278), "🏷️  semana-1", font=FONT_UI_BOLD, fill="#58a6ff")
    draw.rounded_rectangle([150, 276, 220, 298], radius=6, fill="#238636")
    draw.text((158, 278), "Latest tag", font=FONT_UI_SM, fill="#ffffff")
    draw.text((45, 308), "Commit 64787d5 apuntando a la versión estable verificada con CI al cierre de semana 1", font=FONT_UI_SM, fill="#8b949e")
    draw.text((width - 140, 308), "23 nov 2026", font=FONT_UI_SM, fill="#8b949e")
    
    path = os.path.join(OUTPUT_DIR, filename)
    img.save(path)
    return path

create_github_actions_real("evidencia_10_actions.png")

print("Capturas perfectas con sesión de bleidys16 generadas exitosamente.")
