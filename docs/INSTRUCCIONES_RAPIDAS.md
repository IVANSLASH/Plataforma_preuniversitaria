# ⚡ INSTRUCCIONES RÁPIDAS - Empezar en 5 minutos

## 🚀 **INICIO SUPER RÁPIDO**

### 0. **Instalar requerimientos (PRIMERA VEZ)**
```bash
# Opción automática (recomendada)
python instalar_requerimientos.py

# O manualmente
pip install -r requirements_minimos.txt
```

### 1. **Crear tu primer problema (automático)**
```bash
python crear_primer_problema.py
```
**¡Sigue las instrucciones en pantalla!**

### 2. **Crear problema manualmente**
1. Copia `plantillas/plantilla_ejercicio.tex`
2. Guárdalo como `ejercicios/algebra/mi_problema_001.tex`
3. Modifica el contenido
4. Ejecuta: `python exportador/exportar_json.py`

### 3. **Ver el resultado**
- Abre: `frontend/componente_ejercicio.html`
- Ejecuta: `python demo.py`

---

## 📝 **FORMATO OBLIGATORIO**

```latex
\begin{ejercicio}[
  id=ALG_EXP_001,           ← ÚNICO
  materia=algebra,          ← OBLIGATORIO
  capitulo=exponentes,      ← OBLIGATORIO
  nivel=basico,             ← OBLIGATORIO
  procedencia="Origen",     ← OBLIGATORIO
  visibilidad=true,         ← OBLIGATORIO
  libros={libro1, libro2}   ← OPCIONAL
]
[ENUNCIADO]

\begin{solucion}
[SOLUCIÓN]
\end{solucion}
\end{ejercicio}
```

---

## 🔧 **COMANDOS ESENCIALES**

| Acción | Comando |
|--------|---------|
| Crear problema automático | `python crear_primer_problema.py` |
| Exportar a JSON | `python exportador/exportar_json.py` |
| Ver demo | `python demo.py` |
| Generar simulacro | `python simulacros/generador_simulacro.py --titulo "Mi Simulacro" --materia algebra` |
| Ver en web | Abrir `frontend/componente_ejercicio.html` |

---

## 📁 **ESTRUCTURA DE ARCHIVOS**

```
ejercicios/
├── algebra/
│   ├── exponentes_exp_001.tex
│   └── polinomios_pol_001.tex
├── calculo/
│   └── derivadas_der_001.tex
└── fisica/
    └── cinematica_cin_001.tex
```

---

## 🆔 **SISTEMA DE IDs**

### **Formato 3 dígitos (recomendado para proyectos pequeños):**
| Materia | Formato | Ejemplo |
|---------|---------|---------|
| Álgebra | `ALG_[CAP]_[NUM]` | `ALG_EXP_001` |
| Cálculo | `CAL_[CAP]_[NUM]` | `CAL_DER_001` |
| Física | `FIS_[CAP]_[NUM]` | `FIS_CIN_001` |

### **Formato 4 dígitos (recomendado para proyectos grandes):**
| Materia | Formato | Ejemplo |
|---------|---------|---------|
| Álgebra | `ALG_[CAP]_[NUM]` | `ALG_EXP_0001` |
| Cálculo | `CAL_[CAP]_[NUM]` | `CAL_DER_0001` |
| Física | `FIS_[CAP]_[NUM]` | `FIS_CIN_0001` |

**Ventajas de 4 dígitos:**
- Hasta 9,999 problemas por capítulo
- Mejor organización para proyectos grandes
- Más profesional

---

## ⚠️ **REGLAS CLAVE**

### ✅ **HACER:**
- Usar IDs únicos
- Incluir todos los metadatos
- Usar LaTeX para matemáticas: `$x^2$`, `$$\frac{a}{b}$$`
- Probar después de crear

### ❌ **NO HACER:**
- IDs duplicados
- Olvidar metadatos
- Modificar JSON manualmente
- Espacios en nombres de archivos

---

## 🆘 **SOLUCIÓN DE PROBLEMAS**

| Problema | Solución |
|----------|----------|
| "Error al exportar" | Verificar formato LaTeX |
| "No aparece en web" | Verificar `visibilidad=true` |
| "ID duplicado" | Cambiar ID |
| "Error de sintaxis" | Revisar llaves `{}` |

---

## 📚 **RECURSOS ADICIONALES**

- **Guía completa:** `GUIA_INCORPORAR_PROBLEMAS.md`
- **Plantilla:** `plantillas/plantilla_ejercicio.tex`
- **Comandos LaTeX:** `plantillas/comandos_latex_utiles.md`
- **Ejemplos:** `ejercicios/` (carpeta)

---

## 🎯 **CHECKLIST RÁPIDO**

- [ ] ID único
- [ ] Metadatos completos
- [ ] Enunciado claro
- [ ] Solución detallada
- [ ] Archivo en ubicación correcta
- [ ] Exportador ejecutado
- [ ] Verificado en web

---

**¡Listo! Ya puedes empezar a crear problemas. 🎉** 