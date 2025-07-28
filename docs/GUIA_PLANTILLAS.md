# 📝 GUÍA COMPLETA: Plantillas LaTeX para Problemas y Teoría

## 🎯 **OBJETIVO**
Esta guía te enseñará cómo usar las plantillas LaTeX para crear problemas y teoría de manera eficiente y consistente.

---

## 📋 **CONTENIDO CREADO**

### ✅ **Plantillas Disponibles**
1. **`plantillas/plantilla_problema_latex.tex`** - Para generar problemas matemáticos
2. **`plantillas/plantilla_teoria_latex.tex`** - Para generar contenido teórico
3. **`generar_contenido.py`** - Script interactivo para generar contenido automáticamente

---

## 🚀 **MÉTODO RÁPIDO: Script Automático**

### **Paso 1: Ejecutar el generador**
```bash
python generar_contenido.py
```

### **Paso 2: Seguir las instrucciones**
- Selecciona "1" para generar un problema
- Selecciona "2" para generar teoría
- Completa la información solicitada
- El script creará el archivo automáticamente

### **Paso 3: Editar el contenido**
- El archivo se abrirá automáticamente en tu editor
- Reemplaza los marcadores `[ESCRIBIR_AQUI]` con tu contenido
- Guarda el archivo

### **Paso 4: Exportar a JSON**
```bash
python exportador/exportar_json.py
```

---

## 📝 **MÉTODO MANUAL: Usar Plantillas Directamente**

### **Para Problemas:**

#### **1. Copiar la plantilla**
```bash
cp plantillas/plantilla_problema_latex.tex ejercicios/algebra/mi_problema.tex
```

#### **2. Editar los campos obligatorios**
```latex
\begin{ejercicio}[
  id=ALG_EXP_001,                    ← CAMBIAR
  materia=algebra,                   ← CAMBIAR
  capitulo=exponentes,               ← CAMBIAR
  nivel=basico,                      ← CAMBIAR
  procedencia="Examen UNI 2024",     ← CAMBIAR
  visibilidad=true,
  libros={algebra_pre},              ← CAMBIAR
  youtube_url="",                    ← CAMBIAR
  mostrar_solucion=true,
  libro_promocion=""
]
```

#### **3. Escribir el enunciado**
```latex
% Reemplazar [ESCRIBIR_ENUNCIADO_AQUI] con:
Calcula el valor de: $2^3 \cdot 2^4 \div 2^2$

% Si necesitas una imagen:
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{imagenes/mi_imagen.png}
\caption{Descripción de la imagen}
\label{fig:mi_imagen}
\end{figure}
```

#### **4. Escribir la solución**
```latex
\begin{solucion}
% Reemplazar [ESCRIBIR_SOLUCION_AQUI] con:
Aplicando las propiedades de exponentes:

1) $2^3 \cdot 2^4 = 2^{3+4} = 2^7$
2) $2^7 \div 2^2 = 2^{7-2} = 2^5 = 32$

\textbf{Respuesta:} 32
\end{solucion}
```

### **Para Teoría:**

#### **1. Copiar la plantilla**
```bash
cp plantillas/plantilla_teoria_latex.tex teoria/algebra/exponentes.tex
```

#### **2. Editar los campos obligatorios**
```latex
\begin{teoria}[
  materia=algebra,                   ← CAMBIAR
  capitulo=exponentes,               ← CAMBIAR
  nivel=basico,                      ← CAMBIAR
  titulo="Propiedades de Exponentes", ← CAMBIAR
  descripcion="Conceptos fundamentales", ← CAMBIAR
  tiempo_estimado=30,                ← CAMBIAR
  dificultad=2,                      ← CAMBIAR
  prerequisitos={aritmetica_basica}, ← CAMBIAR
  objetivos={"Comprender propiedades"}, ← CAMBIAR
  tags={exponentes, potencias}       ← CAMBIAR
]
```

