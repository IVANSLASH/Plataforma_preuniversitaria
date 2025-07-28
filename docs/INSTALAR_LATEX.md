# 📄 GUÍA DE INSTALACIÓN DE LATEX - Para compilar `algebra_pre.tex`

## 🎯 **¿Qué necesitas instalar?**

Para ver tu documento `algebra_pre.tex` en tiempo real como PDF, necesitas instalar un **compilador de LaTeX**.

---

## 🖥️ **INSTALACIÓN POR SISTEMA OPERATIVO**

### **Windows (RECOMENDADO)**

#### **Opción 1: MiKTeX (Más fácil)**
1. **Descargar:** https://miktex.org/download
2. **Instalar:** Ejecutar el instalador como administrador
3. **Verificar:** Abrir PowerShell y escribir `pdflatex --version`

#### **Opción 2: TeX Live**
1. **Descargar:** https://www.tug.org/texlive/
2. **Instalar:** Ejecutar `install-tl-windows.exe`
3. **Tiempo:** ~30 minutos (descarga completa)

### **macOS**

#### **Opción 1: MacTeX (Recomendado)**
1. **Descargar:** https://www.tug.org/mactex/
2. **Instalar:** Arrastrar a Applications
3. **Tamaño:** ~4 GB (completo)

#### **Opción 2: BasicTeX (Ligero)**
```bash
# En Terminal
sudo tlmgr update --self
sudo tlmgr install basictex
```

### **Linux (Ubuntu/Debian)**
```bash
sudo apt-get update
sudo apt-get install texlive-full
sudo apt-get install texlive-latex-extra
sudo apt-get install texlive-fonts-recommended
```

---

## 🚀 **COMPILACIÓN AUTOMÁTICA**

### **Paso 1: Verificar instalación**
```bash
python compilar_libro.py
```

### **Paso 2: Compilar manualmente**
```bash
# Navegar a la carpeta libros
cd libros

# Compilar
pdflatex algebra_pre.tex

# Segunda compilación (para referencias)
pdflatex algebra_pre.tex
```

---

## 📋 **PAQUETES REQUERIDOS**

Tu documento `algebra_pre.tex` usa estos paquetes:

```latex
\documentclass[12pt,a4paper]{book}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{fancyhdr}
\usepackage{titlesec}
```

**Todos vienen incluidos** en las instalaciones completas de LaTeX.

---

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### **Error: "pdflatex no encontrado"**
```bash
# Windows: Reiniciar PowerShell después de instalar
# macOS: Agregar /Library/TeX/texbin al PATH
# Linux: sudo apt-get install texlive-latex-base
```

### **Error: "Package not found"**
```bash
# MiKTeX: Package Manager → Refresh FNDB
# TeX Live: sudo tlmgr update --self
# MacTeX: sudo tlmgr update --self
```

### **Error: "Font not found"**
```bash
# Instalar paquetes de fuentes
sudo tlmgr install collection-fontsrecommended
```

---

## 📊 **COMPARACIÓN DE INSTALADORES**

| Característica | MiKTeX | TeX Live | MacTeX |
|----------------|--------|----------|--------|
| **Tamaño** | ~200 MB | ~4 GB | ~4 GB |
| **Velocidad** | Rápida | Media | Media |
| **Actualizaciones** | Automáticas | Manuales | Manuales |
| **Recomendado para** | Windows | Linux | macOS |

---

## 🎯 **VERIFICACIÓN RÁPIDA**

### **Test 1: Verificar LaTeX**
```bash
pdflatex --version
```
**Debe mostrar:** versión de LaTeX

### **Test 2: Compilar documento**
```bash
python compilar_libro.py
```
**Debe generar:** `libros/algebra_pre.pdf`

### **Test 3: Ver PDF**
- Abrir: `libros/algebra_pre.pdf`
- Debe mostrar: Documento con matemáticas

---

## 📚 **EDITORES RECOMENDADOS**

### **Para editar LaTeX en tiempo real:**

#### **Visual Studio Code**
1. Instalar extensión "LaTeX Workshop"
2. Configurar compilación automática
3. Vista previa en tiempo real

#### **Overleaf (Online)**
1. Ir a: https://overleaf.com
2. Subir tu archivo `algebra_pre.tex`
3. Compilación automática

#### **TeXstudio**
1. Descargar: https://www.texstudio.org/
2. Editor dedicado para LaTeX
3. Vista previa integrada

---

## 🚀 **PRÓXIMOS PASOS**

1. ✅ **Instalar LaTeX** (esta guía)
2. 🔄 **Compilar:** `python compilar_libro.py`
3. 📖 **Editar:** Modificar `libros/algebra_pre.tex`
4. 🔄 **Recompilar:** Ver cambios en tiempo real
5. 📤 **Exportar:** PDF listo para imprimir

---

## 💡 **CONSEJOS ÚTILES**

### **Compilación rápida:**
```bash
# En la carpeta libros
pdflatex -interaction=nonstopmode algebra_pre.tex
```

### **Limpiar archivos temporales:**
```bash
# Eliminar archivos .aux, .log, .out
del *.aux *.log *.out *.toc
```

### **Vista previa automática:**
- Usar VS Code + LaTeX Workshop
- Configurar compilación al guardar
- Vista previa en tiempo real

---

**¿Necesitas ayuda?** Ejecuta `python compilar_libro.py` y sigue las instrucciones. 