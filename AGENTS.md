# Proyecto
Blog con comentarios - Reto 0 y Taller 4 (Aprendiz: Bleidys Paola Larios).
Aplicación web en Python para publicar entradas y gestionar comentarios de usuarios.

## Stack
- Python 3.14+, Flask 3.1+, SQLite3
- Testing & Calidad: Pytest, Ruff, Pre-commit, python-dotenv

## Comandos
- Entorno: `.venv\Scripts\activate`
- Ejecutar: `python app/main.py`
- Tests: `pytest`
- Linter: `ruff check .`
- Pre-commit: `pre-commit run --all-files`

## Estructura
- `app/`: Lógica principal (`main.py`) y plantillas HTML (`templates/`).
- `tests/`: Pruebas de humo (`test_humo.py`) y fallos (`test_fallos.py`).
- `.env.example`: Plantilla de variables de entorno (no versionar `.env`).

## Qué no hacer
- No subir secretos ni contraseñas en código fuente.
- No versionar `.env`, `.venv`, `blog.db` ni archivos `.pyc`.
- No alterar pruebas para forzar aprobación; refactorizar solo el código productivo.
- No desactivar pre-commit ni omitir revisión con Ruff.

## Lecciones aprendidas
- Las variables de entorno son indispensables para desacoplar configuración y secretos.
- Mantener una red de seguridad (humo + ruff) previene regresiones antes de commitear.
