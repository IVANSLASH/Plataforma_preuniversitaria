# 🔧 Solución: Error al procesar la autenticación con Google

## ⚡ Solución Rápida (2 minutos)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar credenciales automáticamente
python3 configurar_oauth.py

# 3. Probar aplicación
python app.py
```

## 📋 Qué Necesitas Hacer

### 1. **Configurar Google Cloud Console** (5 minutos)

1. Ir a: https://console.cloud.google.com/
2. Crear proyecto nuevo: "Plataforma Preuniversitaria"
3. Ir a **APIs y servicios** → **Credenciales**
4. **Crear credenciales** → **ID de cliente OAuth 2.0**
5. Tipo: **Aplicación web**
6. **URIs de redirección autorizadas**:
   ```
   http://localhost:5000/auth/google/callback
   ```
7. **Copiar** el Client ID y Client Secret

### 2. **Configurar Variables de Entorno**

**Opción A: Usar script automático**
```bash
python3 configurar_oauth.py
```

**Opción B: Configurar manualmente**
```bash
export GOOGLE_CLIENT_ID='tu_client_id_aqui'
export GOOGLE_CLIENT_SECRET='tu_client_secret_aqui'
```

### 3. **Probar que Funciona**

```bash
# Verificar configuración
python3 diagnosticar_google_oauth.py

# Si todo está OK, iniciar aplicación
python app.py

# Ir a: http://localhost:5000/auth/login
# Hacer clic en "Continuar con Google"
```

## 🚨 Error Más Común

**Error**: "redirect_uri_mismatch"

**Solución**: En Google Cloud Console, agregar **exactamente**:
```
http://localhost:5000/auth/google/callback
```

## 📞 Si Aún No Funciona

1. **Ejecutar diagnóstico**:
   ```bash
   python3 diagnosticar_google_oauth.py
   ```

2. **Revisar logs detallados**: 
   Los errores aparecen en la consola cuando ejecutas `python app.py`

3. **Verificar dependencias**:
   ```bash
   pip list | grep google
   pip list | grep flask
   ```

## ✅ Debería Ver Esto Si Funciona

**En el diagnóstico**:
```
✅ Todas las dependencias están instaladas
✅ GOOGLE_CLIENT_ID configurado correctamente  
✅ GOOGLE_CLIENT_SECRET configurado correctamente
✅ Flujo OAuth creado exitosamente
🎉 DIAGNÓSTICO EXITOSO
```

**Al hacer clic en "Continuar con Google"**:
- Redirige a Google
- Pide permisos
- Regresa a tu aplicación
- Muestra formulario para completar perfil académico

## 🔗 Archivos de Ayuda Creados

- `SOLUCION_GOOGLE_OAUTH.md` - Guía detallada completa
- `diagnosticar_google_oauth.py` - Script de diagnóstico
- `configurar_oauth.py` - Configuración automática
- `google_oauth_fixed.py` - Versión mejorada con mejor manejo de errores

## 💡 Lo Que Se Arregló

1. ✅ **Manejo de errores mejorado** - Mensajes más claros
2. ✅ **Logging detallado** - Para identificar problemas específicos  
3. ✅ **Validaciones robustas** - Verificación de configuración
4. ✅ **Scripts de diagnóstico** - Para identificar problemas rápidamente
5. ✅ **Guías paso a paso** - Para configuración correcta

El sistema de Google OAuth ahora es mucho más robusto y fácil de diagnosticar. 🚀