#### **3. Completar las secciones**
```latex
\section{Introducción}
% Reemplazar [ESCRIBIR_INTRODUCCION_AQUI]

\section{Conceptos Fundamentales}
\subsection{Definición Básica}
% Reemplazar [ESCRIBIR_DEFINICION_AQUI]

\section{Fórmulas Principales}
% Reemplazar [ESCRIBIR_FORMULAS_AQUI]

\section{Ejemplos Resueltos}
% Reemplazar [ESCRIBIR_EJEMPLO_1_AQUI]

\section{Resumen}
% Reemplazar [ESCRIBIR_RESUMEN_AQUI]
```

---

## 📁 **ESTRUCTURA DE CARPETAS RECOMENDADA**

```
plataforma_preuniversitaria/
├── ejercicios/
│   ├── algebra/
│   │   ├── exponentes_exp_001.tex
│   │   ├── exponentes_exp_002.tex
│   │   ├── polinomios_pol_001.tex
│   │   └── imagenes/
│   │       └── grafico_polinomio_001.png
│   ├── calculo/
│   │   ├── derivadas_der_001.tex
│   │   ├── integrales_int_001.tex
│   │   └── imagenes/
│   │       └── grafico_funcion_001.png
│   ├── fisica/
│   │   ├── cinematica_cin_001.tex
│   │   ├── dinamica_din_001.tex
│   │   └── imagenes/
│   │       └── diagrama_fuerzas_001.png
│   └── geometria/
│       ├── triangulos_tri_001.tex
│       ├── circunferencia_cir_001.tex
│       └── imagenes/
│           └── figura_geometrica_001.png
├── teoria/
│   ├── algebra/
│   │   ├── exponentes.tex
│   │   ├── polinomios.tex
│   │   └── imagenes/
│   │       └── grafico_exponencial.png
│   ├── calculo/
│   │   ├── derivadas.tex
│   │   ├── integrales.tex
│   │   └── imagenes/
│   │       └── grafico_derivada.png
│   ├── fisica/
│   │   ├── cinematica.tex
│   │   ├── dinamica.tex
│   │   └── imagenes/
│   │       └── diagrama_fuerzas.png
│   └── geometria/
│       ├── triangulos.tex
│       ├── circunferencia.tex
│       └── imagenes/
│           └── figura_triangulo.png
└── plantillas/
    ├── plantilla_problema_latex.tex
    └── plantilla_teoria_latex.tex
```

---

## 🆔 **SISTEMA DE IDs PARA PROBLEMAS**

### **Formato:** `PREFIJO_CAPITULO_NUMERO`

| Materia | Prefijo | Ejemplo |
|---------|---------|---------|
| Álgebra | `ALG` | `ALG_EXP_001` |
| Cálculo | `CAL` | `CAL_DER_001` |
| Física | `FIS` | `FIS_CIN_001` |
| Geometría | `GEO` | `GEO_TRI_001` |

### **Capítulos Comunes:**
- **Álgebra:** `EXP` (exponentes), `POL` (polinomios), `ECU` (ecuaciones)
- **Cálculo:** `DER` (derivadas), `INT` (integrales), `LIM` (límites)
- **Física:** `CIN` (cinemática), `DIN` (dinámica), `TER` (termodinámica)
- **Geometría:** `TRI` (triángulos), `CIR` (circunferencia), `POL` (polígonos)

---

## 📊 **CAMPOS OBLIGATORIOS**

### **Para Problemas:**
- `id` - Identificador único
- `materia` - algebra, calculo, fisica, geometria
- `capitulo` - exponentes, derivadas, cinematica, etc.
- `nivel` - basico, intermedio, avanzado
- `procedencia` - Origen del problema
- `visibilidad` - true/false
- `mostrar_solucion` - true/false

