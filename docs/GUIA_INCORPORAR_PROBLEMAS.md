# 📚 GUÍA COMPLETA: Cómo Incorporar Problemas

## 🎯 **OBJETIVO**
Esta guía te enseñará paso a paso cómo añadir nuevos problemas matemáticos a tu plataforma preuniversitaria.

---

## 📋 **PASO 1: PREPARACIÓN INICIAL**

### 1.1 Verificar que tienes Python instalado
```bash
python --version
```
**Debe mostrar:** Python 3.8 o superior ✅

### 1.2 Instalar dependencias (solo la primera vez)
```bash
pip install -r requirements.txt
```

### 1.3 Verificar la estructura del proyecto
```
plataforma_preuniversitaria/
├── ejercicios/          ← AQUÍ VAN TUS PROBLEMAS
├── exportador/          ← Scripts de conversión
├── etiquetas/           ← Archivos JSON generados
└── ...
```

---

## 📝 **PASO 2: CREAR UN NUEVO PROBLEMA**

### 2.1 Elegir la ubicación del archivo
**Regla:** `ejercicios/[MATERIA]/[CAPITULO]_[CODIGO].tex`

**Ejemplos:**
- `ejercicios/algebra/exponentes_exp_003.tex`
- `ejercicios/calculo/derivadas_der_001.tex`
- `ejercicios/fisica/cinematica_cin_002.tex`

### 2.2 Estructura OBLIGATORIA del problema

```latex
\begin{ejercicio}[
  id=ALG_EXP_003,
  materia=algebra,
  capitulo=exponentes,
  nivel=basico,
  procedencia="Examen UNI 2023",
  visibilidad=true,
  libros={algebra_pre, algebra_basica}
]
[TU ENUNCIADO AQUÍ]

\begin{solucion}
[TU SOLUCIÓN AQUÍ]
\end{solucion}
\end{ejercicio}
```

### 2.3 Explicación de cada campo:

| Campo | Descripción | Ejemplos |
|-------|-------------|----------|
| `id` | Identificador único | `ALG_EXP_003`, `CAL_DER_001` |
| `materia` | Materia del problema | `algebra`, `calculo`, `fisica` |
| `capitulo` | Tema específico | `exponentes`, `derivadas`, `cinematica` |
| `nivel` | Dificultad | `basico`, `intermedio`, `avanzado` |
| `procedencia` | Origen del problema | `"Examen UNI 2023"`, `"Libro Álgebra 1"` |
| `visibilidad` | ¿Aparece en la web? | `true` (sí), `false` (no) |
| `libros` | Libros donde aparece | `{algebra_pre}`, `{calculo1, calculo_basico}` |

---

## 📖 **PASO 3: EJEMPLOS PRÁCTICOS**

### 3.1 Problema Básico de Álgebra

**Archivo:** `ejercicios/algebra/exponentes_exp_003.tex`

```latex
\begin{ejercicio}[
  id=ALG_EXP_003,
  materia=algebra,
  capitulo=exponentes,
  nivel=basico,
  procedencia="Examen UNI 2023",
  visibilidad=true,
  libros={algebra_pre}
]
Calcula el valor de: $3^2 \cdot 3^3$

\begin{solucion}
Aplicando la propiedad de exponentes: $a^m \cdot a^n = a^{m+n}$

$3^2 \cdot 3^3 = 3^{2+3} = 3^5 = 243$

\textbf{Respuesta:} 243
\end{solucion}
\end{ejercicio}
```

### 3.2 Problema de Cálculo

**Archivo:** `ejercicios/calculo/derivadas_der_001.tex`

```latex
\begin{ejercicio}[
  id=CAL_DER_001,
  materia=calculo,
  capitulo=derivadas,
  nivel=intermedio,
  procedencia="Libro Cálculo Avanzado",
  visibilidad=true,
  libros={calculo1, calculo_avanzado}
]
Calcula la derivada de: $f(x) = x^2 \cdot e^x$

\begin{solucion}
Usando la regla del producto: $(u \cdot v)' = u' \cdot v + u \cdot v'$

Donde $u = x^2$ y $v = e^x$

$u' = 2x$ y $v' = e^x$

Por tanto: $f'(x) = 2x \cdot e^x + x^2 \cdot e^x = e^x(2x + x^2)$

\textbf{Respuesta:} $f'(x) = e^x(2x + x^2)$
\end{solucion}
\end{ejercicio}
```

### 3.3 Problema de Física

**Archivo:** `ejercicios/fisica/cinematica_cin_001.tex`

```latex
\begin{ejercicio}[
  id=FIS_CIN_001,
  materia=fisica,
  capitulo=cinematica,
  nivel=basico,
  procedencia="Examen CEPRE 2023",
  visibilidad=true,
  libros={fisica_basica}
]
Un auto parte del reposo y acelera uniformemente a $2 \, m/s^2$. 
¿Qué distancia recorre en 10 segundos?

\begin{solucion}
Usando la ecuación: $d = v_0 t + \frac{1}{2} a t^2$

Donde:
- $v_0 = 0$ (parte del reposo)
- $a = 2 \, m/s^2$
- $t = 10 \, s$

$d = 0 \cdot 10 + \frac{1}{2} \cdot 2 \cdot 10^2 = 100 \, m$

\textbf{Respuesta:} 100 metros
\end{solucion}
\end{ejercicio}
```

---

## 🔄 **PASO 4: CONVERTIR A JSON**

### 4.1 Ejecutar el exportador
```bash
python exportador/exportar_json.py
```

