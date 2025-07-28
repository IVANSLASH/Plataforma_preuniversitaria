# 🚀 Instrucciones para Ejecutar el Servidor

## Método Recomendado (FÁCIL)

### 1. Activar entorno virtual
```bash
source venv/bin/activate
```

### 2. Ejecutar servidor robusto
```bash
python iniciar_servidor.py
```
- ✅ Encuentra puerto libre automáticamente
- ✅ Muestra todas las URLs de acceso
- ✅ Abre navegador automáticamente
- ✅ Funciona en red local

### 3. Acceder al sitio
- **Local**: http://localhost:5000 (o puerto mostrado)
- **Red**: http://IP_MOSTRADA:5000

## Método Alternativo

### 1. Ejecutar servidor básico
```bash
python app.py
```

### 2. Acceder
**URL**: http://localhost:5000

## 🌐 URLs disponibles

### Páginas principales:
- `/` - Ejercicios con filtros avanzados
- `/ejercicio/<id>` - Detalle de ejercicio específico  
- `/simulacro` - Generador de simulacros
- `/estadisticas` - Estadísticas detalladas
- `/libros` - Libros disponibles

### APIs:
- `/api/ejercicios` - JSON con ejercicios
- `/api/metadatos` - JSON con estadísticas  
- `/generar_simulacro` - POST para crear simulacro

## 🔍 Filtros URL soportados

```
?codigo_materia=MATU    # Por código de materia
?nivel=basico           # Por nivel
?dificultad=2           # Por dificultad 1-5
?visibilidad=web_impreso # Por visibilidad
```

## 📊 Ejemplos de uso

```
http://localhost:5000/?codigo_materia=MATU
http://localhost:5000/?nivel=basico&dificultad=2
http://localhost:5000/ejercicio/MATU_ALG_001
```

## 🛠️ Comandos útiles

### Exportar ejercicios a JSON:
```bash
python exportador/exportar_json_nuevo.py
```

### Verificar instalación:
```bash
python -c "import flask; print('✅ Flask OK')"
```

### Detener servidor:
```
Ctrl + C
```