### **Para Teoría:**
- `materia` - algebra, calculo, fisica, geometria
- `capitulo` - exponentes, derivadas, cinematica, etc.
- `nivel` - basico, intermedio, avanzado
- `titulo` - Título de la teoría
- `descripcion` - Descripción breve
- `tiempo_estimado` - Minutos estimados
- `dificultad` - 1-5 (1=fácil, 5=difícil)

---

## 🎨 **COMANDOS LaTeX ÚTILES**

### **Matemáticas:**
```latex
% Fracciones
$\frac{a}{b}$

% Exponentes
$x^2$, $x^{n+1}$

% Raíces
$\sqrt{x}$, $\sqrt[n]{x}$

% Integrales
$\int_a^b f(x) dx$

% Derivadas
$\frac{d}{dx}f(x)$

% Límites
$\lim_{x \to a} f(x)$

% Sumatorias
$\sum_{i=1}^n x_i$

% Productorias
$\prod_{i=1}^n x_i$
```

### **Geometría:**
```latex
% Ángulos
$\angle ABC$

% Triángulos
$\triangle ABC$

% Paralelo
$\parallel$

% Perpendicular
$\perp$

% Congruente
$\cong$

% Similar
$\sim$

% Grados
$45^\circ$
```

### **Física:**
```latex
% Velocidad
$v = \frac{d}{t}$

% Aceleración
$a = \frac{v}{t}$

% Fuerza
$F = ma$

% Energía
$E = mc^2$

% Presión
$P = \frac{F}{A}$

% Densidad
$\rho = \frac{m}{V}$
```

### **Formato:**
```latex
% Negrita
\textbf{texto}

% Cursiva
\textit{texto}

% Subrayado
\underline{texto}

% Centrado
\begin{center}
texto centrado
\end{center}

% Listas
\begin{itemize}
\item Elemento 1
\item Elemento 2
\end{itemize}

% Numeración
\begin{enumerate}
\item Elemento 1
\item Elemento 2
\end{enumerate}
```

---

## 🖼️ **INCLUIR IMÁGENES**

### **En Problemas:**
```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{imagenes/mi_imagen.png}
\caption{Descripción de la imagen}
\label{fig:mi_imagen}
\end{figure}
```

### **En Teoría:**
```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.7\textwidth]{imagenes/grafico_teoria.png}
\caption{Gráfico explicativo}
\label{fig:grafico}
\end{figure}
```

### **Ubicación de Imágenes:**
- **Problemas:** `ejercicios/[MATERIA]/imagenes/`
- **Teoría:** `teoria/[MATERIA]/imagenes/`

---

## 🔧 **DIAGRAMAS TIKZ (OPCIONAL)**

### **Para Diagramas Geométricos:**
```latex
\begin{center}
\begin{tikzpicture}[scale=0.6]
\coordinate (A) at (0,0);
\coordinate (B) at (4,0);
\coordinate (C) at (2,3);

\draw[thick] (A) -- (B) -- (C) -- cycle;
\node[below] at (A) {$A$};
\node[below] at (B) {$B$};
\node[above] at (C) {$C$};
\end{tikzpicture}
\end{center}
```

---

## 📋 **EJEMPLOS COMPLETOS**

### **Ejemplo 1: Problema Básico**
```latex
\begin{ejercicio}[
  id=ALG_EXP_001,
  materia=algebra,
  capitulo=exponentes,
  nivel=basico,
  procedencia="Examen UNI 2024",
  visibilidad=true,
  libros={algebra_pre},
  youtube_url="https://www.youtube.com/watch?v=ejemplo",
  mostrar_solucion=true,
  libro_promocion=""
]
Calcula el valor de: $2^3 \cdot 2^4 \div 2^2$

\begin{solucion}
Aplicando las propiedades de exponentes:

1) $2^3 \cdot 2^4 = 2^{3+4} = 2^7$
2) $2^7 \div 2^2 = 2^{7-2} = 2^5 = 32$

\textbf{Respuesta:} 32
\end{solucion}
\end{ejercicio}
```

