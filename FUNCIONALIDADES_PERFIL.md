# Funcionalidades de Perfil de Usuario

## 📝 Edición de Perfil Inline

### Características
- **Edición en la misma página**: Los usuarios pueden editar su perfil directamente en la página de perfil sin navegar a otra página
- **Campos editables**: Todos los campos del perfil son editables excepto el email y la información de cuenta
- **Validación en tiempo real**: Los campos se validan antes de guardar
- **Feedback visual**: Indicadores de carga y mensajes de éxito/error

### Campos Editables
- **Nombre Completo** (obligatorio)
- **Última Unidad Educativa**
- **Nivel Académico Actual** (con opción "Otro")
- **Ciudad**
- **WhatsApp** (con formato sugerido)
- **Carrera de Interés**
- **Intereses Académicos** (textarea)
- **Aceptar Anuncios** (checkbox)

### Funcionamiento
1. El usuario hace clic en "Editar" en la página de perfil
2. Los campos se convierten en inputs editables
3. El usuario modifica los datos deseados
4. Hace clic en "Guardar Cambios" para enviar los datos
5. Los cambios se guardan mediante AJAX sin recargar la página
6. Se muestra feedback visual del resultado

## 🗑️ Eliminación de Cuenta

### Características
- **Confirmación múltiple**: Sistema de confirmación en dos pasos para evitar eliminaciones accidentales
- **Modal informativo**: Muestra claramente qué datos se eliminarán
- **Validación por texto**: El usuario debe escribir "ELIMINAR" para confirmar
- **Eliminación completa**: Borra todos los datos del usuario y sus sesiones

### Proceso de Eliminación
1. El usuario hace clic en "Eliminar Cuenta"
2. Se muestra un modal con advertencia detallada
3. Si confirma, debe escribir "ELIMINAR" en mayúsculas
4. Se eliminan todas las sesiones del usuario
5. Se elimina la cuenta del usuario
6. Se cierra la sesión automáticamente
7. Se redirige a la página principal

### Datos Eliminados
- Cuenta de usuario completa
- Todos los datos personales
- Historial de sesiones
- Acceso a recursos de la plataforma

## 🔧 Endpoints API

### POST `/auth/update_profile`
Actualiza el perfil del usuario mediante AJAX.

**Parámetros:**
- `nombre_completo` (obligatorio)
- `ultima_unidad_educativa`
- `nivel_academico_actual`
- `nivel_academico_otro` (si se selecciona "otro")
- `ciudad`
- `whatsapp`
- `carrera_interes`
- `intereses`
- `acepta_anuncios` (checkbox)

**Respuesta:**
```json
{
  "success": true/false,
  "message": "Mensaje descriptivo"
}
```

### POST `/auth/delete_account`
Elimina la cuenta del usuario.

**Parámetros:** Ninguno

**Respuesta:**
```json
{
  "success": true/false,
  "message": "Mensaje descriptivo"
}
```

## 🎨 Mejoras de UX

### Indicadores Visuales
- **Spinner de carga**: Se muestra durante las operaciones
- **Botones deshabilitados**: Previenen múltiples envíos
- **Mensajes de feedback**: Alertas de éxito y error
- **Animaciones**: Transiciones suaves entre estados

### Validaciones
- **Campos obligatorios**: El nombre completo es obligatorio
- **Formato de WhatsApp**: Sugiere formato +591 12345678
- **Longitud de intereses**: Máximo 500 caracteres
- **Nivel académico**: Lista predefinida con opción "Otro"

### Responsive Design
- **Mobile-friendly**: Funciona bien en dispositivos móviles
- **Accesibilidad**: Controles fáciles de usar
- **Feedback táctil**: Botones con efectos hover

## 🚀 Beneficios

1. **Mejor experiencia de usuario**: Edición sin navegación
2. **Mayor seguridad**: Confirmación múltiple para eliminación
3. **Feedback inmediato**: Respuestas en tiempo real
4. **Interfaz moderna**: Diseño actualizado y responsive
5. **Funcionalidad completa**: Todas las operaciones de perfil en un lugar

## ⚠️ Consideraciones

- La eliminación de cuenta es **irreversible**
- Los usuarios de Google no pueden cambiar su contraseña desde la plataforma
- Todos los cambios se guardan automáticamente en la base de datos
- Las sesiones se eliminan completamente al borrar la cuenta 