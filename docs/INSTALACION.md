# 🚀 GUÍA DE INSTALACIÓN - Plataforma Preuniversitaria

## 📋 **INFORMACIÓN DEL PROYECTO**

**Plataforma Preuniversitaria** es una aplicación web Flask completa que proporciona:
- 🎯 Sistema de ejercicios matemáticos y físicos con LaTeX
- 👤 Autenticación exclusiva con Google OAuth
- 💎 Sistema de suscripciones Premium
- 📊 Simulacros de examen personalizables
- 📚 Sistema de teoría y formularios descargables
- 🛡️ Límites diarios para uso gratuito
- 👨‍💼 Panel de administración completo

---

## 🛠️ **REQUISITOS PREVIOS**

### **Sistema Operativo**
- ✅ **Windows** (10, 11)
- ✅ **macOS** (10.14+)
- ✅ **Linux** (Ubuntu 18.04+, CentOS 7+)

### **Python**
- ✅ **Versión:** Python 3.8 o superior
- ✅ **Verificar:** `python --version` o `python3 --version`
- ❌ **No compatible:** Python 2.x

### **pip (Gestor de Paquetes)**
- ✅ **Incluido** con Python 3.4+
- ✅ **Verificar:** `pip --version`
- 🔄 **Actualizar:** `pip install --upgrade pip`