### **Ejemplo 2: Teoría Completa**
```latex
\begin{teoria}[
  materia=algebra,
  capitulo=exponentes,
  nivel=basico,
  titulo="Propiedades de Exponentes",
  descripcion="Conceptos fundamentales de exponentes",
  tiempo_estimado=30,
  dificultad=2,
  prerequisitos={aritmetica_basica},
  objetivos={"Comprender propiedades básicas"},
  tags={exponentes, potencias}
]

\section{Introducción}
Los exponentes son una herramienta fundamental...

\section{Conceptos Fundamentales}
\subsection{Definición Básica}
Si $a$ es un número real y $n$ es un entero positivo...

\section{Fórmulas Principales}
\begin{center}
\begin{tabular}{|c|c|}
\hline
\textbf{Propiedad} & \textbf{Fórmula} \\
\hline
Producto de potencias & $a^m \cdot a^n = a^{m+n}$ \\
\hline
\end{tabular}
\end{center}

\section{Resumen}
En este capítulo hemos aprendido...
\end{teoria}
```

---

## 🚀 **FLUJO DE TRABAJO RECOMENDADO**

### **1. Planificación**
- Decide la materia y capítulo
- Determina el nivel de dificultad
- Planifica el contenido

### **2. Generación**
- Usa `python generar_contenido.py`
- O copia manualmente las plantillas

### **3. Escritura**
- Completa los campos obligatorios
- Escribe el contenido principal
- Incluye imágenes si es necesario

### **4. Revisión**
- Verifica que todos los campos estén completos
- Revisa la ortografía y gramática
- Comprueba que las fórmulas sean correctas

### **5. Exportación**
```bash
python exportador/exportar_json.py
```

### **6. Prueba**
- Ejecuta `python app.py`
- Verifica que el contenido se muestre correctamente
- Prueba en la web: http://localhost:5000

---

## 🔍 **SOLUCIÓN DE PROBLEMAS**

### **Error: "Plantilla no encontrada"**
- Verifica que las plantillas estén en `plantillas/`
- Ejecuta desde el directorio raíz del proyecto

### **Error: "ID duplicado"**
- El script genera IDs automáticamente
- Si es manual, verifica que el ID sea único

### **Error: "Imagen no encontrada"**
- Verifica que la imagen esté en la carpeta correcta
- Usa rutas relativas: `imagenes/mi_imagen.png`

### **Error: "Sintaxis LaTeX incorrecta"**
- Verifica que las fórmulas estén entre `$` o `$$`
- Comprueba que los comandos estén bien escritos

---

## 📞 **SOPORTE**

### **Comandos Útiles:**
```bash
# Generar contenido automáticamente
python generar_contenido.py

# Exportar a JSON
python exportador/exportar_json.py

# Ejecutar servidor web
python app.py

# Ver estructura de carpetas
python generar_contenido.py
# Seleccionar opción 3
```

### **Archivos de Referencia:**
- `plantillas/plantilla_problema_latex.tex` - Plantilla de problemas
- `plantillas/plantilla_teoria_latex.tex` - Plantilla de teoría
- `GUIA_PLANTILLAS.md` - Esta guía
- `SOLUCION_ERRORES.md` - Solución de errores comunes

---

## 🎯 **CONSEJOS FINALES**

1. **Sé consistente:** Usa el mismo formato para problemas similares
2. **Incluye ejemplos:** Los ejemplos ayudan a entender mejor
3. **Usa imágenes:** Las imágenes mejoran la comprensión
4. **Revisa antes de publicar:** Siempre verifica el contenido
5. **Mantén organizado:** Sigue la estructura de carpetas
6. **Documenta:** Incluye referencias y fuentes
7. **Prueba:** Verifica que todo funcione en la web

¡Con estas plantillas y herramientas, crear contenido preuniversitario será mucho más fácil y eficiente! 🚀 