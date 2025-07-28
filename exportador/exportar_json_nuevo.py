#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exportador de ejercicios LaTeX a JSON - NUEVA ESTRUCTURA
======================================================

Este script lee todos los archivos .tex de la nueva estructura jerárquica
ejercicios_nuevo/ y los exporta a formato JSON con metadatos expandidos.

Nueva estructura:
ejercicios_nuevo/
├── matematicas_preuniversitaria/
│   ├── algebra/
│   ├── geometria/
│   └── ...
├── fisica_preuniversitaria/
│   ├── cinematica/
│   ├── dinamica/
│   └── ...
└── ...

Autor: Plataforma Preuniversitaria
Fecha: 2024 - Versión Nueva Estructura
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EjercicioExporterNuevo:
    """Clase para exportar ejercicios de la nueva estructura LaTeX a JSON."""
    
    def __init__(self, ejercicios_dir: str = "ejercicios_nuevo", output_dir: str = "etiquetas"):
        self.ejercicios_dir = Path(ejercicios_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Patrón regex para extraer ejercicios
        self.ejercicio_pattern = re.compile(
            r'\\begin\{ejercicio\}\[(.*?)\](.*?)\\end\{ejercicio\}',
            re.DOTALL
        )
        
        # Patrón mejorado para extraer metadatos con comentarios
        self.metadata_pattern = re.compile(
            r'(\w+)=([^,\n%]+(?:{[^}]*})?)',
            re.DOTALL
        )
        
        # Patrón para extraer solución
        self.solucion_pattern = re.compile(
            r'\\begin\{solucion\}(.*?)\\end\{solucion\}',
            re.DOTALL
        )
        
        # Mapeo de códigos de materia a nombres completos
        self.mapeo_materias = {
            'MATU': 'matematicas_preuniversitaria',
            'FISU': 'fisica_preuniversitaria',
            'QUIM': 'quimica_preuniversitaria',
            'LENG': 'lenguaje_literatura',
            'CAL2': 'calculo_2',
            'ALGN': 'algebra_lineal',
            'FIS1': 'fisica_1',
            'FIS2': 'fisica_2',
            'HIST': 'historia',
            'EDIF': 'ecuaciones_diferenciales'
        }
    
    def parse_metadata(self, metadata_str: str) -> Dict[str, Any]:
        """Parsea los metadatos de un ejercicio con nueva estructura."""
        metadata = {}
        
        # Limpiar comentarios de LaTeX
        lines = metadata_str.split('\n')
        clean_lines = []
        for line in lines:
            # Remover comentarios que empiezan con %
            comment_pos = line.find('%')
            if comment_pos != -1:
                line = line[:comment_pos]
            clean_lines.append(line)
        
        clean_metadata = '\n'.join(clean_lines)
        
        # Extraer pares clave=valor
        matches = self.metadata_pattern.findall(clean_metadata)
        
        for key, value in matches:
            # Limpiar el valor
            value = value.strip().strip('"').strip("'").rstrip(',')
            
            # Procesar listas (valores entre llaves)
            if value.startswith('{') and value.endswith('}'):
                inner_value = value[1:-1].strip()
                if inner_value:
                    value = [v.strip() for v in inner_value.split(',')]
                else:
                    value = []
            
            # Convertir tipos
            if isinstance(value, str):
                if value.lower() in ['true', 'false']:
                    value = value.lower() == 'true'
                elif value.isdigit():
                    value = int(value)
                elif value.replace('.', '').isdigit():
                    value = float(value)
            
            metadata[key] = value
        
        return metadata
    
    def extract_ejercicio_content(self, content: str) -> str:
        """Extrae el contenido del ejercicio (sin metadatos ni solución)."""
        # Remover metadatos
        content = re.sub(r'\\begin\{ejercicio\}\[.*?\]', '', content, flags=re.DOTALL)
        content = re.sub(r'\\end\{ejercicio\}', '', content)
        
        # Remover solución
        content = re.sub(r'\\begin\{solucion\}.*?\\end\{solucion\}', '', content, flags=re.DOTALL)
        
        # Remover comentarios de LaTeX
        lines = content.split('\n')
        clean_lines = []
        for line in lines:
            # No remover % que están dentro de fórmulas matemáticas
            if not (line.strip().startswith('%') and '$' not in line):
                clean_lines.append(line)
        
        return '\n'.join(clean_lines).strip()
    
    def extract_solucion(self, content: str) -> str:
        """Extrae la solución del ejercicio."""
        match = self.solucion_pattern.search(content)
        if match:
            solucion = match.group(1).strip()
            # Limpiar comentarios de la solución
            lines = solucion.split('\n')
            clean_lines = []
            for line in lines:
                if not line.strip().startswith('%'):
                    clean_lines.append(line)
            return '\n'.join(clean_lines).strip()
        return ""
    
    def process_tex_file(self, file_path: Path, materia_principal: str, capitulo: str) -> List[Dict[str, Any]]:
        """Procesa un archivo .tex y extrae todos los ejercicios."""
        ejercicios = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Error al leer {file_path}: {e}")
            return ejercicios
        
        # Buscar todos los ejercicios en el archivo
        matches = self.ejercicio_pattern.findall(content)
        
        for metadata_str, ejercicio_content in matches:
            try:
                # Parsear metadatos
                metadata = self.parse_metadata(metadata_str)
                
                # Extraer contenido y solución
                enunciado = self.extract_ejercicio_content(ejercicio_content)
                solucion = self.extract_solucion(ejercicio_content)
                
                # Validar que tenga ID
                if 'id' not in metadata:
                    logger.warning(f"Ejercicio sin ID en {file_path}")
                    continue
                
                # Crear objeto ejercicio con estructura expandida
                ejercicio = {
                    'id': metadata.get('id', ''),
                    'materia_principal': metadata.get('materia_principal', materia_principal),
                    'codigo_materia': metadata.get('codigo_materia', ''),
                    'capitulo': metadata.get('capitulo', capitulo),
                    'subtema': metadata.get('subtema', ''),
                    'nivel': metadata.get('nivel', 'basico'),
                    'dificultad': metadata.get('dificultad', 2),
                    'tiempo_estimado': metadata.get('tiempo_estimado', 5),
                    'procedencia': metadata.get('procedencia', ''),
                    'visibilidad': metadata.get('visibilidad', 'web_impreso'),
                    'libros': metadata.get('libros', []),
                    'tags': metadata.get('tags', []),
                    'enunciado': enunciado,
                    'solucion': solucion,
                    'archivo_origen': str(file_path.relative_to(self.ejercicios_dir)),
                    'fecha_procesado': datetime.now().isoformat()
                }
                
                # Agregar campos opcionales si existen
                campos_opcionales = ['youtube_url', 'mostrar_solucion', 'libro_promocion']
                for campo in campos_opcionales:
                    if campo in metadata:
                        ejercicio[campo] = metadata[campo]
                
                ejercicios.append(ejercicio)
                logger.info(f"Procesado ejercicio: {ejercicio['id']}")
                
            except Exception as e:
                logger.error(f"Error al procesar ejercicio en {file_path}: {e}")
                continue
        
        return ejercicios
    
    def scan_ejercicios_directory(self) -> List[Dict[str, Any]]:
        """Escanea todo el directorio de ejercicios y extrae todos los ejercicios."""
        todos_ejercicios = []
        
        if not self.ejercicios_dir.exists():
            logger.error(f"Directorio no encontrado: {self.ejercicios_dir}")
            return todos_ejercicios
        
        # Recorrer estructura jerárquica: materia_principal/capitulo/*.tex
        for materia_dir in self.ejercicios_dir.iterdir():
            if not materia_dir.is_dir():
                continue
                
            materia_principal = materia_dir.name
            logger.info(f"Procesando materia principal: {materia_principal}")
            
            # Recorrer capítulos dentro de la materia
            for capitulo_dir in materia_dir.iterdir():
                if not capitulo_dir.is_dir():
                    continue
                    
                capitulo = capitulo_dir.name
                if capitulo == 'imagenes':  # Saltar directorio de imágenes
                    continue
                    
                logger.info(f"  Procesando capítulo: {capitulo}")
                
                # Procesar archivos .tex en el capítulo
                for tex_file in capitulo_dir.glob("*.tex"):
                    logger.info(f"    Procesando archivo: {tex_file.name}")
                    ejercicios = self.process_tex_file(tex_file, materia_principal, capitulo)
                    todos_ejercicios.extend(ejercicios)
        
        return todos_ejercicios
    
    def generar_metadatos(self, ejercicios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Genera metadatos estadísticos de los ejercicios."""
        metadatos = {
            'total_ejercicios': len(ejercicios),
            'fecha_generacion': datetime.now().isoformat(),
            'version_estructura': '2.0_jerarquica',
            'materias_principales': {},
            'capitulos': {},
            'niveles': {},
            'dificultades': {},
            'visibilidades': {},
            'codigos_materia': {}
        }
        
        for ejercicio in ejercicios:
            # Contadores por materia principal
            materia_principal = ejercicio['materia_principal']
            if materia_principal not in metadatos['materias_principales']:
                metadatos['materias_principales'][materia_principal] = 0
            metadatos['materias_principales'][materia_principal] += 1
            
            # Contadores por capítulo
            capitulo = ejercicio['capitulo']
            if capitulo not in metadatos['capitulos']:
                metadatos['capitulos'][capitulo] = 0
            metadatos['capitulos'][capitulo] += 1
            
            # Contadores por nivel
            nivel = ejercicio['nivel']
            if nivel not in metadatos['niveles']:
                metadatos['niveles'][nivel] = 0
            metadatos['niveles'][nivel] += 1
            
            # Contadores por dificultad
            dificultad = str(ejercicio['dificultad'])
            if dificultad not in metadatos['dificultades']:
                metadatos['dificultades'][dificultad] = 0
            metadatos['dificultades'][dificultad] += 1
            
            # Contadores por visibilidad
            visibilidad = ejercicio['visibilidad']
            if visibilidad not in metadatos['visibilidades']:
                metadatos['visibilidades'][visibilidad] = 0
            metadatos['visibilidades'][visibilidad] += 1
            
            # Contadores por código de materia
            codigo = ejercicio['codigo_materia']
            if codigo not in metadatos['codigos_materia']:
                metadatos['codigos_materia'][codigo] = 0
            metadatos['codigos_materia'][codigo] += 1
        
        return metadatos
    
    def export_to_json(self) -> bool:
        """Exporta todos los ejercicios a archivos JSON."""
        logger.info("Iniciando exportación a JSON...")
        
        # Escanear todos los ejercicios
        todos_ejercicios = self.scan_ejercicios_directory()
        
        if not todos_ejercicios:
            logger.warning("No se encontraron ejercicios para exportar")
            return False
        
        # Generar metadatos
        metadatos = self.generar_metadatos(todos_ejercicios)
        
        # Exportar archivo principal con todos los ejercicios
        archivo_principal = self.output_dir / "todos_ejercicios_nuevo.json"
        data_principal = {
            'metadatos': metadatos,
            'ejercicios': todos_ejercicios
        }
        
        with open(archivo_principal, 'w', encoding='utf-8') as f:
            json.dump(data_principal, f, ensure_ascii=False, indent=2)
        logger.info(f"Exportado: {archivo_principal}")
        
        # Exportar metadatos por separado
        archivo_metadatos = self.output_dir / "metadata_ejercicios_nuevo.json"
        with open(archivo_metadatos, 'w', encoding='utf-8') as f:
            json.dump(metadatos, f, ensure_ascii=False, indent=2)
        logger.info(f"Exportado: {archivo_metadatos}")
        
        # Exportar por materia principal
        ejercicios_por_materia = {}
        for ejercicio in todos_ejercicios:
            materia = ejercicio['materia_principal']
            if materia not in ejercicios_por_materia:
                ejercicios_por_materia[materia] = []
            ejercicios_por_materia[materia].append(ejercicio)
        
        for materia, ejercicios in ejercicios_por_materia.items():
            archivo_materia = self.output_dir / f"{materia}_nuevo.json"
            data_materia = {
                'materia_principal': materia,
                'total_ejercicios': len(ejercicios),
                'ejercicios': ejercicios
            }
            with open(archivo_materia, 'w', encoding='utf-8') as f:
                json.dump(data_materia, f, ensure_ascii=False, indent=2)
            logger.info(f"Exportado: {archivo_materia}")
        
        logger.info(f"✅ Exportación completada: {len(todos_ejercicios)} ejercicios procesados")
        return True

def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description='Exportar ejercicios LaTeX a JSON (Nueva Estructura)')
    parser.add_argument('--input', '-i', default='ejercicios_nuevo', help='Directorio de ejercicios (default: ejercicios_nuevo)')
    parser.add_argument('--output', '-o', default='etiquetas', help='Directorio de salida (default: etiquetas)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Salida detallada')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Crear exportador y ejecutar
    exporter = EjercicioExporterNuevo(args.input, args.output)
    success = exporter.export_to_json()
    
    if success:
        print("🎉 Exportación exitosa!")
        print(f"📁 Archivos generados en: {args.output}/")
        print("📋 Archivos principales:")
        print("   - todos_ejercicios_nuevo.json")
        print("   - metadata_ejercicios_nuevo.json")
        print("   - [materia]_nuevo.json (por materia)")
    else:
        print("❌ Error en la exportación")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())