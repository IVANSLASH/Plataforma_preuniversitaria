# 🔧 GUÍA DE INSTALACIÓN - Plataforma Preuniversitaria

## 📋 **ARCHIVOS DE REQUERIMIENTOS**

### **1. `requirements_minimos.txt` - ARCHIVO MAESTRO PARA INICIO RÁPIDO**
```
✅ RECOMENDADO para empezar
📦 Solo dependencias esenciales (7 paquetes)
⚡ Instalación rápida (< 2 minutos)
🎯 Todo lo necesario para crear problemas
```

**Contiene:**
- `pathlib2` - Manejo de archivos
- `regex` - Procesamiento de texto
- `jsonschema` - Validación de datos
- `ijson` - Manejo de JSON
- `colorlog` - Logging con colores
- `python-dateutil` - Manejo de fechas
- `unidecode` - Procesamiento de texto Unicode

### **2. `requirements.txt` - INSTALACIÓN COMPLETA**
```
🔧 Para desarrolladores avanzados
📦 Todas las dependencias (20+ paquetes)
⏱️ Instalación más larga
🛠️ Incluye herramientas de desarrollo
```

**Incluye además:**
- Herramientas de testing (`pytest`, `pytest-cov`)
- Formateo de código (`black`, `flake8`)
- Dependencias opcionales comentadas
- Herramientas de desarrollo

### **3. `instalar_requerimientos.py` - INSTALADOR AUTOMÁTICO**
```
🤖 Script inteligente
🔍 Verifica Python y pip
📋 Menú interactivo
✅ Verifica la instalación
```

---

## 🚀 **OPCIONES DE INSTALACIÓN**

### **Opción 1: Automática (RECOMENDADA)**
```bash
python instalar_requerimientos.py
```
**Ventajas:**
- ✅ Verifica requisitos previos
- ✅ Menú interactivo
- ✅ Verifica la instalación
- ✅ Instrucciones claras

### **Opción 2: Manual - Mínima**
```bash
pip install -r requirements_minimos.txt
```
**Para usuarios que prefieren control manual**

### **Opción 3: Manual - Completa**
```bash
pip install -r requirements.txt
```
**Para desarrolladores que quieren todas las herramientas**

---

## 📋 **REQUISITOS PREVIOS**

### **Python**
- ✅ **Versión:** 3.8 o superior
- ✅ **Verificar:** `python --version`
- ❌ **No compatible:** Python 2.x

### **pip**
- ✅ **Incluido** con Python 3.4+
- ✅ **Verificar:** `pip --version`
- 🔄 **Actualizar:** `pip install --upgrade pip`

### **Sistema Operativo**
- ✅ **Windows** (10, 11)
- ✅ **macOS** (10.14+)
- ✅ **Linux** (Ubuntu 18.04+, CentOS 7+)

---

## 🔧 **PROCESO DE INSTALACIÓN DETALLADO**

### **Paso 1: Verificar Python**
```bash
python --version
```
**Debe mostrar:** Python 3.8.x o superior

### **Paso 2: Verificar pip**
```bash
pip --version
```
**Debe mostrar:** pip 20.x o superior

### **Paso 3: Instalar requerimientos**
```bash
# Opción automática
python instalar_requerimientos.py

# O manual
pip install -r requirements_minimos.txt
```

### **Paso 4: Verificar instalación**
```bash
python demo.py
```
**Debe mostrar:** "Demo completado exitosamente"

---

## 🆘 **SOLUCIÓN DE PROBLEMAS**

### **Error: "Python no encontrado"**
```bash
# Windows
python --version
# Si no funciona, prueba:
py --version

# macOS/Linux
python3 --version
```

### **Error: "pip no encontrado"**
```bash
# Instalar pip manualmente
python -m ensurepip --upgrade
```

### **Error: "Permission denied"**
```bash
# Windows (ejecutar como administrador)
pip install -r requirements_minimos.txt

# macOS/Linux
sudo pip install -r requirements_minimos.txt
```

### **Error: "SSL Certificate"**
```bash
# Usar --trusted-host
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements_minimos.txt
```

### **Error: "Microsoft Visual C++" (Windows)**
```bash
# Instalar Visual Studio Build Tools
# O usar wheels precompilados
pip install --only-binary=all -r requirements_minimos.txt
```

---

## 📊 **COMPARACIÓN DE ARCHIVOS**

| Característica | `requirements_minimos.txt` | `requirements.txt` |
|----------------|---------------------------|-------------------|
| **Tamaño** | 7 dependencias | 20+ dependencias |
| **Tiempo instalación** | < 2 minutos | 5-10 minutos |
| **Uso recomendado** | Inicio rápido | Desarrollo |
| **Espacio en disco** | ~50 MB | ~200 MB |
| **Funcionalidad** | Básica completa | Completa + desarrollo |

---

## 🎯 **VERIFICACIÓN POST-INSTALACIÓN**

### **Test 1: Verificar dependencias**
```bash
python instalar_requerimientos.py
# Elegir opción 3: "Verificar instalación actual"
```

### **Test 2: Ejecutar demo**
```bash
python demo.py
```

### **Test 3: Crear problema de prueba**
```bash
python crear_primer_problema.py
```

### **Test 4: Ver en web**
- Abrir: `frontend/componente_ejercicio.html`

---

## 📚 **PRÓXIMOS PASOS**

1. ✅ **Instalar requerimientos** (este archivo)
2. 🚀 **Crear primer problema:** `python crear_primer_problema.py`
3. 📖 **Leer guía:** `GUIA_INCORPORAR_PROBLEMAS.md`
4. 🎯 **Ver ejemplos:** `ejercicios/` (carpeta)
5. 🌐 **Personalizar web:** `frontend/componente_ejercicio.html`

---

## 🔗 **ARCHIVOS RELACIONADOS**

- **`requirements_minimos.txt`** - Dependencias esenciales
- **`requirements.txt`** - Dependencias completas
- **`instalar_requerimientos.py`** - Instalador automático
- **`GUIA_INCORPORAR_PROBLEMAS.md`** - Guía de uso
- **`INSTRUCCIONES_RAPIDAS.md`** - Resumen ejecutivo

---

**¿Necesitas ayuda?** Ejecuta `python instalar_requerimientos.py` y sigue las instrucciones en pantalla. 