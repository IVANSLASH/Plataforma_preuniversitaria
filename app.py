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

from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from flask_login import LoginManager, login_required, current_user
import json
import os
import re
from datetime import datetime
from pathlib import Path

# Importar modelos y rutas de autenticación
from models import db, Usuario, init_db
from auth import auth

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
app.register_blueprint(auth, url_prefix='/auth')

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
    
    return ejercicios

def cargar_metadatos():
    """Carga los metadatos de ejercicios"""
    try:
        with open('etiquetas/metadata_ejercicios_nuevo.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Agregar compatibilidad con templates existentes
            data['materias'] = data.get('codigos_materia', {})
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
        
        # Fallback a estructura antigua
        materias_antiguas = ['fisica', 'geometria', 'calculo', 'algebra']
        for materia in materias_antiguas:
            ruta_completa = f'static/ejercicios/{materia}/{ruta_imagen}'
            if os.path.exists(ruta_completa):
                return f'/static/ejercicios/{materia}/{ruta_imagen}'
        
        # Si no se encuentra, devolver la ruta original
        return f'/static/ejercicios/{ruta_imagen}'
    
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
    
    # Procesar LaTeX en los ejercicios
    for ejercicio in ejercicios_filtrados:
        ejercicio['enunciado'] = procesar_latex(ejercicio['enunciado'])
        ejercicio['solucion'] = procesar_latex(ejercicio['solucion'])
        # Agregar información amigable de la materia
        ejercicio['info_materia'] = obtener_info_materia(ejercicio.get('codigo_materia', ''))
    
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
    
    return render_template('index.html', 
                         ejercicios=ejercicios,  # Todos los ejercicios para el JavaScript
                         ejercicios_filtrados=ejercicios_filtrados,  # Ejercicios filtrados para mostrar
                         metadatos=metadatos,
                         filtros_datos=filtros_datos,
                         filtros_activos=filtros_activos,
                         filtros=filtros,  # Agregar variable filtros
                         codigos_materias=CODIGOS_MATERIAS,
                         total_ejercicios=len(ejercicios),
                         ejercicios_filtrados_count=len(ejercicios_filtrados))

@app.route('/ejercicio/<ejercicio_id>')
def ejercicio_detalle(ejercicio_id):
    """Página de detalle de un ejercicio específico"""
    ejercicios = cargar_ejercicios()
    ejercicio = next((e for e in ejercicios if e['id'] == ejercicio_id), None)
    
    if not ejercicio:
        return "Ejercicio no encontrado", 404
    
    # Procesar LaTeX en el ejercicio
    ejercicio['enunciado'] = procesar_latex(ejercicio['enunciado'])
    ejercicio['solucion'] = procesar_latex(ejercicio['solucion'])
    ejercicio['info_materia'] = obtener_info_materia(ejercicio.get('codigo_materia', ''))
    
    return render_template('ejercicio_detalle.html', ejercicio=ejercicio)

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

@app.route('/formularios')
def formularios():
    """Página de formularios descargables"""
    formularios_data = cargar_formularios()
    return render_template('formularios.html', formularios=formularios_data)

@app.route('/simulacro')
def simulacro():
    """Página para configurar y generar simulacros"""
    metadatos = cargar_metadatos()
    return render_template('simulacro.html', 
                         metadatos=metadatos,
                         codigos_materias=CODIGOS_MATERIAS)

@app.route('/generar_simulacro', methods=['POST'])
def generar_simulacro():
    """Generar un simulacro con los parámetros especificados"""
    data = request.get_json()
    
    num_preguntas = data.get('num_preguntas', 10)
    niveles = data.get('niveles', [])
    codigos_materia = data.get('codigos_materia', [])
    capitulos = data.get('capitulos', [])
    dificultades = data.get('dificultades', [])
    
    # Validar restricciones
    opciones_validas = [5, 7, 8, 10, 12, 15, 20]
    if num_preguntas not in opciones_validas:
        return jsonify({'error': f'Número de preguntas debe ser uno de: {opciones_validas}'}), 400
    
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
    
    return jsonify({
        'ejercicios': simulacro_ejercicios,
        'total': len(simulacro_ejercicios),
        'configuracion': {
            'num_preguntas': num_preguntas,
            'niveles': niveles,
            'codigos_materia': codigos_materia,
            'capitulos': capitulos,
            'dificultades': dificultades
        }
    })

@app.route('/estadisticas')
def estadisticas():
    """Página de estadísticas avanzadas"""
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
    print("\n🔐 Sistema de autenticación:")
    print("   - /auth/login (Iniciar sesión)")
    print("   - /auth/register (Registrarse)")
    print("   - /auth/google/login (Login con Google)")
    print("   - /auth/google/register (Registro con Google)")
    print("   - /auth/complete_profile (Completar perfil - Google)")
    print("   - /auth/profile (Mi perfil)")
    print("   - /auth/admin/users (Administrar usuarios - solo admin)")
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