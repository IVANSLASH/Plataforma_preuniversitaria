# Actualización de Nombres de Materias

## Resumen de Cambios

Se ha actualizado todo el proyecto para mostrar los nombres completos y descriptivos de las materias en lugar de los códigos abreviados (FISU, MATU, etc.) en la interfaz de usuario.

## Cambios Realizados

### 1. Archivo Principal (`app.py`)

- **Agregada función `obtener_nombre_materia()`**: Obtiene el nombre completo de una materia por su código
- **Actualizada función `cargar_ejercicios()`**: Agrega el campo `nombre_materia` a cada ejercicio
- **Actualizada función `cargar_metadatos()`**: Incluye `materias_nombres` con los nombres completos para los filtros

### 2. Templates Actualizados

#### `templates/index.html`
- **Filtro de materias**: Ahora muestra "Matemáticas Preuniversitaria" en lugar de "MATU"
- **Lista de ejercicios**: Muestra el nombre completo de la materia en lugar del código

#### `templates/ejercicio_detalle.html`
- **Breadcrumb**: Muestra el nombre completo de la materia
- **Información del ejercicio**: Muestra el nombre completo de la materia

#### `templates/simulacro.html`
- **Selector de materias**: Muestra los nombres completos en las opciones de radio

#### `templates/estadisticas.html`
- **Gráfico de materias**: Muestra los nombres completos en las etiquetas

### 3. Exportador (`exportador/exportar_json_nuevo.py`)

- **Agregado mapeo de nombres**: `nombres_materias` con los nombres completos
- **Actualizado procesamiento**: Incluye `nombre_materia` en cada ejercicio exportado
- **Actualizado metadatos**: Incluye `materias_nombres` en los metadatos

### 4. Archivos JSON Regenerados

Los archivos JSON ahora incluyen:
- Campo `nombre_materia` en cada ejercicio
- Sección `materias_nombres` en los metadatos

### 5. Documentación Actualizada

- **`docs/CODIGOS_MATERIAS.md`**: Agregada nota sobre el uso interno de códigos
- **`INSTRUCCIONES_SERVIDOR.md`**: Actualizadas las referencias para clarificar que se muestran nombres completos

## Mapeo de Códigos a Nombres

| Código | Nombre Completo |
|--------|----------------|
| MATU   | Matemáticas Preuniversitaria |
| FISU   | Física Preuniversitaria |
| QUIM   | Química Preuniversitaria |
| LENG   | Lenguaje y Literatura |
| CAL2   | Cálculo 2 |
| ALGN   | Álgebra Lineal |
| FIS1   | Física 1 |
| FIS2   | Física 2 |
| HIST   | Historia |
| EDIF   | Ecuaciones Diferenciales |

## Beneficios de los Cambios

1. **Mejor experiencia de usuario**: Los usuarios ven nombres descriptivos en lugar de códigos
2. **Mantenimiento de compatibilidad**: Los códigos siguen usándose internamente
3. **Consistencia**: Todos los templates muestran los mismos nombres
4. **Escalabilidad**: Fácil agregar nuevas materias con sus nombres completos

## Notas Técnicas

- Los códigos de materia (FISU, MATU, etc.) se mantienen para:
  - Organización de archivos
  - Identificación interna
  - Compatibilidad con sistemas existentes
- Los nombres completos se usan únicamente para la interfaz de usuario
- El sistema es retrocompatible con archivos JSON existentes

## Verificación

Para verificar que los cambios funcionan correctamente:

1. Ejecutar el exportador: `python exportador/exportar_json_nuevo.py`
2. Iniciar el servidor: `python app.py`
3. Verificar que en la interfaz web se muestren los nombres completos de las materias
4. Comprobar que los filtros funcionen correctamente con los nombres completos

## Archivos Modificados

- `app.py`
- `templates/index.html`
- `templates/ejercicio_detalle.html`
- `templates/simulacro.html`
- `templates/estadisticas.html`
- `exportador/exportar_json_nuevo.py`
- `docs/CODIGOS_MATERIAS.md`
- `INSTRUCCIONES_SERVIDOR.md`
- `etiquetas/todos_ejercicios_nuevo.json` (regenerado)
- `etiquetas/metadata_ejercicios_nuevo.json` (regenerado) 