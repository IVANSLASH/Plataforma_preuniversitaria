# 🎓 Plataforma Preuniversitaria - SlashDevs

Sistema educativo multiplataforma que combina:
- **Libros de matemáticas** escritos en LaTeX
- **Aplicación web interactiva** con banco de problemas
- **Sistema unificado** de gestión de ejercicios

## 📁 Estructura del Proyecto

```
plataforma_preuniversitaria/
├── libros/                    # Documentos LaTeX para libros
├── ejercicios/               # Repositorio central de problemas
├── etiquetas/               # Metadatos e índices
├── exportador/              # Scripts de conversión
├── simulacros/              # Generador de exámenes
├── api_backend/             # Backend para la web
├── frontend/                # Componentes web
└── README.md
```

## 🚀 Características Principales

### ✨ Gestión Unificada de Ejercicios
- **Un solo repositorio** para problemas de web y libros
- **Metadatos completos** en cada ejercicio
- **Filtrado dinámico** por materia, nivel, visibilidad

### 📚 Sistema de Libros
- **Múltiples libros** desde un mismo banco de problemas
- **Selección flexible** de ejercicios por libro
- **Control de visibilidad** (web vs impresión)

### 🌐 Plataforma Web
- **Problemas interactivos** con MathJax
- **Filtros avanzados** por materia y nivel
- **Sistema de progreso** del estudiante

## 🛠️ Instalación y Uso

### Requisitos
- Python 3.8+
- LaTeX (MiKTeX, TeX Live)
- Node.js (para frontend)

### Configuración Inicial
```bash
# Clonar el repositorio
git clone [url-del-repositorio]
cd plataforma_preuniversitaria

# Instalar dependencias Python
pip install -r requirements.txt

# Configurar LaTeX
# (Instalar MiKTeX o TeX Live según tu sistema)
```

### Uso Básico

1. **Crear un ejercicio:**
   ```bash
   # Editar archivo .tex en ejercicios/[materia]/
   # Ejemplo: ejercicios/algebra/exponentes_exp_001.tex
   ```

2. **Exportar a JSON:**
   ```bash
   python exportador/exportar_json.py
   ```

3. **Generar libro:**
   ```bash
   # Compilar desde libros/
   pdflatex algebra_pre.tex
   ```

4. **Crear simulacro:**
   ```bash
   python simulacros/generador_simulacro.py --materia=algebra --nivel=intermedio
   ```

## 📖 Formato de Ejercicios

Cada ejercicio debe seguir este formato LaTeX:

```latex
\begin{ejercicio}[
  id=ALG_EXP_001,
  materia=algebra,
  capitulo=exponentes,
  nivel=basico,
  procedencia="Examen 2022",
  visibilidad=true,
  libros={algebra_pre}
]
[Enunciado del problema]

\begin{solucion}
[Solución detallada]
\end{solucion}
\end{ejercicio}
```

## 🔧 Metadatos de Ejercicios

- **id**: Identificador único (ej: ALG_EXP_001)
- **materia**: Álgebra, Cálculo, Física, etc.
- **capitulo**: Tema específico (exponentes, límites, etc.)
- **nivel**: Básico, Intermedio, Avanzado
- **procedencia**: Origen del problema
- **visibilidad**: true/false (web vs impresión)
- **libros**: Lista de libros donde aparece

## 📊 Materias Soportadas

- ✅ **Matemáticas**: Álgebra, Cálculo, Geometría
- ✅ **Ciencias**: Física, Química, Biología
- ✅ **Lenguaje**: Comprensión, Gramática
- 🔄 **En desarrollo**: Historia, Filosofía

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature
3. Añade ejercicios siguiendo el formato
4. Actualiza metadatos
5. Envía un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 📞 Contacto

- **Desarrollador**: [Tu nombre]
- **Email**: [tu-email@ejemplo.com]
- **GitHub**: [tu-usuario]

---

*Desarrollado con ❤️ para la educación preuniversitaria* 

git --version
git status

# crar un commit con mensaje
git commit -m "actualizacion primer intento surface"

cargar
git push
