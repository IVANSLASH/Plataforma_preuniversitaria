#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exportador de ejercicios LaTeX a JSON
=====================================

Este script lee todos los archivos .tex de la carpeta ejercicios/,
extrae los ejercicios con sus metadatos y los exporta a formato JSON
organizados por materia.

Autor: Plataforma Preuniversitaria
Fecha: 2024
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EjercicioExporter:
    """Clase para exportar ejercicios de LaTeX a JSON."""
    
    def __init__(self, ejercicios_dir: str = "ejercicios", output_dir: str = "etiquetas"):
        self.ejercicios_dir = Path(ejercicios_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Patrón regex para extraer ejercicios
        self.ejercicio_pattern = re.compile(
            r'\\begin\{ejercicio\}\[(.*?)\](.*?)\\end\{ejercicio\}',
            re.DOTALL
        )
        
        # Patrón mejorado para extraer metadatos
        self.metadata_pattern = re.compile(
            r'(\w+)=([^,\n]+(?:{[^}]*})?)',
            re.DOTALL
        )
        
        # Patrón para extraer solución
        self.solucion_pattern = re.compile(
            r'\\begin\{solucion\}(.*?)\\end\{solucion\}',
            re.DOTALL
        )
    
    def parse_metadata(self, metadata_str: str) -> Dict[str, Any]:
        """Parsea los metadatos de un ejercicio."""
        metadata = {}
        
        # Extraer pares clave=valor
        matches = self.metadata_pattern.findall(metadata_str)
        
        for key, value in matches:
            # Limpiar el valor
            value = value.strip().strip('"').strip("'")
            
            # Procesar listas (valores entre llaves)
            if value.startswith('{') and value.endswith('}'):
                value = value[1:-1].split(',')
                value = [v.strip() for v in value]
            
            # Convertir tipos
            if value.lower() in ['true', 'false']:
                value = value.lower() == 'true'
            elif value.isdigit():
                value = int(value)
            
            metadata[key] = value
        
        return metadata
    
    def extract_ejercicio_content(self, content: str) -> str:
        """Extrae el contenido del ejercicio (sin metadatos ni solución)."""
        # Remover metadatos
        content = re.sub(r'\\begin\{ejercicio\}\[.*?\]', '', content)
        content = re.sub(r'\\end\{ejercicio\}', '', content)
        
        # Remover solución
        content = re.sub(r'\\begin\{solucion\}.*?\\end\{solucion\}', '', content, flags=re.DOTALL)
        
        return content.strip()
    
    def extract_solucion(self, content: str) -> str:
        """Extrae la solución del ejercicio."""
        match = self.solucion_pattern.search(content)
        if match:
            return match.group(1).strip()
        return ""
    
    def process_tex_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Procesa un archivo .tex y extrae todos los ejercicios."""
        ejercicios = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Encontrar todos los ejercicios
            matches = self.ejercicio_pattern.findall(content)
            
            for metadata_str, ejercicio_content in matches:
                try:
                    # Parsear metadatos
                    metadata = self.parse_metadata(metadata_str)
                    
                    # Extraer contenido y solución
                    enunciado = self.extract_ejercicio_content(ejercicio_content)
                    solucion = self.extract_solucion(ejercicio_content)
                    
                    # Crear objeto del ejercicio
                    ejercicio = {
                        'id': metadata.get('id', ''),
                        'materia': metadata.get('materia', ''),
                        'capitulo': metadata.get('capitulo', ''),
                        'nivel': metadata.get('nivel', ''),
                        'procedencia': metadata.get('procedencia', ''),
                        'visibilidad': metadata.get('visibilidad', True),
                        'libros': metadata.get('libros', []),
                        'youtube_url': metadata.get('youtube_url', ''),
                        'mostrar_solucion': metadata.get('mostrar_solucion', True),
                        'libro_promocion': metadata.get('libro_promocion', ''),
                        'enunciado': enunciado,
                        'solucion': solucion,
                        'archivo_origen': str(file_path),
                        'linea_inicio': content[:content.find(metadata_str)].count('\n') + 1
                    }
                    
                    ejercicios.append(ejercicio)
                    
                except Exception as e:
                    logger.error(f"Error procesando ejercicio en {file_path}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error leyendo archivo {file_path}: {e}")
        
        return ejercicios
    
    def export_by_materia(self, ejercicios: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Organiza ejercicios por materia."""
        materias = {}
        
        for ejercicio in ejercicios:
            materia = ejercicio.get('materia', 'sin_materia')
            if materia not in materias:
                materias[materia] = []
            materias[materia].append(ejercicio)
        
        return materias
    
    def create_metadata_index(self, ejercicios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Crea un índice de metadatos para filtrado rápido."""
        index = {
            'total_ejercicios': len(ejercicios),
            'materias': {},
            'capitulos': {},
            'niveles': {},
            'libros': {},
            'visibles_web': 0,
            'no_visibles_web': 0
        }
        
        for ejercicio in ejercicios:
            materia = ejercicio.get('materia', 'sin_materia')
            capitulo = ejercicio.get('capitulo', 'sin_capitulo')
            nivel = ejercicio.get('nivel', 'sin_nivel')
            libros = ejercicio.get('libros', [])
            visibilidad = ejercicio.get('visibilidad', True)
            
            # Contar por materia
            if materia not in index['materias']:
                index['materias'][materia] = 0
            index['materias'][materia] += 1
            
            # Contar por capítulo
            if capitulo not in index['capitulos']:
                index['capitulos'][capitulo] = 0
            index['capitulos'][capitulo] += 1
            
            # Contar por nivel
            if nivel not in index['niveles']:
                index['niveles'][nivel] = 0
            index['niveles'][nivel] += 1
            
            # Contar por libro
            for libro in libros:
                if libro not in index['libros']:
                    index['libros'][libro] = 0
                index['libros'][libro] += 1
            
            # Contar visibilidad
            if visibilidad:
                index['visibles_web'] += 1
            else:
                index['no_visibles_web'] += 1
        
        return index
    
    def export(self) -> None:
        """Exporta todos los ejercicios a JSON."""
        logger.info("Iniciando exportación de ejercicios...")
        
        all_ejercicios = []
        
        # Procesar todos los archivos .tex
        for tex_file in self.ejercicios_dir.rglob("*.tex"):
            logger.info(f"Procesando: {tex_file}")
            ejercicios = self.process_tex_file(tex_file)
            all_ejercicios.extend(ejercicios)
        
        logger.info(f"Total de ejercicios encontrados: {len(all_ejercicios)}")
        
        if not all_ejercicios:
            logger.warning("No se encontraron ejercicios para exportar")
            return
        
        # Organizar por materia
        materias = self.export_by_materia(all_ejercicios)
        
        # Exportar archivos JSON por materia
        for materia, ejercicios_materia in materias.items():
            output_file = self.output_dir / f"{materia}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'materia': materia,
                    'total_ejercicios': len(ejercicios_materia),
                    'ejercicios': ejercicios_materia
                }, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Exportado {len(ejercicios_materia)} ejercicios de {materia} a {output_file}")
        
        # Crear índice de metadatos
        metadata_index = self.create_metadata_index(all_ejercicios)
        index_file = self.output_dir / "metadata_ejercicios.json"
        
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(metadata_index, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Índice de metadatos creado en {index_file}")
        
        # Exportar todos los ejercicios en un solo archivo
        all_file = self.output_dir / "todos_ejercicios.json"
        with open(all_file, 'w', encoding='utf-8') as f:
            json.dump({
                'total_ejercicios': len(all_ejercicios),
                'ejercicios': all_ejercicios
            }, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Todos los ejercicios exportados a {all_file}")
        logger.info("Exportación completada exitosamente!")

def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description='Exportar ejercicios LaTeX a JSON')
    parser.add_argument('--ejercicios-dir', default='ejercicios', 
                       help='Directorio con archivos .tex de ejercicios')
    parser.add_argument('--output-dir', default='etiquetas',
                       help='Directorio de salida para archivos JSON')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Mostrar información detallada')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    exporter = EjercicioExporter(args.ejercicios_dir, args.output_dir)
    exporter.export()

if __name__ == "__main__":
    main() 