### 4.2 Verificar que se generaron los archivos
```
etiquetas/
├── algebra.json          ← Problemas de álgebra
├── calculo.json          ← Problemas de cálculo
├── fisica.json           ← Problemas de física
├── metadata_ejercicios.json  ← Índice general
└── todos_ejercicios.json     ← Todos los problemas
```

### 4.3 Verificar el resultado
```bash
python demo.py
```

---

## 🌐 **PASO 5: VER EN LA WEB**

### 5.1 Abrir el componente web
- Abre el archivo: `frontend/componente_ejercicio.html`
- Se cargará automáticamente el primer ejercicio

### 5.2 Personalizar el ejercicio mostrado
Edita las líneas 280-290 en `componente_ejercicio.html`:

```javascript
const ejercicioData = {
    id: "TU_NUEVO_ID",
    materia: "tu_materia",
    capitulo: "tu_capitulo",
    nivel: "tu_nivel",
    procedencia: "Tu procedencia",
    visibilidad: true,
    libros: ["tu_libro"],
    enunciado: "Tu enunciado...",
    solucion: "Tu solución..."
};
```

---

## 📚 **PASO 6: INCLUIR EN LIBROS**

### 6.1 Editar un libro existente
Abre `libros/algebra_pre.tex` y añade tu ejercicio:

```latex
% Tu nuevo ejercicio
\begin{ejercicio}[ALG_EXP_003]
Calcula el valor de: $3^2 \cdot 3^3$

\begin{solucion}
Aplicando la propiedad de exponentes...
\end{solucion}
\end{ejercicio}
```

### 6.2 Compilar el libro
```bash
pdflatex libros/algebra_pre.tex
```

---

## 📝 **PASO 7: GENERAR SIMULACROS**

### 7.1 Crear simulacro con tus problemas
```bash
python simulacros/generador_simulacro.py --titulo "Mi Simulacro" --materia algebra --nivel basico --cantidad 5
```

### 7.2 Opciones disponibles
- `--materia`: algebra, calculo, fisica, etc.
- `--nivel`: basico, intermedio, avanzado
- `--capitulo`: exponentes, derivadas, etc.
- `--cantidad`: número de problemas
- `--formato`: latex o json

---

## ⚠️ **REGLAS IMPORTANTES**

### ✅ **HACER:**
- Usar IDs únicos (ej: `ALG_EXP_003`)
- Incluir TODOS los metadatos obligatorios
- Usar LaTeX para matemáticas: `$x^2$`, `$$\frac{a}{b}$$`
- Probar el exportador después de cada problema
- Mantener consistencia en el formato

### ❌ **NO HACER:**
- Usar IDs duplicados
- Olvidar metadatos obligatorios
- Usar caracteres especiales en IDs
- Modificar archivos JSON manualmente
- Usar espacios en nombres de archivos

---

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### Problema: "Error al exportar"
**Solución:** Verifica que el formato LaTeX sea correcto

### Problema: "No aparece en la web"
**Solución:** Verifica que `visibilidad=true`

### Problema: "Error de sintaxis"
**Solución:** Revisa que no falten llaves `{}` o corchetes `[]`

### Problema: "ID duplicado"
**Solución:** Cambia el ID por uno único

---

## 📊 **ESTRUCTURA DE IDS RECOMENDADA**

### **Formato 3 dígitos (hasta 999 problemas por capítulo):**
| Materia | Prefijo | Ejemplo |
|---------|---------|---------|
| Álgebra | `ALG` | `ALG_EXP_001` |
| Cálculo | `CAL` | `CAL_DER_001` |
| Física | `FIS` | `FIS_CIN_001` |
| Química | `QUI` | `QUI_EST_001` |
| Biología | `BIO` | `BIO_CEL_001` |
| Lenguaje | `LEN` | `LEN_GRAM_001` |

### **Formato 4 dígitos (hasta 9,999 problemas por capítulo):**
| Materia | Prefijo | Ejemplo |
|---------|---------|---------|
| Álgebra | `ALG` | `ALG_EXP_0001` |
| Cálculo | `CAL` | `CAL_DER_0001` |
| Física | `FIS` | `FIS_CIN_0001` |
| Química | `QUI` | `QUI_EST_0001` |
| Biología | `BIO` | `BIO_CEL_0001` |
| Lenguaje | `LEN` | `LEN_GRAM_0001` |

**¿Cuál elegir?**
- **3 dígitos:** Para proyectos pequeños (hasta 999 problemas por capítulo)
- **4 dígitos:** Para proyectos grandes (hasta 9,999 problemas por capítulo)
- **El script automático te permite elegir al crear cada problema**

---

## 🎯 **CHECKLIST PARA CADA PROBLEMA**

- [ ] ID único y bien formateado
- [ ] Todos los metadatos completos
- [ ] Enunciado claro y completo
- [ ] Solución detallada paso a paso
- [ ] Archivo guardado en la ubicación correcta
- [ ] Exportador ejecutado sin errores
- [ ] Problema visible en la web
- [ ] Incluido en libros (si aplica)

---

## 🚀 **PRÓXIMOS PASOS**

1. **Crea tu primer problema** siguiendo esta guía
2. **Ejecuta el exportador** para convertirlo
3. **Verifica en la web** que se vea correctamente
4. **Genera un simulacro** con tu problema
5. **¡Repite el proceso!** 

---

**¿Necesitas ayuda?** Revisa los ejemplos en `ejercicios/` o ejecuta `python demo.py` para ver el sistema en acción. 