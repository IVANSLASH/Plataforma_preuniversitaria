# Solución: Error al procesar la autenticación con Google

## 🔍 Problema Identificado

El diagnóstico ha encontrado los siguientes problemas:

1. **❌ Dependencias faltantes**: Librerías de Flask y Google OAuth no instaladas
2. **❌ Variables de entorno**: GOOGLE_CLIENT_ID y GOOGLE_CLIENT_SECRET no configuradas

## 🔧 Solución Paso a Paso

### Paso 1: Instalar Dependencias

```bash
pip install flask flask-login flask-sqlalchemy
pip install google-auth google-auth-oauthlib google-auth-httplib2
```

O instalar todas las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

### Paso 2: Configurar Google Cloud Console

1. **Ir a Google Cloud Console**: https://console.cloud.google.com/

2. **Crear un proyecto** (si no tienes uno):
   - Hacer clic en "Seleccionar proyecto" → "Proyecto nuevo"
   - Nombre: "Plataforma Preuniversitaria" (o el que prefieras)
   - Crear

3. **Habilitar APIs necesarias**:
   - Ir a "APIs y servicios" → "Biblioteca"
   - Buscar "Google+ API" → Habilitar
   - Buscar "Google Identity" → Habilitar (si está disponible)

4. **Crear credenciales OAuth 2.0**:
   - Ir a "APIs y servicios" → "Credenciales"
   - Hacer clic en "Crear credenciales" → "ID de cliente de OAuth 2.0"
   - Tipo de aplicación: "Aplicación web"
   - Nombre: "Plataforma Preuniversitaria"
   
   **URIs de redirección autorizadas** (agregar ambas):
   ```
   http://localhost:5000/auth/google/callback
   http://127.0.0.1:5000/auth/google/callback
   ```

5. **Obtener credenciales**:
   - Copiar el "ID de cliente"
   - Copiar el "Secreto del cliente"

### Paso 3: Configurar Variables de Entorno

**Opción A: Usando terminal (temporal)**
```bash
export GOOGLE_CLIENT_ID='tu_client_id_aqui'
export GOOGLE_CLIENT_SECRET='tu_client_secret_aqui'
```

**Opción B: Crear archivo .env (recomendado)**
```bash
# Crear archivo .env en la raíz del proyecto
echo "GOOGLE_CLIENT_ID=tu_client_id_aqui" > .env
echo "GOOGLE_CLIENT_SECRET=tu_client_secret_aqui" >> .env
```

Luego instalar python-dotenv:
```bash
pip install python-dotenv
```

Y agregar al inicio de `app.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

### Paso 4: Verificar Configuración

Ejecutar el diagnóstico nuevamente:
```bash
python3 diagnosticar_google_oauth.py
```

Debería mostrar:
```
✅ Todas las dependencias están instaladas
✅ GOOGLE_CLIENT_ID configurado correctamente
✅ GOOGLE_CLIENT_SECRET configurado correctamente
✅ Flujo OAuth creado exitosamente
```

### Paso 5: Probar la Aplicación

1. **Iniciar el servidor**:
   ```bash
   python app.py
   ```

2. **Abrir navegador**:
   - Ir a: http://localhost:5000/auth/login

3. **Probar Google OAuth**:
   - Hacer clic en "Continuar con Google"
   - Debería redirigir a Google para autenticación

## 🚨 Errores Comunes y Soluciones

### Error: "redirect_uri_mismatch"
**Problema**: La URL de callback no coincide con la configurada en Google Console.
**Solución**: Verificar que en Google Console esté configurada exactamente:
- `http://localhost:5000/auth/google/callback`

### Error: "invalid_client"
**Problema**: CLIENT_ID o CLIENT_SECRET incorrectos.
**Solución**: Verificar que las credenciales sean exactas (sin espacios extra).

### Error: "access_denied"
**Problema**: Usuario canceló la autorización.
**Solución**: Normal, el usuario debe intentar nuevamente.

### Error: "invalid_request"
**Problema**: Falta algún parámetro en la solicitud OAuth.
**Solución**: Verificar que el flujo OAuth esté correctamente configurado.

## 🧪 Script de Verificación Rápida

Crear un archivo `test_oauth.py`:

```python
#!/usr/bin/env python3
import os
from google_oauth import get_google_auth_url, check_google_oauth_config

def test_oauth():
    print("🧪 PRUEBA RÁPIDA DE OAUTH")
    print("-" * 30)
    
    # Verificar configuración
    config_ok, issues = check_google_oauth_config()
    if not config_ok:
        print("❌ Configuración inválida:")
        for issue in issues:
            print(f"   {issue}")
        return False
    
    # Generar URL de autorización
    auth_url = get_google_auth_url()
    if auth_url:
        print("✅ URL de autorización generada:")
        print(f"   {auth_url[:80]}...")
        return True
    else:
        print("❌ No se pudo generar URL de autorización")
        return False

if __name__ == "__main__":
    test_oauth()
```

Ejecutar:
```bash
python3 test_oauth.py
```

## 📋 Checklist Final

Antes de reportar que sigue fallando, verificar:

- [ ] ✅ Dependencias instaladas (`pip list | grep google`)
- [ ] ✅ Variables de entorno configuradas (`echo $GOOGLE_CLIENT_ID`)
- [ ] ✅ Proyecto creado en Google Cloud Console
- [ ] ✅ OAuth 2.0 credentials creadas
- [ ] ✅ URIs de callback correctas en Google Console
- [ ] ✅ APIs habilitadas (Google+ API)
- [ ] ✅ Diagnóstico pasa sin errores
- [ ] ✅ Aplicación inicia sin errores
- [ ] ✅ URL http://localhost:5000/auth/login carga correctamente

## 🆘 Si Sigue Fallando

Si después de seguir todos los pasos aún hay problemas:

1. **Ejecutar diagnóstico**: `python3 diagnosticar_google_oauth.py`
2. **Revisar logs**: Los errores detallados aparecen en la consola cuando inicias `python app.py`
3. **Verificar navegador**: Abrir herramientas de desarrollador (F12) y revisar errores
4. **Probar URL directa**: Ir a http://localhost:5000/auth/google/login directamente

## 📞 Información de Contacto para Soporte

Si necesitas ayuda adicional, proporciona:
- Resultado completo del diagnóstico
- Logs de error específicos
- Versión de Python (`python --version`)
- Sistema operativo