### **Git (Opcional pero recomendado)**
- ✅ Para clonar el repositorio
- ✅ **Descargar:** [git-scm.com](https://git-scm.com/)

---

## 📦 **INSTALACIÓN PASO A PASO**

### **Paso 1: Obtener el código**

#### Opción A: Clonar repositorio (Git)
```bash
git clone https://github.com/usuario/plataforma-preuniversitaria.git
cd plataforma-preuniversitaria
```

#### Opción B: Descargar ZIP
1. Descargar ZIP del repositorio
2. Extraer en carpeta de trabajo
3. Abrir terminal en esa carpeta

### **Paso 2: Crear entorno virtual (RECOMENDADO)**
```bash
# Crear entorno virtual
python -m venv plataforma_env

# Activar entorno virtual
# Windows:
plataforma_env\Scripts\activate
# macOS/Linux:
source plataforma_env/bin/activate
```

### **Paso 3: Instalar dependencias**
```bash
# Instalar todas las dependencias necesarias
pip install -r requirements.txt
```

**Dependencias principales instaladas:**
- `Flask==2.3.3` - Framework web
- `Flask-Login==0.6.3` - Sistema de autenticación
- `Flask-SQLAlchemy==3.0.5` - ORM base de datos
- `Authlib>=1.2.0` - Cliente OAuth para Google
- `ReportLab>=4.0.0` - Generación de PDFs
- `requests>=2.28.0` - Cliente HTTP

### **Paso 4: Configurar variables de entorno**

#### Crear archivo `.env`
```bash
# Crear archivo .env en la raíz del proyecto
touch .env
```

#### Contenido del archivo `.env`:
```bash
# Configuración Flask
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura_aqui_cambiala
FLASK_ENV=development

# Base de datos
DATABASE_URL=sqlite:///plataforma.db

# Google OAuth (OBLIGATORIO)
GOOGLE_CLIENT_ID=tu_client_id_de_google_oauth.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu_client_secret_de_google_oauth

# Configuración opcional
LOG_LEVEL=INFO
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_app_password
```

### **Paso 5: Configurar Google OAuth**

#### 5.1 Crear proyecto en Google Cloud Console
1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear nuevo proyecto o seleccionar existente
3. Habilitar "Google+ API" y "Gmail API"

#### 5.2 Configurar OAuth Credentials
1. Ir a "Credentials" > "Create Credentials" > "OAuth 2.0 Client ID"
2. Tipo: "Web application"
3. Agregar URIs autorizadas:
   - **Development:** `http://localhost:5000/auth/authorize`
   - **Production:** `https://tu-dominio.com/auth/authorize`
4. Copiar Client ID y Client Secret al archivo `.env`

### **Paso 6: Inicializar base de datos**
```bash
# La base de datos se inicializa automáticamente al ejecutar la aplicación
python app.py
```

---

## ⚡ **EJECUCIÓN RÁPIDA**

### **Desarrollo**
```bash
# Activar entorno virtual (si no está activo)
source plataforma_env/bin/activate  # macOS/Linux
# plataforma_env\Scripts\activate   # Windows

# Ejecutar aplicación
python app.py
```

**Aplicación disponible en:** http://localhost:5000

### **Producción**
```bash
# Usar servidor WSGI como Gunicorn
pip install gunicorn

# Ejecutar con Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 🔧 **CONFIGURACIÓN AVANZADA**

### **Base de Datos (PostgreSQL)**
Para producción, se recomienda usar PostgreSQL:

```bash
# Instalar adaptador PostgreSQL
pip install psycopg2-binary

# Actualizar DATABASE_URL en .env
DATABASE_URL=postgresql://usuario:password@localhost:5432/plataforma_db
```

### **Configuración de Email**
Para funciones como notificaciones y recuperación:

```bash
# En .env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_app_password  # No tu contraseña normal
```

### **Configuración SSL/HTTPS**
```bash
# En .env para producción
FLASK_ENV=production
SESSION_COOKIE_SECURE=True
```

---

## 🧪 **VERIFICACIÓN DE INSTALACIÓN**

### **Test 1: Verificar dependencias**
```bash
python -c "import flask; print('Flask OK')"
python -c "import flask_login; print('Flask-Login OK')"
python -c "import flask_sqlalchemy; print('SQLAlchemy OK')"
python -c "import authlib; print('Authlib OK')"
```

### **Test 2: Verificar aplicación**
```bash
python app.py
```
**Debe mostrar:**
```
🚀 Iniciando servidor de ejercicios preuniversitarios...
✅ Base de datos inicializada con X usuarios
🌐 Servidor iniciado en: http://localhost:5000
```

### **Test 3: Verificar autenticación**
1. Ir a http://localhost:5000
2. Hacer clic en "Iniciar Sesión"
3. Debe redirigir a Google OAuth

---

## 📊 **ESTRUCTURA DE ARCHIVOS POST-INSTALACIÓN**

```
plataforma-preuniversitaria/
├── app.py                    # Aplicación principal Flask
├── models.py                 # Modelos de base de datos
├── auth.py                   # Sistema de autenticación OAuth
├── config.py                 # Configuraciones de la aplicación
├── requirements.txt          # Dependencias Python
├── .env                     # Variables de entorno (CREAR)

├── ejercicios_nuevo/         # Ejercicios en estructura jerárquica
│   ├── matematicas_preuniversitaria/
│   └── fisica_preuniversitaria/

├── templates/                # Templates HTML Jinja2
│   ├── base.html            # Template base con Bootstrap 5
│   ├── index.html           # Página principal
│   └── auth/                # Templates de autenticación

├── static/                   # Archivos estáticos
├── etiquetas/               # Metadatos JSON de ejercicios
├── instance/                # Base de datos SQLite
└── docs/                    # Documentación del proyecto
```

---

## 🆘 **SOLUCIÓN DE PROBLEMAS**

### **Error: "Python no encontrado"**
```bash
# Windows - Probar diferentes comandos
python --version
py --version
python3 --version

# Agregar Python al PATH si es necesario
```

### **Error: "pip no encontrado"**
```bash
# Instalar/actualizar pip
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### **Error: "Permission denied"**
```bash
# Windows - Ejecutar como administrador
# macOS/Linux - Usar sudo solo si es necesario
sudo pip install -r requirements.txt

# O mejor: usar entorno virtual
python -m venv plataforma_env
```

### **Error: "Google OAuth failed"**
1. ✅ Verificar GOOGLE_CLIENT_ID y GOOGLE_CLIENT_SECRET en `.env`
2. ✅ Verificar URIs autorizadas en Google Cloud Console
3. ✅ Verificar que las APIs estén habilitadas
4. ✅ Verificar que el dominio esté autorizado

### **Error: "Database connection failed"**
```bash
# Eliminar base de datos y recrear
rm instance/plataforma.db
python app.py
```

### **Error: "Port already in use"**
```bash
# Usar puerto diferente
export FLASK_RUN_PORT=5001
python app.py

# O matar proceso en puerto 5000
# Windows: netstat -ano | findstr :5000
# macOS/Linux: lsof -ti:5000 | xargs kill
```

### **Error: SSL Certificate**
```bash
# Usar --trusted-host para instalación
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

---

## 🔐 **CONFIGURACIÓN DE SEGURIDAD**

### **Para Producción:**
1. ✅ Cambiar `SECRET_KEY` por valor aleatorio largo
2. ✅ Usar `FLASK_ENV=production`
3. ✅ Configurar HTTPS
4. ✅ Usar base de datos externa (PostgreSQL)
5. ✅ Configurar firewall
6. ✅ Usar servidor web (Nginx + Gunicorn)

### **Variables de Entorno Críticas:**
```bash
# OBLIGATORIAS
SECRET_KEY=         # Clave de sesión Flask
GOOGLE_CLIENT_ID=   # ID de cliente OAuth
GOOGLE_CLIENT_SECRET=  # Secreto cliente OAuth

# RECOMENDADAS
DATABASE_URL=       # URL de base de datos
LOG_LEVEL=         # Nivel de logging
```

---

## 👥 **PRIMER USO - CREAR ADMINISTRADOR**

### **Automático (Email hardcodeado)**
El email `ingivanladislao@gmail.com` se convierte automáticamente en administrador.

### **Manual (Script)**
```bash
python hacer_admin.py
```

### **Desde aplicación**
1. Registrarse con Google OAuth
2. Un administrador existente puede otorgar privilegios desde el panel admin

---

## 📚 **PRÓXIMOS PASOS DESPUÉS DE INSTALACIÓN**

1. ✅ **Configurar Google OAuth** (obligatorio)
2. 🎯 **Acceder a la aplicación:** http://localhost:5000
3. 👤 **Registrarse con Google** para probar autenticación
4. 📊 **Explorar panel admin** (si eres administrador)
5. 🎓 **Revisar ejercicios disponibles**
6. 📖 **Leer documentación adicional:**
   - `INSTRUCCIONES_RAPIDAS.md` - Uso básico
   - `SISTEMA_LIMITES_DIARIOS.md` - Sistema de límites
   - `CODIGOS_MATERIAS.md` - Códigos de materias

---

## 🔗 **RECURSOS ADICIONALES**

### **Documentación**
- **Instalación:** Este archivo
- **Uso rápido:** `INSTRUCCIONES_RAPIDAS.md`
- **Códigos de materias:** `CODIGOS_MATERIAS.md`
- **Sistema de límites:** `SISTEMA_LIMITES_DIARIOS.md`

### **Scripts de Utilidad**
- `hacer_admin.py` - Convertir usuario en administrador
- `otorgar_premium.py` - Gestionar cuentas premium
- `exportador/exportar_json_nuevo.py` - Exportar ejercicios

### **Archivos de Configuración**
- `requirements.txt` - Dependencias Python
- `.env` - Variables de entorno (crear manualmente)
- `config.py` - Configuraciones de Flask

---

**¿Necesitas ayuda adicional?** 
- 📧 Contacta al administrador
- 📖 Revisa la documentación en `docs/`
- 🐛 Reporta problemas en el repositorio

**¡Listo para usar tu Plataforma Preuniversitaria! 🎉**