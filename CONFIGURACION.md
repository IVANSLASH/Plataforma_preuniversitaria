# 🔧 Configuración de la Plataforma Preuniversitaria

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Cuenta de Google Cloud Platform (para OAuth)

## 🚀 Instalación y Configuración

### 1. **Clonar el repositorio**
```bash
git clone https://github.com/IVANSLASH/Plataforma_preuniversitaria.git
cd Plataforma_preuniversitaria
```

### 2. **Instalar dependencias**
```bash
python -m pip install -r requirements.txt
```

### 3. **Configurar variables de entorno**

#### Opción A: Crear archivo `.env` manualmente
Crea un archivo llamado `.env` en la raíz del proyecto con el siguiente contenido:

```env
# Configuración de la Aplicación Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=tu_clave_secreta_aqui_cambiala_en_produccion

# Configuración de Google OAuth
GOOGLE_CLIENT_ID=tu_client_id_aqui
GOOGLE_CLIENT_SECRET=tu_client_secret_aqui

# Configuración de Base de Datos
DATABASE_URL=sqlite:///plataforma.db

# Configuración del Servidor
HOST=0.0.0.0
PORT=5000
```

#### Opción B: Usar el archivo de ejemplo
```bash
cp .env.example .env
# Editar .env con tus valores reales
```

### 4. **Configurar Google OAuth**

#### Paso 1: Crear proyecto en Google Cloud Console
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de Google+ y Google OAuth2

#### Paso 2: Crear credenciales OAuth
1. Ve a **APIs & Services** > **Credentials**
2. Haz clic en **Create Credentials** > **OAuth 2.0 Client IDs**
3. Selecciona **Web application**
4. Configura las URLs autorizadas:
   - **Authorized JavaScript origins**:
     ```
     http://localhost:5000
     http://127.0.0.1:5000
     ```
   - **Authorized redirect URIs**:
     ```
     http://localhost:5000/auth/authorize
     http://127.0.0.1:5000/auth/authorize
     ```

#### Paso 3: Obtener credenciales
1. Copia el **Client ID** y **Client Secret**
2. Agrégales al archivo `.env`:
   ```env
   GOOGLE_CLIENT_ID=tu_client_id_aqui
   GOOGLE_CLIENT_SECRET=tu_client_secret_aqui
   ```

### 5. **Inicializar la base de datos**
```bash
python app.py
```
La aplicación creará automáticamente la base de datos y cargará datos de ejemplo.

### 6. **Ejecutar la aplicación**
```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 🔐 Variables de Entorno Importantes

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta para sesiones Flask | `mi_clave_secreta_123` |
| `GOOGLE_CLIENT_ID` | ID del cliente OAuth de Google | `123456789-abc...` |
| `GOOGLE_CLIENT_SECRET` | Secreto del cliente OAuth de Google | `GOCSPX-abc...` |
| `DATABASE_URL` | URL de conexión a la base de datos | `sqlite:///plataforma.db` |
| `FLASK_ENV` | Entorno de Flask | `development` o `production` |

## 🛡️ Seguridad

### ✅ Buenas Prácticas
- **Nunca** commits el archivo `.env` al repositorio
- Usa claves secretas fuertes y únicas
- Cambia las credenciales regularmente
- Usa HTTPS en producción

### ❌ Evitar
- Compartir credenciales en código
- Usar credenciales de desarrollo en producción
- Dejar credenciales en logs o mensajes de error

## 🚨 Solución de Problemas

### Error: "redirect_uri_mismatch"
- Verifica que las URLs de redirección en Google Cloud Console coincidan con tu aplicación
- Asegúrate de incluir tanto `localhost` como `127.0.0.1`

### Error: "ModuleNotFoundError"
- Instala las dependencias: `python -m pip install -r requirements.txt`
- Verifica que estés usando la versión correcta de Python

### Error: "BuildError"
- Verifica que todas las rutas estén definidas en los blueprints
- Revisa los templates por referencias incorrectas

## 📞 Soporte

Si tienes problemas con la configuración:
1. Revisa los logs de la aplicación
2. Verifica que todas las variables de entorno estén configuradas
3. Asegúrate de que Google OAuth esté configurado correctamente
4. Consulta la documentación de Flask y Google OAuth 