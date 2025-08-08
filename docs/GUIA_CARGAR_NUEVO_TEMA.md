# Guía para Cargar un Nuevo Tema

Esta guía te ayudará a cargar un nuevo tema en la plataforma, incluyendo todos sus componentes: formulario PDF, teoría en PDF y teoría web.

## Índice
1. [Estructura de Archivos](#estructura-de-archivos)
2. [Pasos para Cargar un Nuevo Tema](#pasos-para-cargar-un-nuevo-tema)
3. [Configuración de Archivos](#configuración-de-archivos)
4. [Ejemplo Práctico](#ejemplo-práctico)

## Estructura de Archivos

```
plataforma_preuniversitaria/
├── etiquetas/
│   ├── formularios.json           # Configuración de formularios
│   └── teoria_capitulos.json      # Configuración de teoría
├── static/
│   ├── formularios/
│   │   └── form_[materia]_[tema].pdf    # Ej: form_calculo_limites.pdf
│   └── teoria/
│       └── [materia]/
│           └── teo_[materia]_[tema].pdf  # Ej: teo_algebra_exponentes.pdf
└── ejercicios_nuevo/
    └── [materia_principal]/
        └── [capitulo]/
            └── [CODIGO]_[CAP]_[NUM].tex  # Ej: MATU_ALG_001.tex
```

## Pasos para Cargar un Nuevo Tema

### 1. Preparar los Archivos PDF

1. **Formulario PDF**:
   - Crear el formulario con las fórmulas principales
   - Nombrar como: `form_[materia]_[tema].pdf`
   - Guardar en: `static/formularios/`
   - Ejemplo: `form_algebra_exponentes.pdf`

2. **Teoría PDF**:
   - Crear el PDF con la teoría completa
   - Nombrar como: `teo_[materia]_[tema].pdf`
   - Guardar en: `static/teoria/[materia]/`
   - Ejemplo: `teo_algebra_exponentes.pdf`

### 2. Configurar Formularios

Editar `etiquetas/formularios.json`:

```json
{
  "formularios": {
    "algebra": {
      "exponentes": {
        "titulo": "Formulario de Exponentes y Radicales",
        "descripcion": "Todas las propiedades y fórmulas importantes...",
        "archivo": "formularios/form_algebra_exponentes.pdf",
        "tamaño": "245 KB",
        "version": "1.0",
        "fecha_actualizacion": "2024-03-19",
        "contenido": [
          "Propiedades básicas de exponentes",
          "Exponentes negativos y cero",
          "Radicales y exponentes fraccionarios"
        ]
      }
    }
  }
}
```

### 3. Configurar Teoría

Editar `etiquetas/teoria_capitulos.json`:

```json
{
  "capitulos": {
    "algebra": {
      "exponentes": {
        "titulo": "Exponentes y Radicales",
        "introduccion": "Los exponentes son una herramienta fundamental...",
        "conceptos_clave": [
          "Potenciación como multiplicación repetida",
          "Propiedades de los exponentes",
          "Exponentes negativos y cero"
        ],
        "propiedades": [
          {
            "nombre": "Producto de potencias de igual base",
            "formula": "$a^m \\cdot a^n = a^{m+n}$",
            "ejemplo": "$2^3 \\cdot 2^4 = 2^{3+4} = 2^7 = 128$"
          }
        ],
        "ejemplos_practicos": [
          {
            "titulo": "Simplificación de expresiones",
            "descripcion": "Simplificar $\\frac{x^4 y^{-2}}{x^{-1} y^3}$",
            "solucion": "..."
          }
        ],
        "consejos_estudio": [
          "Memoriza las propiedades básicas",
          "Practica con ejercicios de simplificación"
        ]
      }
    }
  }
}
```

## Ejemplo Práctico

Vamos a agregar un tema de "Límites" en Cálculo:

1. **Preparar archivos**:
   ```bash
   # Crear directorios si no existen
   mkdir -p static/teoria/calculo
   
   # Mover archivos PDF
   mv form_calculo_limites.pdf static/formularios/
   mv teo_calculo_limites.pdf static/teoria/calculo/
   ```

2. **Configurar formularios.json**:
   ```json
   {
     "formularios": {
       "calculo": {
         "limites": {
           "titulo": "Formulario de Límites",
           "descripcion": "Propiedades y técnicas para el cálculo de límites",
           "archivo": "formularios/form_calculo_limites.pdf",
           "tamaño": "312 KB",
           "version": "1.0",
           "fecha_actualizacion": "2024-03-19",
           "contenido": [
             "Propiedades básicas de límites",
             "Límites laterales",
             "Límites infinitos"
           ]
         }
       }
     }
   }
   ```

3. **Verificar acceso**:
   - Teoría web: `/teoria/calculo/limites`
   - Descargar teoría: `/descargar/teoria/calculo/limites`
   - Descargar formulario: `/descargar/calculo/limites`

## Verificación Final

1. **Archivos necesarios**:
   - [ ] Formulario PDF en `static/formularios/`
   - [ ] Teoría PDF en `static/teoria/[materia]/`
   - [ ] Configuración en `formularios.json`
   - [ ] Configuración en `teoria_capitulos.json`

2. **Verificar en la web**:
   - [ ] El tema aparece en la página de teoría
   - [ ] El botón "Ver Teoría Completa" funciona
   - [ ] El botón "Teoría PDF" descarga el archivo correcto
   - [ ] El botón "Formulario" descarga el archivo correcto

3. **Convenciones de nombres**:
   - Formularios: `form_[materia]_[tema].pdf`
   - Teoría PDF: `teo_[materia]_[tema].pdf`
   - URLs: usar todo en minúsculas y guiones para espacios

4. **Reiniciar servidor**:
   ```bash
   # Detener el servidor actual
   Ctrl + C
   
   # Reiniciar el servidor
   python app.py
   ```