#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación Web - Plataforma Preuniversitaria (NUEVA ESTRUCTURA)
==============================================================

Aplicación Flask que maneja la nueva estructura jerárquica de ejercicios
con materias principales, capítulos y metadatos expandidos.

Nueva estructura soportada:
- ejercicios_nuevo/materia_principal/capitulo/*.tex
- Códigos de 4 caracteres (MATU, FISU, QUIM, etc.)
- Metadatos expandidos (dificultad, tiempo_estimado, tags, etc.)
- Sistema de visibilidad flexible
- Sistema de autenticación completo

Autor: Plataforma Preuniversitaria
Fecha: 2024 - Versión Nueva Estructura
"""
# python -m pip install -r requirements.txt

from flask import Flask, render_template, jsonify, request, flash, redirect, url_for, send_file
from flask_login import LoginManager, login_required, current_user
import json
import os
import re
from datetime import datetime, date
from pathlib import Path
from io import BytesIO

# Importar modelos y rutas de autenticación
from models import db, Usuario, init_db, VisitaPagina
from auth import auth_bp, init_oauth

app = Flask(__name__)

# Configuración de la aplicación
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plataforma.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de sesiones
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui_cambiala_en_produccion'

# Inicializar extensiones
db.init_app(app)
init_oauth(app)  # Inicializar OAuth

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Registrar blueprints
app.register_blueprint(auth_bp)

# Mapeo de códigos de materia a nombres amigables
CODIGOS_MATERIAS = {
    'MATU': {'nombre': 'Matemáticas Preuniversitaria', 'color': '#2563eb'},
    'FISU': {'nombre': 'Física Preuniversitaria', 'color': '#dc2626'},
    'QUIM': {'nombre': 'Química Preuniversitaria', 'color': '#16a34a'},
    'LENG': {'nombre': 'Lenguaje y Literatura', 'color': '#ea580c'},
    'CAL2': {'nombre': 'Cálculo 2', 'color': '#7c3aed'},
    'ALGN': {'nombre': 'Álgebra Lineal', 'color': '#0891b2'},
    'FIS1': {'nombre': 'Física 1', 'color': '#be123c'},
    'FIS2': {'nombre': 'Física 2', 'color': '#a21caf'},
    'HIST': {'nombre': 'Historia', 'color': '#ca8a04'},
    'EDIF': {'nombre': 'Ecuaciones Diferenciales', 'color': '#059669'}
}

def cargar_ejercicios():
    """Carga todos los ejercicios desde los nuevos archivos JSON"""
    ejercicios = []
    
    # Intentar cargar desde el archivo nuevo primero
    try:
        with open('etiquetas/todos_ejercicios_nuevo.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            ejercicios.extend(data['ejercicios'])
        print(f"✅ Cargados {len(ejercicios)} ejercicios desde estructura nueva")
    except FileNotFoundError:
        print("⚠️  Archivo todos_ejercicios_nuevo.json no encontrado")
        # Fallback al archivo antiguo
        try:
            with open('etiquetas/todos_ejercicios.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                ejercicios.extend(data['ejercicios'])
            print(f"📄 Cargados {len(ejercicios)} ejercicios desde estructura antigua")
        except FileNotFoundError:
            print("❌ No se encontraron archivos de ejercicios")
    
    # Agregar nombre completo de materia a cada ejercicio
    for ejercicio in ejercicios:
        if 'codigo_materia' in ejercicio:
            ejercicio['nombre_materia'] = obtener_nombre_materia(ejercicio['codigo_materia'])
    
    return ejercicios

def cargar_metadatos():
    """Carga los metadatos de ejercicios"""
    try:
        with open('etiquetas/metadata_ejercicios_nuevo.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Agregar compatibilidad con templates existentes
            data['materias'] = data.get('codigos_materia', {})
            # Agregar nombres completos de materias para los filtros
            data['materias_nombres'] = {}
            for codigo, count in data.get('codigos_materia', {}).items():
                data['materias_nombres'][codigo] = obtener_nombre_materia(codigo)
            # Agregar campos faltantes para estadísticas
            data['visibles_web'] = data.get('total_ejercicios', 0)  # Por defecto todos visibles
            data['no_visibles_web'] = 0
            return data
    except FileNotFoundError:
        # Fallback al archivo antiguo
        try:
            with open('etiquetas/metadata_ejercicios.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Agregar compatibilidad con templates existentes
                data['materias'] = data.get('codigos_materia', {})
                # Agregar nombres completos de materias para los filtros
                data['materias_nombres'] = {}
                for codigo, count in data.get('codigos_materia', {}).items():
                    data['materias_nombres'][codigo] = obtener_nombre_materia(codigo)
                # Agregar campos faltantes para estadísticas
                data['visibles_web'] = data.get('total_ejercicios', 0)
                data['no_visibles_web'] = 0
                return data
        except FileNotFoundError:
            return {
                "total_ejercicios": 0, 
                "materias_principales": {}, 
                "capitulos": {}, 
                "niveles": {},
                "dificultades": {},
                "codigos_materia": {},
                "materias": {},  # Para compatibilidad con templates
                "materias_nombres": {},  # Nombres completos de materias
                "visibles_web": 0,
                "no_visibles_web": 0
            }

def cargar_teoria():
    """Carga la teoría de los capítulos"""
    try:
        with open('etiquetas/teoria_capitulos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"capitulos": {}}

def cargar_formularios():
    """Carga la información de formularios"""
    try:
        with open('etiquetas/formularios.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"formularios": {}, "formularios_generales": {}}

def procesar_latex(texto):
    """Procesa el texto LaTeX para que sea compatible con MathJax y HTML"""
    if not texto:
        return texto
    
    # Función auxiliar para encontrar la ruta correcta de la imagen
    def encontrar_ruta_imagen(ruta_imagen):
        # Buscar en la nueva estructura
        materias_principales = [
            'matematicas_preuniversitaria',
            'fisica_preuniversitaria', 
            'quimica_preuniversitaria',
            'lenguaje_literatura'
        ]
        
        for materia in materias_principales:
            # Buscar en todos los capítulos de la materia
            materia_path = Path(f'ejercicios_nuevo/{materia}')
            if materia_path.exists():
                for capitulo_dir in materia_path.iterdir():
                    if capitulo_dir.is_dir():
                        ruta_completa = capitulo_dir / 'imagenes' / ruta_imagen
                        if ruta_completa.exists():
                            return f'/static/ejercicios_nuevo/{materia}/{capitulo_dir.name}/imagenes/{ruta_imagen}'
        
        # Si no se encuentra en la nueva estructura, devolver ruta por defecto
        return f'/static/ejercicios_nuevo/{ruta_imagen}'
    
    # Eliminar líneas de comentarios de LaTeX (que empiezan con %)
    lineas = texto.split('\n')
    lineas_filtradas = []
    for linea in lineas:
        linea_limpia = linea.strip()
        if linea_limpia and not linea_limpia.startswith('%'):
            lineas_filtradas.append(linea)
    texto = '\n'.join(lineas_filtradas)
    
    # Procesar entornos figure
    figure_pattern = r'\\begin\{figure\}\[([^\]]*)\](.*?)\\end\{figure\}'
    
    def procesar_figure(match):
        opciones = match.group(1)
        contenido = match.group(2).strip()
        
        # Extraer la imagen y el caption
        imagen_match = re.search(r'\\includegraphics\[([^\]]*)\]\{([^}]+)\}', contenido)
        caption_match = re.search(r'\\caption\{([^}]+)\}', contenido)
        
        if imagen_match:
            opciones_img = imagen_match.group(1)
            ruta_imagen = imagen_match.group(2)
            
            # Convertir ruta de imagen para web
            ruta_web = encontrar_ruta_imagen(ruta_imagen)
            
            # Construir HTML para la imagen
            html_img = f'<img src="{ruta_web}" alt="Diagrama" class="img-fluid rounded shadow-sm" style="max-width: 100%; height: auto;">'
            
            # Agregar caption si existe
            caption_html = ""
            if caption_match:
                caption_text = caption_match.group(1)
                caption_html = f'<figcaption class="text-center mt-2 text-muted"><small><em>{caption_text}</em></small></figcaption>'
            
            # Construir figure HTML completo
            figure_html = f'<figure class="text-center my-4">{html_img}{caption_html}</figure>'
            
            return figure_html
        
        return match.group(0)
    
    # Aplicar procesamiento de figure
    texto = re.sub(figure_pattern, procesar_figure, texto, flags=re.DOTALL)
    
    # Reemplazar \n con <br> para saltos de línea
    texto = texto.replace('\n', '<br>')
    
    # Convertir comandos LaTeX de formato a HTML
    texto = re.sub(r'\\textbf\{([^}]+)\}', r'<strong>\1</strong>', texto)
    texto = re.sub(r'\\textit\{([^}]+)\}', r'<em>\1</em>', texto)
    texto = re.sub(r'\\underline\{([^}]+)\}', r'<u>\1</u>', texto)
    texto = re.sub(r'\\text\{([^}]+)\}', r'\1', texto)
    
    # Convertir listas numeradas con formato
    texto = re.sub(r'(\d+\))\s*\\textbf\{([^}]+)\}', r'\1 <strong>\2</strong>', texto)
    
    # Convertir listas con itemize y enumerate
    texto = re.sub(r'\\begin\{itemize\}(.*?)\\end\{itemize\}', r'<ul>\1</ul>', texto, flags=re.DOTALL)
    texto = re.sub(r'\\begin\{enumerate\}(.*?)\\end\{enumerate\}', r'<ol>\1</ol>', texto, flags=re.DOTALL)
    texto = re.sub(r'\\item\s*', r'<li>', texto)
    # Cerrar las listas de manera más simple
    texto = re.sub(r'</ul>\s*<ul>', r'', texto)
    texto = re.sub(r'</ol>\s*<ol>', r'', texto)
    
    # Convertir respuestas y notas
    texto = re.sub(r'\\textbf\{Respuesta:\}\s*([^<]+)', r'<div class="alert alert-success mt-3"><strong>Respuesta:</strong> \1</div>', texto)
    texto = re.sub(r'\\textbf\{Nota:\}\s*([^<]+)', r'<div class="alert alert-info mt-2"><strong>Nota:</strong> \1</div>', texto)
    
    # Convertir símbolos matemáticos comunes
    texto = re.sub(r'\\cdot', r'·', texto)
    texto = re.sub(r'\\div', r'÷', texto)
    texto = re.sub(r'\\to', r'→', texto)
    texto = re.sub(r'\\infty', r'∞', texto)
    
    # Asegurar que las fórmulas estén bien formateadas
    texto = re.sub(r'\$([^$]+)\$', r'$\1$', texto)
    texto = re.sub(r'\$\$([^$]+)\$\$', r'$$\1$$', texto)
    
    return texto

def obtener_info_materia(codigo_materia):
    """Obtiene información amigable de una materia por su código"""
    return CODIGOS_MATERIAS.get(codigo_materia, {
        'nombre': codigo_materia,
        'color': '#6b7280'
    })

def obtener_nombre_materia(codigo_materia):
    """Obtiene el nombre completo de una materia por su código"""
    info = obtener_info_materia(codigo_materia)
    return info['nombre']

def buscar_ejercicios_por_palabras(ejercicios, palabras_busqueda):
    """
    Busca ejercicios que contengan las palabras clave en cualquier atributo
    
    Args:
        ejercicios: Lista de ejercicios
        palabras_busqueda: String con palabras separadas por espacios
    
    Returns:
        Lista de ejercicios que coinciden con la búsqueda
    """
    if not palabras_busqueda or not palabras_busqueda.strip():
        return ejercicios
    
    # Normalizar y dividir las palabras de búsqueda
    palabras = [palabra.lower().strip() for palabra in palabras_busqueda.split() if palabra.strip()]
    
    if not palabras:
        return ejercicios
    
    ejercicios_coincidentes = []
    
    for ejercicio in ejercicios:
        # Crear un texto combinado de todos los atributos relevantes
        texto_completo = ' '.join([
            str(ejercicio.get('id', '')),
            str(ejercicio.get('codigo_materia', '')),
            str(ejercicio.get('materia_principal', '')),
            str(ejercicio.get('capitulo', '')),
            str(ejercicio.get('nivel', '')),
            str(ejercicio.get('dificultad', '')),
            str(ejercicio.get('visibilidad', '')),
            str(ejercicio.get('procedencia', '')),
            str(ejercicio.get('enunciado', '')),
            str(ejercicio.get('solucion', '')),
            str(ejercicio.get('tags', '')),
            str(ejercicio.get('institucion', '')),
            str(ejercicio.get('año', '')),
            str(ejercicio.get('periodo', '')),
            str(ejercicio.get('tipo_examen', '')),
            # Agregar información de la materia
            str(CODIGOS_MATERIAS.get(ejercicio.get('codigo_materia', ''), {}).get('nombre', ''))
        ]).lower()
        
        # Verificar si todas las palabras están presentes
        todas_palabras_encontradas = all(palabra in texto_completo for palabra in palabras)
        
        if todas_palabras_encontradas:
            ejercicios_coincidentes.append(ejercicio)
    
    return ejercicios_coincidentes

@app.before_request
def registrar_visita():
    try:
        # Solo registrar solicitudes GET normales (no static ni favicon)
        if request.method != 'GET':
            return
        if request.path.startswith('/static') or request.path == '/favicon.ico':
            return
        # Evitar registrar llamadas a APIs internas si no deseas contarlas
        # if request.path.startswith('/api/'): return

        visita = VisitaPagina(
            path=request.path,
            usuario_id=(current_user.id if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated else None),
            ip_address=request.headers.get('X-Forwarded-For', request.remote_addr),
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(visita)
        db.session.commit()
    except Exception:
        db.session.rollback()
        # No bloquear la solicitud por errores de logging
        return

@app.route('/')
def index():
    """Página principal con todos los ejercicios"""
    ejercicios = cargar_ejercicios()
    metadatos = cargar_metadatos()
    
    # Obtener filtros de la URL
    codigo_materia = request.args.get('codigo_materia', '')
    materia_principal = request.args.get('materia_principal', '')
    nivel = request.args.get('nivel', '')
    capitulo = request.args.get('capitulo', '')
    dificultad = request.args.get('dificultad', '')
    visibilidad = request.args.get('visibilidad', '')
    busqueda = request.args.get('busqueda', '')  # Nuevo parámetro de búsqueda

    
    # Aplicar filtros
    ejercicios_filtrados = ejercicios.copy()
    
    # Aplicar filtro de materias favoritas del usuario (si está autenticado y tiene materias favoritas)
    mostrar_todas = request.args.get('mostrar_todas', '0') == '1'
    if current_user.is_authenticated and current_user.materias_favoritas and not mostrar_todas:
        materias_favoritas = current_user.materias_favoritas.split(',')
        materias_favoritas = [m.strip() for m in materias_favoritas if m.strip()]
        if materias_favoritas:
            ejercicios_filtrados = [e for e in ejercicios_filtrados if e.get('codigo_materia') in materias_favoritas]
    
    # Aplicar búsqueda por palabras primero
    if busqueda:
        ejercicios_filtrados = buscar_ejercicios_por_palabras(ejercicios_filtrados, busqueda)
    
    # Aplicar filtros adicionales
    if codigo_materia:
        ejercicios_filtrados = [e for e in ejercicios_filtrados if e.get('codigo_materia') == codigo_materia]
    if materia_principal:
        ejercicios_filtrados = [e for e in ejercicios_filtrados if e.get('materia_principal') == materia_principal]
    if nivel:
        ejercicios_filtrados = [e for e in ejercicios_filtrados if e.get('nivel') == nivel]
    if capitulo:
        ejercicios_filtrados = [e for e in ejercicios_filtrados if e.get('capitulo') == capitulo]
    if dificultad:
        ejercicios_filtrados = [e for e in ejercicios_filtrados if str(e.get('dificultad', '')) == dificultad]
    if visibilidad:
        ejercicios_filtrados = [e for e in ejercicios_filtrados if e.get('visibilidad') == visibilidad]
    

    
    # Aplicar límites diarios de visualización
    ejercicios_mostrables = []
    ejercicios_bloqueados = []
    
    for ejercicio in ejercicios_filtrados:
        # Procesar LaTeX en el ejercicio
        ejercicio['enunciado'] = procesar_latex(ejercicio['enunciado'])
        ejercicio['solucion'] = procesar_latex(ejercicio['solucion'])
        # Agregar información amigable de la materia
        ejercicio['info_materia'] = obtener_info_materia(ejercicio.get('codigo_materia', ''))
        
        # Verificar si el usuario puede ver este ejercicio
        if current_user.is_authenticated:
            # Usuario registrado
            if current_user.can_view_exercise(ejercicio['id']):
                ejercicios_mostrables.append(ejercicio)
            else:
                ejercicio['bloqueado'] = True
                ejercicios_bloqueados.append(ejercicio)
        else:
            # Usuario sin registro - usar sesión para tracking
            from flask import session
            import json
            
            # Inicializar tracking de sesión si no existe
            if 'ejercicios_vistos_hoy' not in session:
                session['ejercicios_vistos_hoy'] = 0
                session['ultima_fecha_conteo'] = datetime.now().date().isoformat()
                session['ejercicios_vistos_ids'] = []
            
            # Verificar si es un nuevo día
            today = datetime.now().date().isoformat()
            if session.get('ultima_fecha_conteo') != today:
                session['ejercicios_vistos_hoy'] = 0
                session['ultima_fecha_conteo'] = today
                session['ejercicios_vistos_ids'] = []
            
            # Verificar límite (5 ejercicios para usuarios sin registro)
            if (session['ejercicios_vistos_hoy'] < 5 or 
                ejercicio['id'] in session.get('ejercicios_vistos_ids', [])):
                ejercicios_mostrables.append(ejercicio)
            else:
                ejercicio['bloqueado'] = True
                ejercicios_bloqueados.append(ejercicio)
    
    # Usar ejercicios mostrables como ejercicios filtrados y ordenar aleatoriamente
    import random
    ejercicios_filtrados = ejercicios_mostrables
    random.shuffle(ejercicios_filtrados)
    
    # Preparar datos para los filtros
    filtros_datos = {
        'codigos_materia': metadatos.get('codigos_materia', {}),
        'materias_principales': metadatos.get('materias_principales', {}),
        'capitulos': metadatos.get('capitulos', {}),
        'niveles': metadatos.get('niveles', {}),
        'dificultades': metadatos.get('dificultades', {}),
        'visibilidades': metadatos.get('visibilidades', {})
    }
    
    filtros_activos = {
        'codigo_materia': codigo_materia,
        'materia_principal': materia_principal,
        'nivel': nivel,
        'capitulo': capitulo,
        'dificultad': dificultad,
        'visibilidad': visibilidad,
        'busqueda': busqueda
    }
    
    # Crear variable filtros para compatibilidad con templates
    filtros = {
        'materia': codigo_materia,  # Usar codigo_materia como materia
        'nivel': nivel,
        'capitulo': capitulo
    }
    
    # Obtener información de límites diarios
    limites_info = {}
    if current_user.is_authenticated:
        limites_info = current_user.get_daily_limit_info()
    else:
        from flask import session
        ejercicios_vistos = session.get('ejercicios_vistos_hoy', 0)
        limite_diario = 5
        limites_info = {
            'limite_diario': limite_diario,
            'ejercicios_vistos': ejercicios_vistos,
            'ejercicios_restantes': max(0, limite_diario - ejercicios_vistos),
            'es_premium': False,
            'tipo_usuario': 'sin_registro'
        }
    
    return render_template('index.html', 
                         ejercicios=ejercicios,  # Todos los ejercicios para el JavaScript
                         ejercicios_filtrados=ejercicios_filtrados,  # Ejercicios filtrados para mostrar
                         ejercicios_bloqueados=ejercicios_bloqueados,  # Ejercicios bloqueados por límite
                         metadatos=metadatos,
                         filtros_datos=filtros_datos,
                         filtros_activos=filtros_activos,
                         filtros=filtros,  # Agregar variable filtros
                         codigos_materias=CODIGOS_MATERIAS,
                         total_ejercicios=len(ejercicios),
                         ejercicios_filtrados_count=len(ejercicios_filtrados),
                         limites_info=limites_info)

@app.route('/ejercicio/<ejercicio_id>')
def ejercicio_detalle(ejercicio_id):
    """Página de detalle de un ejercicio específico"""
    ejercicios = cargar_ejercicios()
    ejercicio = next((e for e in ejercicios if e['id'] == ejercicio_id), None)
    
    if not ejercicio:
        return "Ejercicio no encontrado", 404
    
    # Verificar si el usuario puede ver este ejercicio
    puede_ver = True
    if current_user.is_authenticated:
        if not current_user.can_view_exercise(ejercicio_id):
            puede_ver = False
        else:
            # Marcar como visto
            current_user.mark_exercise_as_viewed(ejercicio_id)
    else:
        # Usuario sin registro
        from flask import session
        import json
        
        # Inicializar tracking de sesión si no existe
        if 'ejercicios_vistos_hoy' not in session:
            session['ejercicios_vistos_hoy'] = 0
            session['ultima_fecha_conteo'] = datetime.now().date().isoformat()
            session['ejercicios_vistos_ids'] = []
        
        # Verificar si es un nuevo día
        today = datetime.now().date().isoformat()
        if session.get('ultima_fecha_conteo') != today:
            session['ejercicios_vistos_hoy'] = 0
            session['ultima_fecha_conteo'] = today
            session['ejercicios_vistos_ids'] = []
        
        # Verificar si ya vio este ejercicio
        if ejercicio_id not in session.get('ejercicios_vistos_ids', []):
            # Verificar límite (5 ejercicios para usuarios sin registro)
            if session['ejercicios_vistos_hoy'] >= 5:
                puede_ver = False
            else:
                # Marcar como visto
                session['ejercicios_vistos_hoy'] += 1
                session['ejercicios_vistos_ids'] = session.get('ejercicios_vistos_ids', []) + [ejercicio_id]
    
    # Procesar LaTeX en el ejercicio
    ejercicio['enunciado'] = procesar_latex(ejercicio['enunciado'])
    ejercicio['solucion'] = procesar_latex(ejercicio['solucion'])
    ejercicio['info_materia'] = obtener_info_materia(ejercicio.get('codigo_materia', ''))
    
    # Obtener información de límites diarios
    limites_info = {}
    if current_user.is_authenticated:
        limites_info = current_user.get_daily_limit_info()
    else:
        ejercicios_vistos = session.get('ejercicios_vistos_hoy', 0)
        limite_diario = 5
        limites_info = {
            'limite_diario': limite_diario,
            'ejercicios_vistos': ejercicios_vistos,
            'ejercicios_restantes': max(0, limite_diario - ejercicios_vistos),
            'es_premium': False,
            'tipo_usuario': 'sin_registro'
        }
    
    return render_template('ejercicio_detalle.html', 
                         ejercicio=ejercicio, 
                         puede_ver=puede_ver,
                         limites_info=limites_info)

@app.route('/api/ejercicios')
def api_ejercicios():
    """API para obtener ejercicios en formato JSON"""
    ejercicios = cargar_ejercicios()
    
    # Aplicar filtros si se proporcionan
    filtros = ['codigo_materia', 'materia_principal', 'nivel', 'capitulo', 'dificultad', 'visibilidad']
    
    for filtro in filtros:
        valor = request.args.get(filtro)
        if valor:
            if filtro == 'dificultad':
                ejercicios = [e for e in ejercicios if str(e.get(filtro, '')) == valor]
            else:
                ejercicios = [e for e in ejercicios if e.get(filtro) == valor]
    
    return jsonify({
        'total': len(ejercicios),
        'ejercicios': ejercicios,
        'filtros_aplicados': {k: request.args.get(k) for k in filtros if request.args.get(k)}
    })

@app.route('/api/metadatos')
def api_metadatos():
    """API para obtener metadatos"""
    metadatos = cargar_metadatos()
    metadatos['codigos_materias_info'] = CODIGOS_MATERIAS
    return jsonify(metadatos)

@app.route('/teoria')
def teoria():
    """Página principal de teoría"""
    teoria_data = cargar_teoria()
    return render_template('teoria.html', teoria=teoria_data)

@app.route('/teoria/<materia>/<capitulo>')
def teoria_capitulo(materia, capitulo):
    """Página de teoría de un capítulo específico"""
    teoria_data = cargar_teoria()
    
    # Verificar si existe el capítulo
    if (materia in teoria_data['capitulos'] and 
        capitulo in teoria_data['capitulos'][materia]):
        
        data = teoria_data['capitulos'][materia][capitulo]
        return render_template('teoria_capitulo.html', 
                             data=data,
                             materia=materia,
                             capitulo=capitulo)
    
    # Si no existe el capítulo, redirigir a la página principal de teoría
    flash('El capítulo solicitado no existe.', 'error')
    return redirect(url_for('teoria'))

@app.route('/formularios')
def formularios():
    """Página de formularios descargables"""
    formularios_data = cargar_formularios()
    return render_template('formularios.html', formularios=formularios_data)

@app.route('/descargar/teoria/<materia>/<capitulo>')
def descargar_teoria(materia, capitulo):
    """Descarga un archivo de teoría específico"""
    teoria_data = cargar_teoria()
    
    # Verificar si existe el capítulo
    if (materia in teoria_data['capitulos'] and 
        capitulo in teoria_data['capitulos'][materia]):
        
        # Construir la ruta del archivo de teoría
        ruta_archivo = os.path.join('static', 'teoria', materia, f'teo_{materia}_{capitulo}.pdf')
        
        # Verificar si el archivo existe
        if os.path.exists(ruta_archivo):
            return send_file(ruta_archivo, as_attachment=True)
    
    # Si no se encuentra el archivo
    flash('El archivo de teoría no se encuentra disponible.', 'error')
    return redirect(url_for('teoria'))

@app.route('/descargar/<materia>/<capitulo>')
def descargar_formulario(materia, capitulo):
    """Descarga un formulario específico"""
    formularios_data = cargar_formularios()
    
    # Verificar si existe el formulario
    if (materia in formularios_data['formularios'] and 
        capitulo in formularios_data['formularios'][materia]):
        
        formulario = formularios_data['formularios'][materia][capitulo]
        archivo = formulario['archivo']
        
        # Construir la ruta completa del archivo
        ruta_archivo = os.path.join('static', archivo)
        
        # Verificar si el archivo existe
        if os.path.exists(ruta_archivo):
            return send_file(ruta_archivo, as_attachment=True)
    
    # Si no se encuentra el formulario
    flash('El formulario solicitado no se encuentra disponible.', 'error')
    return redirect(url_for('formularios'))

@app.route('/descargar/<id>')
def descargar_formulario_completo(id):
    """Descarga un formulario completo"""
    formularios_data = cargar_formularios()
    
    # Verificar si existe el formulario completo
    if id in formularios_data['formularios_generales']:
        formulario = formularios_data['formularios_generales'][id]
        archivo = formulario['archivo']
        
        # Construir la ruta completa del archivo
        ruta_archivo = os.path.join('static', archivo)
        
        # Verificar si el archivo existe
        if os.path.exists(ruta_archivo):
            return send_file(ruta_archivo, as_attachment=True)
        else:
            flash('El archivo del formulario no se encuentra disponible.', 'error')
            return redirect(url_for('formularios'))
    else:
        flash('El formulario solicitado no existe.', 'error')
        return redirect(url_for('formularios'))

@app.route('/simulacro')
def simulacro():
    """Página para configurar y generar simulacros"""
    metadatos = cargar_metadatos()
    
    # Obtener información de límites de simulacros
    simulacro_info = {}
    if current_user.is_authenticated:
        simulacro_info = current_user.get_simulacro_limit_info()
    else:
        simulacro_info = {
            'limite_diario': 0,
            'simulacros_realizados': 0,
            'simulacros_restantes': 0,
            'es_premium': False,
            'puede_hacer': False,
            'mensaje': 'Debes registrarte para realizar simulacros'
        }
    
    return render_template('simulacro.html', 
                         metadatos=metadatos,
                         codigos_materias=CODIGOS_MATERIAS,
                         simulacro_info=simulacro_info)

@app.route('/generar_simulacro', methods=['POST'])
def generar_simulacro():
    """Generar un simulacro con los parámetros especificados"""
    # Verificar límites de simulacros
    if not current_user.is_authenticated:
        return jsonify({'error': 'Debes registrarte para realizar simulacros'}), 403
    
    if not current_user.can_do_simulacro():
        simulacro_info = current_user.get_simulacro_limit_info()
        if simulacro_info['es_premium']:
            return jsonify({'error': 'Error en la verificación premium'}), 403
        else:
            return jsonify({'error': 'Ya has realizado tu simulacro diario. Los usuarios registrados pueden hacer 1 simulacro por día.'}), 403
    
    data = request.get_json()
    
    num_preguntas = data.get('num_preguntas', 10)
    tiempo_examen = data.get('tiempo_examen', 60)
    niveles = data.get('niveles', [])
    codigos_materia = data.get('codigos_materia', [])
    capitulos = data.get('capitulos', [])
    dificultades = data.get('dificultades', [])
    
    # Validar restricciones
    opciones_validas = [5, 7, 8, 10, 12, 15, 20]
    if num_preguntas not in opciones_validas:
        return jsonify({'error': f'Número de preguntas debe ser uno de: {opciones_validas}'}), 400
    
    # Validar tiempo del examen
    tiempos_validos = [30, 60, 90, 120]
    if tiempo_examen not in tiempos_validos:
        return jsonify({'error': f'Tiempo del examen debe ser uno de: {tiempos_validos} minutos'}), 400
    
    # Cargar todos los ejercicios
    ejercicios = cargar_ejercicios()
    
    # Aplicar filtros
    ejercicios_filtrados = ejercicios.copy()
    
    if niveles:
        ejercicios_filtrados = [e for e in ejercicios_filtrados if e.get('nivel') in niveles]
    
    if codigos_materia:
        ejercicios_filtrados = [e for e in ejercicios_filtrados if e.get('codigo_materia') in codigos_materia]
    
    if capitulos:
        ejercicios_filtrados = [e for e in ejercicios_filtrados if e.get('capitulo') in capitulos]
    
    if dificultades:
        ejercicios_filtrados = [e for e in ejercicios_filtrados if str(e.get('dificultad', '')) in dificultades]
    
    # Verificar que hay suficientes ejercicios
    if len(ejercicios_filtrados) < num_preguntas:
        return jsonify({
            'error': f'Solo hay {len(ejercicios_filtrados)} ejercicios disponibles con los filtros seleccionados.'
        }), 400
    
    # Seleccionar ejercicios aleatorios
    import random
    random.shuffle(ejercicios_filtrados)
    simulacro_ejercicios = ejercicios_filtrados[:num_preguntas]
    
    # Procesar LaTeX en los ejercicios
    for ejercicio in simulacro_ejercicios:
        ejercicio['enunciado'] = procesar_latex(ejercicio['enunciado'])
        ejercicio['solucion'] = procesar_latex(ejercicio['solucion'])
        ejercicio['info_materia'] = obtener_info_materia(ejercicio.get('codigo_materia', ''))
    
    # Marcar el simulacro como realizado
    current_user.mark_simulacro_as_done()
    
    return jsonify({
        'ejercicios': simulacro_ejercicios,
        'total': len(simulacro_ejercicios),
        'configuracion': {
            'num_preguntas': num_preguntas,
            'tiempo_examen': tiempo_examen,
            'niveles': niveles,
            'codigos_materia': codigos_materia,
            'capitulos': capitulos,
            'dificultades': dificultades
        }
    })

@app.route('/generar_simulacro_pdf', methods=['POST'])
def generar_simulacro_pdf():
    """Generar un simulacro en formato PDF"""
    # Verificar límites de simulacros
    if not current_user.is_authenticated:
        return jsonify({'error': 'Debes registrarte para realizar simulacros'}), 403
    
    if not current_user.can_do_simulacro():
        simulacro_info = current_user.get_simulacro_limit_info()
        if simulacro_info['es_premium']:
            return jsonify({'error': 'Error en la verificación premium'}), 403
        else:
            return jsonify({'error': 'Ya has realizado tu simulacro diario. Los usuarios registrados pueden hacer 1 simulacro por día.'}), 403
    
    try:
        # Importar reportlab solo cuando sea necesario
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
        
        data = request.get_json()
        
        num_preguntas = data.get('num_preguntas', 10)
        tiempo_examen = data.get('tiempo_examen', 60)
        niveles = data.get('niveles', [])
        codigos_materia = data.get('codigos_materia', [])
        capitulos = data.get('capitulos', [])
        dificultades = data.get('dificultades', [])
        
        # Validar restricciones
        opciones_validas = [5, 7, 8, 10, 12, 15, 20]
        if num_preguntas not in opciones_validas:
            return jsonify({'error': f'Número de preguntas debe ser uno de: {opciones_validas}'}), 400
        
        tiempos_validos = [30, 60, 90, 120]
        if tiempo_examen not in tiempos_validos:
            return jsonify({'error': f'Tiempo del examen debe ser uno de: {tiempos_validos} minutos'}), 400
        
        # Cargar todos los ejercicios
        ejercicios = cargar_ejercicios()
        
        # Aplicar filtros
        ejercicios_filtrados = ejercicios.copy()
        
        if niveles:
            ejercicios_filtrados = [e for e in ejercicios_filtrados if e.get('nivel') in niveles]
        
        if codigos_materia:
            ejercicios_filtrados = [e for e in ejercicios_filtrados if e.get('codigo_materia') in codigos_materia]
        
        if capitulos:
            ejercicios_filtrados = [e for e in ejercicios_filtrados if e.get('capitulo') in capitulos]
        
        if dificultades:
            ejercicios_filtrados = [e for e in ejercicios_filtrados if str(e.get('dificultad', '')) in dificultades]
        
        # Verificar que hay suficientes ejercicios
        if len(ejercicios_filtrados) < num_preguntas:
            return jsonify({
                'error': f'Solo hay {len(ejercicios_filtrados)} ejercicios disponibles con los filtros seleccionados.'
            }), 400
        
        # Seleccionar ejercicios aleatorios
        import random
        random.shuffle(ejercicios_filtrados)
        simulacro_ejercicios = ejercicios_filtrados[:num_preguntas]
        
        # Crear buffer para el PDF
        buffer = BytesIO()
        
        # Crear documento PDF
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=TA_CENTER
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=12
        )
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_JUSTIFY
        )
        question_style = ParagraphStyle(
            'Question',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=8,
            leftIndent=20
        )
        
        # Título del simulacro
        story.append(Paragraph("SIMULACRO DE EXAMEN", title_style))
        story.append(Spacer(1, 20))
        
        # Información del simulacro
        info_text = f"""
        <b>Configuración del Simulacro:</b><br/>
        • Número de preguntas: {num_preguntas}<br/>
        • Tiempo del examen: {tiempo_examen} minutos<br/>
        • Niveles: {', '.join(niveles) if niveles else 'Todos'}<br/>
        • Materias: {', '.join(codigos_materia) if codigos_materia else 'Todas'}<br/>
        • Capítulos: {', '.join(capitulos) if capitulos else 'Todos'}<br/>
        • Dificultades: {', '.join(dificultades) if dificultades else 'Todas'}<br/>
        • Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}
        """
        story.append(Paragraph(info_text, normal_style))
        story.append(Spacer(1, 20))
        
        # Instrucciones
        story.append(Paragraph("INSTRUCCIONES:", heading_style))
        instructions = f"""
        • Tienes {tiempo_examen} minutos para completar este simulacro.<br/>
        • Lee cuidadosamente cada pregunta antes de responder.<br/>
        • Puedes usar calculadora y fórmulas si es necesario.<br/>
        • Marca claramente tus respuestas.<br/>
        • Revisa tus respuestas antes de entregar.
        """
        story.append(Paragraph(instructions, normal_style))
        story.append(Spacer(1, 20))
        
        # Ejercicios
        story.append(Paragraph("EJERCICIOS:", heading_style))
        story.append(Spacer(1, 10))
        
        for i, ejercicio in enumerate(simulacro_ejercicios, 1):
            # Información del ejercicio
            ejercicio_info = f"""
            <b>Pregunta {i}</b> (ID: {ejercicio.get('id', 'N/A')} | 
            Materia: {ejercicio.get('nombre_materia', ejercicio.get('codigo_materia', 'N/A'))} | 
            Nivel: {ejercicio.get('nivel', 'N/A')})
            """
            story.append(Paragraph(ejercicio_info, question_style))
            
            # Enunciado (limpiar HTML y LaTeX)
            enunciado = ejercicio.get('enunciado', 'Sin enunciado')
            # Limpiar tags HTML básicos
            enunciado = re.sub(r'<[^>]+>', '', enunciado)
            # Simplificar LaTeX básico
            enunciado = re.sub(r'\\[a-zA-Z]+', '', enunciado)
            enunciado = re.sub(r'\{[^}]*\}', '', enunciado)
            
            story.append(Paragraph(enunciado, normal_style))
            story.append(Spacer(1, 15))
        
        # Construir PDF
        doc.build(story)
        
        # Obtener contenido del buffer
        buffer.seek(0)
        
        # Marcar el simulacro como realizado
        current_user.mark_simulacro_as_done()
        
        # Generar nombre del archivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'simulacro_{timestamp}.pdf'
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except ImportError:
        return jsonify({'error': 'La biblioteca reportlab no está instalada. Ejecuta: pip install reportlab'}), 500
    except Exception as e:
        return jsonify({'error': f'Error al generar PDF: {str(e)}'}), 500

@app.route('/estadisticas')
@login_required
def estadisticas():
    """Página de estadísticas avanzadas (solo para administradores)"""
    if not current_user.es_admin:
        flash("No tienes permisos para acceder a esta página.", "danger")
        return redirect(url_for('index'))
    
    metadatos = cargar_metadatos()
    ejercicios = cargar_ejercicios()
    
    # Estadísticas adicionales
    estadisticas_detalladas = {
        'total_ejercicios': len(ejercicios),
        'por_codigo_materia': {},
        'por_nivel_y_materia': {},
        'por_dificultad': {},
        'tiempo_promedio_por_materia': {},
        'procedencias': {},
        'visibilidades': {}
    }
    
    # Procesar estadísticas
    for ejercicio in ejercicios:
        codigo = ejercicio.get('codigo_materia', 'SIN_CODIGO')
        nivel = ejercicio.get('nivel', 'sin_nivel')
        dificultad = str(ejercicio.get('dificultad', 'sin_dificultad'))
        procedencia = ejercicio.get('procedencia', 'Sin procedencia')
        visibilidad = ejercicio.get('visibilidad', 'sin_visibilidad')
        tiempo = ejercicio.get('tiempo_estimado', 0)
        
        # Por código de materia
        if codigo not in estadisticas_detalladas['por_codigo_materia']:
            estadisticas_detalladas['por_codigo_materia'][codigo] = 0
        estadisticas_detalladas['por_codigo_materia'][codigo] += 1
        
        # Por nivel y materia
        key_nivel_materia = f"{codigo}_{nivel}"
        if key_nivel_materia not in estadisticas_detalladas['por_nivel_y_materia']:
            estadisticas_detalladas['por_nivel_y_materia'][key_nivel_materia] = 0
        estadisticas_detalladas['por_nivel_y_materia'][key_nivel_materia] += 1
        
        # Por dificultad
        if dificultad not in estadisticas_detalladas['por_dificultad']:
            estadisticas_detalladas['por_dificultad'][dificultad] = 0
        estadisticas_detalladas['por_dificultad'][dificultad] += 1
        
        # Tiempo promedio por materia
        if codigo not in estadisticas_detalladas['tiempo_promedio_por_materia']:
            estadisticas_detalladas['tiempo_promedio_por_materia'][codigo] = []
        if isinstance(tiempo, (int, float)) and tiempo > 0:
            estadisticas_detalladas['tiempo_promedio_por_materia'][codigo].append(tiempo)
        
        # Procedencias
        if procedencia not in estadisticas_detalladas['procedencias']:
            estadisticas_detalladas['procedencias'][procedencia] = 0
        estadisticas_detalladas['procedencias'][procedencia] += 1
        
        # Visibilidades
        if visibilidad not in estadisticas_detalladas['visibilidades']:
            estadisticas_detalladas['visibilidades'][visibilidad] = 0
        estadisticas_detalladas['visibilidades'][visibilidad] += 1
    
    # Calcular promedios de tiempo
    for codigo, tiempos in estadisticas_detalladas['tiempo_promedio_por_materia'].items():
        if tiempos:
            estadisticas_detalladas['tiempo_promedio_por_materia'][codigo] = round(sum(tiempos) / len(tiempos), 1)
        else:
            estadisticas_detalladas['tiempo_promedio_por_materia'][codigo] = 0
    
    return render_template('estadisticas.html',
                         metadatos=metadatos,
                         estadisticas=estadisticas_detalladas,
                         codigos_materias=CODIGOS_MATERIAS,
                         total_ejercicios=len(ejercicios),
                         procedencias=estadisticas_detalladas['procedencias'])

@app.route('/libros')
def libros():
    """Página de libros disponibles"""
    return render_template('libros.html')

@app.route('/anuncios')
def anuncios():
    """Página de anuncios y promociones"""
    return render_template('anuncios.html')

@app.route('/premium')
def premium():
    """Página de suscripción premium"""
    # Obtener información de límites diarios
    limites_info = {}
    if current_user.is_authenticated:
        limites_info = current_user.get_daily_limit_info()
    else:
        from flask import session
        ejercicios_vistos = session.get('ejercicios_vistos_hoy', 0)
        limite_diario = 5
        limites_info = {
            'limite_diario': limite_diario,
            'ejercicios_vistos': ejercicios_vistos,
            'ejercicios_restantes': max(0, limite_diario - ejercicios_vistos),
            'es_premium': False,
            'tipo_usuario': 'sin_registro'
        }
    
    return render_template('premium.html', limites_info=limites_info)

# Rutas adicionales para compatibilidad
@app.route('/api/teoria')
def api_teoria():
    """API para obtener teoría"""
    return jsonify(cargar_teoria())

@app.route('/api/formularios')
def api_formularios():
    """API para obtener formularios"""
    return jsonify(cargar_formularios())

@app.route('/api/buscar')
def api_buscar():
    """API para búsqueda en tiempo real de ejercicios"""
    busqueda = request.args.get('q', '')
    ejercicios = cargar_ejercicios()
    
    if not busqueda:
        return jsonify({'ejercicios': [], 'total': 0})
    
    ejercicios_encontrados = buscar_ejercicios_por_palabras(ejercicios, busqueda)
    
    # Limitar resultados para respuesta rápida
    resultados_limitados = ejercicios_encontrados[:10]
    
    # Preparar datos para JSON (sin procesar LaTeX para velocidad)
    for ejercicio in resultados_limitados:
        ejercicio['info_materia'] = obtener_info_materia(ejercicio.get('codigo_materia', ''))
    
    return jsonify({
        'ejercicios': resultados_limitados,
        'total': len(ejercicios_encontrados),
        'mostrados': len(resultados_limitados),
        'busqueda': busqueda
    })

if __name__ == '__main__':
    print("🚀 Iniciando servidor de ejercicios preuniversitarios (NUEVA ESTRUCTURA)...")
    print("📚 Cargando ejercicios desde nueva estructura jerárquica...")
    
    # Inicializar base de datos
    with app.app_context():
        init_db(app)
    
    ejercicios = cargar_ejercicios()
    metadatos = cargar_metadatos()
    
    print(f"✅ Cargados {len(ejercicios)} ejercicios")
    print(f"🏷️  Códigos de materia disponibles: {list(metadatos.get('codigos_materia', {}).keys())}")
    print(f"📊 Materias principales: {list(metadatos.get('materias_principales', {}).keys())}")
    print(f"📈 Niveles disponibles: {list(metadatos.get('niveles', {}).keys())}")
    print(f"⭐ Dificultades: {list(metadatos.get('dificultades', {}).keys())}")
    
    print("\n🌐 Servidor iniciado en: http://localhost:5000")
    print("📖 Páginas principales:")
    print("   - / (Ejercicios con filtros avanzados)")
    print("   - /ejercicio/<id> (Detalle de ejercicio)")
    print("   - /simulacro (Simulacros personalizados)")
    print("   - /estadisticas (Estadísticas detalladas)")
    print("   - /libros (Libros disponibles)")
    print("\n🔐 Sistema de autenticación (Solo Google OAuth):")
    print("   - /auth/login (Autenticación exclusiva con Google OAuth)")
    print("   - /auth/logout (Cerrar sesión)")
    print("   - /auth/profile (Perfil de usuario)")
    print("   - /auth/admin/users (Panel de administración)")
    print("   \n   📝 NOTA: Solo se permite autenticación mediante Google OAuth.")
    print("           El sistema tradicional de contraseñas ha sido deshabilitado por seguridad.")
    print("\n🔍 Filtros soportados:")
    print("   - ?codigo_materia=MATU (por código de materia)")
    print("   - ?nivel=basico (por nivel)")
    print("   - ?dificultad=2 (por dificultad 1-5)")
    print("   - ?visibilidad=web_impreso (por visibilidad)")
    print("   - ?busqueda=parcial umsa (búsqueda por palabras)")
    print("\n🛠️  APIs disponibles:")
    print("   - /api/ejercicios (JSON con ejercicios)")
    print("   - /api/metadatos (JSON con estadísticas)")
    print("   - /api/buscar?q=parcial (búsqueda en tiempo real)")
    print("   - /generar_simulacro (POST - crear simulacro)")
    
    app.run(debug=True, host='0.0.0.0', port=5000)