# Guía para Crear Ejercicios en LaTeX

Esta guía te enseñará a crear ejercicios paso a paso usando LaTeX antes de cargarlos al proyecto.

## Índice
1. [Preparación Inicial](#preparación-inicial)
2. [Estructura del Ejercicio](#estructura-del-ejercicio)
3. [Configuración de Metadatos](#configuración-de-metadatos)
4. [Redacción del Enunciado](#redacción-del-enunciado)
5. [Solución Detallada](#solución-detallada)
6. [Comandos LaTeX Útiles](#comandos-latex-útiles)
7. [Ejemplos Completos](#ejemplos-completos)

## Preparación Inicial

### 1. Copia la Plantilla
```bash
cp plantillas/plantilla_ejercicio_nueva.tex mi_ejercicio.tex
```

### 2. Determina el ID del Ejercicio
- **Formato**: `[CODIGO_MATERIA]_[CAPITULO]_[NUMERO]`
- **Ejemplo**: `MATU_ALG_001`, `FISU_CIN_042`

### 3. Códigos de Materias Disponibles
- `MATU` = Matemáticas Preuniversitaria
- `FISU` = Física Preuniversitaria
- `QUIM` = Química Preuniversitaria
- `LENG` = Lenguaje y Literatura
- `CAL2` = Cálculo 2
- `FIS1` = Física 1

## Estructura del Ejercicio

```latex
\begin{ejercicio}[
  % METADATOS AQUÍ
]

% ENUNCIADO DEL PROBLEMA

\begin{solucion}
% SOLUCIÓN DETALLADA
\end{solucion}

\end{ejercicio}
```

## Configuración de Metadatos

### Metadatos Obligatorios

```latex
\begin{ejercicio}[
  id=MATU_ALG_001,                           % ID único
  materia_principal=matematicas_preuniversitaria,  % Materia principal
  codigo_materia=MATU,                       % Código de 4 chars
  capitulo=algebra,                          % Capítulo específico
  subtema=exponentes,                        % Subtema
  nivel=basico,                              % Nivel de dificultad
  procedencia="Examen UNI 2023",             % Origen del ejercicio
  visibilidad=web_impreso,                   % Dónde aparece
  tiempo_estimado=5,                         % Minutos estimados
  libros={matematicas_pre, algebra_completa}, % Libros relacionados
  dificultad=2,                              % Escala 1-5
  tags={exponentes, propiedades}             % Etiquetas
]
```

### Valores Permitidos

**Materias Principales**:
- `matematicas_preuniversitaria`
- `fisica_preuniversitaria`
- `quimica_preuniversitaria`
- `lenguaje_literatura`

**Niveles**:
- `basico`: Conceptos fundamentales, aplicación directa
- `intermedio`: Requiere varios pasos, conexión de conceptos
- `avanzado`: Problemas complejos, pensamiento crítico

**Visibilidad**:
- `web_impreso`: Aparece en ambos formatos
- `solo_impreso`: Solo en libros físicos
- `solo_web`: Solo en plataforma digital

**Dificultad**: Escala del 1 al 5
- `1`: Muy fácil
- `2`: Fácil
- `3`: Moderado
- `4`: Difícil
- `5`: Muy difícil

## Redacción del Enunciado

### 1. Estructura Recomendada
```latex
% Contexto del problema (si es necesario)
En un laboratorio de física...

% Enunciado principal
Calcula la velocidad final de un objeto que...

% Datos (si aplica)
Datos:
- Velocidad inicial: $v_0 = 10$ m/s
- Aceleración: $a = 2$ m/s²
- Tiempo: $t = 5$ s

% Opciones múltiples (si es examen)
a) $v = 15$ m/s  \quad b) $v = 20$ m/s  \quad c) $v = 25$ m/s
```

### 2. Comandos LaTeX para Matemáticas

**Fórmulas en línea**: `$x^2 + y^2 = z^2$`

**Fórmulas centradas**:
```latex
$$E = mc^2$$
```

**Sistemas de ecuaciones**:
```latex
\begin{cases}
x + y = 5 \\
2x - y = 1
\end{cases}
```

### 3. Incluir Imágenes
```latex
\begin{figure}[h]
  \includegraphics[width=0.6\textwidth]{imagenes/diagrama_fuerzas.png}
  \caption{Diagrama de fuerzas del problema}
\end{figure}
```

## Solución Detallada

### 1. Estructura Recomendada

```latex
\begin{solucion}

\textbf{Datos del problema:}
\begin{itemize}
    \item Velocidad inicial: $v_0 = 10$ m/s
    \item Aceleración: $a = 2$ m/s²
    \item Tiempo: $t = 5$ s
\end{itemize}

\textbf{Fórmula a usar:}
$$v = v_0 + at$$

\textbf{Desarrollo:}

Paso 1: Sustituir los valores
$$v = 10 + 2 \cdot 5$$

Paso 2: Calcular
$$v = 10 + 10 = 20 \text{ m/s}$$

\textbf{Respuesta:} La velocidad final es $v = 20$ m/s.

\end{solucion}
```

### 2. Elementos de una Buena Solución

1. **Identificar datos**: Lista clara de la información dada
2. **Fórmulas/Propiedades**: Ecuaciones o conceptos a usar
3. **Desarrollo paso a paso**: Cada paso claramente explicado
4. **Resultado final**: Respuesta clara y con unidades

## Comandos LaTeX Útiles

### Matemáticas Básicas
```latex
$x^2$           % Exponente
$x_1$           % Subíndice
$\frac{a}{b}$   % Fracción
$\sqrt{x}$      % Raíz cuadrada
$\sqrt[3]{x}$   % Raíz cúbica
```

### Símbolos Especiales
```latex
$\pi$       % Pi
$\alpha$    % Alpha
$\beta$     % Beta
$\theta$    % Theta
$\infty$    % Infinito
$\pm$       % Más/menos
$\cdot$     % Multiplicación (punto)
$\times$    % Multiplicación (cruz)
```

### Funciones
```latex
$\sin(x)$   % Seno
$\cos(x)$   % Coseno
$\tan(x)$   % Tangente
$\log(x)$   % Logaritmo
$\ln(x)$    % Logaritmo natural
```

### Vectores y Matrices
```latex
$\vec{v}$       % Vector
$\overrightarrow{AB}$  % Vector dirigido

\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}   % Matriz con paréntesis
```

## Ejemplos Completos

### Ejemplo 1: Matemáticas (Álgebra)

```latex
\begin{ejercicio}[
  id=MATU_ALG_002,
  materia_principal=matematicas_preuniversitaria,
  codigo_materia=MATU,
  capitulo=algebra,
  subtema=ecuaciones,
  nivel=basico,
  procedencia="Libro de texto",
  visibilidad=web_impreso,
  tiempo_estimado=3,
  libros={matematicas_pre},
  dificultad=1,
  tags={ecuaciones_lineales, algebra_basica}
]

Resuelve la siguiente ecuación:

$$3x + 7 = 22$$

a) $x = 4$  \quad b) $x = 5$  \quad c) $x = 6$  \quad d) $x = 7$

\begin{solucion}

\textbf{Ecuación a resolver:} $3x + 7 = 22$

\textbf{Desarrollo:}

Paso 1: Restar 7 en ambos lados
$$3x + 7 - 7 = 22 - 7$$
$$3x = 15$$

Paso 2: Dividir entre 3
$$\frac{3x}{3} = \frac{15}{3}$$
$$x = 5$$

\textbf{Verificación:}
$$3(5) + 7 = 15 + 7 = 22 \checkmark$$

\textbf{Respuesta:} b) $x = 5$

\end{solucion}

\end{ejercicio}
```

### Ejemplo 2: Física (Cinemática)

```latex
\begin{ejercicio}[
  id=FISU_CIN_001,
  materia_principal=fisica_preuniversitaria,
  codigo_materia=FISU,
  capitulo=cinematica,
  subtema=movimiento_rectilineo,
  nivel=intermedio,
  procedencia="Examen UNMSM 2023",
  visibilidad=web_impreso,
  tiempo_estimado=8,
  libros={fisica_pre},
  dificultad=3,
  tags={cinematica, velocidad, aceleracion}
]

Un automóvil parte del reposo y acelera uniformemente a razón de $2$ m/s². 
¿Qué distancia habrá recorrido después de $10$ segundos?

a) $50$ m  \quad b) $100$ m  \quad c) $150$ m  \quad d) $200$ m

\begin{solucion}

\textbf{Datos del problema:}
\begin{itemize}
    \item Velocidad inicial: $v_0 = 0$ m/s (parte del reposo)
    \item Aceleración: $a = 2$ m/s²
    \item Tiempo: $t = 10$ s
    \item Distancia: $d = ?$
\end{itemize}

\textbf{Fórmula cinemática:}
$$d = v_0 t + \frac{1}{2}at^2$$

\textbf{Desarrollo:}

Paso 1: Sustituir los valores conocidos
$$d = 0 \cdot 10 + \frac{1}{2} \cdot 2 \cdot 10^2$$

Paso 2: Simplificar
$$d = 0 + \frac{1}{2} \cdot 2 \cdot 100$$
$$d = 1 \cdot 100 = 100 \text{ m}$$

\textbf{Respuesta:} b) $100$ m

\end{solucion}

\end{ejercicio}
```

## Lista de Verificación

Antes de cargar tu ejercicio, verifica:

- [ ] ID único y correcto formato
- [ ] Todos los metadatos completos
- [ ] Enunciado claro y sin ambigüedades
- [ ] Matemáticas correctamente escritas en LaTeX
- [ ] Solución paso a paso detallada
- [ ] Respuesta final clara
- [ ] Nivel de dificultad apropiado
- [ ] Tags relevantes para búsqueda
