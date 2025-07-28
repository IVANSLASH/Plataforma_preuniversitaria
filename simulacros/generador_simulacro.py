#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Simulacros
=======================

Este script genera simulacros de práctica seleccionando ejercicios
aleatoriamente del repositorio central según criterios específicos.

Autor: Plataforma Preuniversitaria
Fecha: 2024
"""

import os
import json
import random
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimulacroGenerator:
    """Generador de simulacros de práctica."""
    
    def __init__(self, ejercicios_dir: str = "etiquetas", output_dir: str = "simulacros"):
        self.ejercicios_dir = Path(ejercicios_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Cargar todos los ejercicios
        self.ejercicios = self.load_ejercicios()
    
    def load_ejercicios(self) -> List[Dict[str, Any]]:
        """Carga todos los ejercicios desde los archivos JSON."""
        ejercicios = []
        
        # Cargar desde el archivo principal
        todos_file = self.ejercicios_dir / "todos_ejercicios.json"
        if todos_file.exists():
            with open(todos_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                ejercicios = data.get('ejercicios', [])
                logger.info(f"Cargados {len(ejercicios)} ejercicios desde {todos_file}")
        else:
            # Cargar desde archivos por materia
            for json_file in self.ejercicios_dir.glob("*.json"):
                if json_file.name != "metadata_ejercicios.json":
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        ejercicios.extend(data.get('ejercicios', []))
                        logger.info(f"Cargados ejercicios desde {json_file}")
        
        return ejercicios
    
    def filter_ejercicios(self, 
                         materia: Optional[str] = None,
                         nivel: Optional[str] = None,
                         capitulo: Optional[str] = None,
                         visibilidad: Optional[bool] = None,
                         libros: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Filtra ejercicios según criterios específicos."""
        filtered = self.ejercicios.copy()
        
        if materia:
            filtered = [e for e in filtered if e.get('materia') == materia]
            logger.info(f"Filtrado por materia '{materia}': {len(filtered)} ejercicios")
        
        if nivel:
            filtered = [e for e in filtered if e.get('nivel') == nivel]
            logger.info(f"Filtrado por nivel '{nivel}': {len(filtered)} ejercicios")
        
        if capitulo:
            filtered = [e for e in filtered if e.get('capitulo') == capitulo]
            logger.info(f"Filtrado por capítulo '{capitulo}': {len(filtered)} ejercicios")
        
        if visibilidad is not None:
            filtered = [e for e in filtered if e.get('visibilidad') == visibilidad]
            logger.info(f"Filtrado por visibilidad '{visibilidad}': {len(filtered)} ejercicios")
        
        if libros:
            filtered = [e for e in filtered if any(libro in e.get('libros', []) for libro in libros)]
            logger.info(f"Filtrado por libros {libros}: {len(filtered)} ejercicios")
        
        return filtered
    
    def select_random_ejercicios(self, ejercicios: List[Dict[str, Any]], 
                                cantidad: int, 
                                evitar_duplicados: bool = True) -> List[Dict[str, Any]]:
        """Selecciona ejercicios aleatoriamente."""
        if len(ejercicios) < cantidad:
            logger.warning(f"Solo hay {len(ejercicios)} ejercicios disponibles, se seleccionarán todos")
            cantidad = len(ejercicios)
        
        if evitar_duplicados:
            selected = random.sample(ejercicios, cantidad)
        else:
            selected = random.choices(ejercicios, k=cantidad)
        
        return selected
    
    def generate_latex_simulacro(self, ejercicios: List[Dict[str, Any]], 
                                titulo: str, 
                                instrucciones: str = "") -> str:
        """Genera el contenido LaTeX del simulacro."""
        latex_content = f"""\\documentclass[12pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[spanish]{{babel}}
\\usepackage{{amsmath,amssymb,amsfonts}}
\\usepackage{{geometry}}
\\usepackage{{fancyhdr}}
\\usepackage{{enumitem}}

% Configuración de página
\\geometry{{margin=2.5cm}}
\\pagestyle{{fancy}}
\\fancyhf{{}}
\\fancyhead[L]{{{titulo}}}
\\fancyhead[R]{{Página \\thepage}}
\\renewcommand{{\\headrulewidth}}{{0.4pt}}

% Configuración de listas
\\setlist[enumerate]{{label=\\arabic*., leftmargin=*}}

% Información del documento
\\title{{\\Huge \\textbf{{{titulo}}}}}
\\author{{Plataforma Preuniversitaria}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

\\section*{{Instrucciones}}
{instrucciones}

\\section*{{Ejercicios}}

"""
        
        # Agregar ejercicios numerados
        for i, ejercicio in enumerate(ejercicios, 1):
            latex_content += f"""
\\begin{{enumerate}}
\\item[\\textbf{{{i}.}}] {ejercicio['enunciado']}
\\end{{enumerate}}

\\vspace{{1cm}}

"""
        
        # Agregar sección de soluciones
        latex_content += """
\\newpage
\\section*{Soluciones}

"""
        
        for i, ejercicio in enumerate(ejercicios, 1):
            latex_content += f"""
\\textbf{{{i}.}} {ejercicio['solucion']}

\\vspace{{0.5cm}}

"""
        
        latex_content += """
\\end{document}
"""
        
        return latex_content
    
    def generate_json_simulacro(self, ejercicios: List[Dict[str, Any]], 
                               titulo: str, 
                               metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Genera la estructura JSON del simulacro."""
        return {
            'titulo': titulo,
            'fecha_generacion': datetime.now().isoformat(),
            'total_ejercicios': len(ejercicios),
            'metadata': metadata,
            'ejercicios': ejercicios
        }
    
    def create_simulacro(self, 
                        titulo: str,
                        cantidad: int = 10,
                        materia: Optional[str] = None,
                        nivel: Optional[str] = None,
                        capitulo: Optional[str] = None,
                        visibilidad: bool = True,
                        libros: Optional[List[str]] = None,
                        instrucciones: str = "Resuelve los siguientes ejercicios. Tienes 2 horas para completar el simulacro.",
                        formato: str = "latex") -> str:
        """Crea un simulacro completo."""
        logger.info(f"Generando simulacro: {titulo}")
        
        # Filtrar ejercicios
        ejercicios_filtrados = self.filter_ejercicios(
            materia=materia,
            nivel=nivel,
            capitulo=capitulo,
            visibilidad=visibilidad,
            libros=libros
        )
        
        if not ejercicios_filtrados:
            raise ValueError("No se encontraron ejercicios que cumplan los criterios especificados")
        
        # Seleccionar ejercicios aleatoriamente
        ejercicios_seleccionados = self.select_random_ejercicios(
            ejercicios_filtrados, 
            cantidad
        )
        
        # Crear metadata del simulacro
        metadata = {
            'materia': materia,
            'nivel': nivel,
            'capitulo': capitulo,
            'visibilidad': visibilidad,
            'libros': libros,
            'criterios_seleccion': {
                'materia': materia,
                'nivel': nivel,
                'capitulo': capitulo,
                'visibilidad': visibilidad,
                'libros': libros
            }
        }
        
        # Generar archivo según formato
        if formato.lower() == "latex":
            contenido = self.generate_latex_simulacro(
                ejercicios_seleccionados, 
                titulo, 
                instrucciones
            )
            filename = f"simulacro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tex"
        elif formato.lower() == "json":
            contenido = self.generate_json_simulacro(
                ejercicios_seleccionados, 
                titulo, 
                metadata
            )
            filename = f"simulacro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        else:
            raise ValueError(f"Formato no soportado: {formato}")
        
        # Guardar archivo
        output_file = self.output_dir / filename
        
        if formato.lower() == "latex":
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(contenido)
        else:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(contenido, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Simulacro guardado en: {output_file}")
        
        # Generar resumen
        self.print_simulacro_summary(titulo, ejercicios_seleccionados, metadata)
        
        return str(output_file)
    
    def print_simulacro_summary(self, titulo: str, ejercicios: List[Dict[str, Any]], 
                               metadata: Dict[str, Any]) -> None:
        """Imprime un resumen del simulacro generado."""
        print(f"\n{'='*60}")
        print(f"SIMULACRO GENERADO: {titulo}")
        print(f"{'='*60}")
        print(f"Total de ejercicios: {len(ejercicios)}")
        print(f"Materia: {metadata.get('materia', 'Todas')}")
        print(f"Nivel: {metadata.get('nivel', 'Todos')}")
        print(f"Capítulo: {metadata.get('capitulo', 'Todos')}")
        print(f"Visibilidad web: {metadata.get('visibilidad', True)}")
        
        # Estadísticas por nivel
        niveles = {}
        capitulos = {}
        for ejercicio in ejercicios:
            nivel = ejercicio.get('nivel', 'sin_nivel')
            capitulo = ejercicio.get('capitulo', 'sin_capitulo')
            
            niveles[nivel] = niveles.get(nivel, 0) + 1
            capitulos[capitulo] = capitulos.get(capitulo, 0) + 1
        
        print(f"\nDistribución por nivel:")
        for nivel, count in niveles.items():
            print(f"  - {nivel}: {count} ejercicios")
        
        print(f"\nDistribución por capítulo:")
        for capitulo, count in capitulos.items():
            print(f"  - {capitulo}: {count} ejercicios")
        
        print(f"{'='*60}\n")

def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description='Generar simulacros de práctica')
    parser.add_argument('--titulo', required=True, help='Título del simulacro')
    parser.add_argument('--cantidad', type=int, default=10, help='Número de ejercicios')
    parser.add_argument('--materia', help='Filtrar por materia')
    parser.add_argument('--nivel', help='Filtrar por nivel (basico, intermedio, avanzado)')
    parser.add_argument('--capitulo', help='Filtrar por capítulo')
    parser.add_argument('--visibilidad', type=bool, default=True, help='Filtrar por visibilidad')
    parser.add_argument('--libros', nargs='+', help='Filtrar por libros')
    parser.add_argument('--formato', choices=['latex', 'json'], default='latex', help='Formato de salida')
    parser.add_argument('--ejercicios-dir', default='etiquetas', help='Directorio con ejercicios JSON')
    parser.add_argument('--output-dir', default='simulacros', help='Directorio de salida')
    parser.add_argument('--instrucciones', default='Resuelve los siguientes ejercicios. Tienes 2 horas para completar el simulacro.', help='Instrucciones del simulacro')
    
    args = parser.parse_args()
    
    try:
        generator = SimulacroGenerator(args.ejercicios_dir, args.output_dir)
        
        output_file = generator.create_simulacro(
            titulo=args.titulo,
            cantidad=args.cantidad,
            materia=args.materia,
            nivel=args.nivel,
            capitulo=args.capitulo,
            visibilidad=args.visibilidad,
            libros=args.libros,
            instrucciones=args.instrucciones,
            formato=args.formato
        )
        
        print(f"✅ Simulacro generado exitosamente: {output_file}")
        
    except Exception as e:
        logger.error(f"Error generando simulacro: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 