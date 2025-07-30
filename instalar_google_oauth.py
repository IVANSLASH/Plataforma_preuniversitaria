#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Instalación - Google OAuth para Plataforma Preuniversitaria
====================================================================

Script para instalar y configurar Google OAuth en la plataforma.

Autor: Plataforma Preuniversitaria
Fecha: 2025
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header():
    """Imprime el encabezado del script"""
    print("=" * 60)
    print("🔐 INSTALADOR DE GOOGLE OAUTH")
    print("   Plataforma Preuniversitaria")
    print("=" * 60)
    print()

def check_python_version():
    """Verifica la versión de Python"""
    print("🐍 Verificando versión de Python...")
    
    if sys.version_info < (3, 7):
        print("❌ Error: Se requiere Python 3.7 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def install_dependencies():
    """Instala las dependencias necesarias"""
    print("\n📦 Instalando dependencias de Google OAuth...")
    
    dependencies = [
        'requests-oauthlib>=1.3.1',
        'google-auth>=2.17.3',
        'google-auth-oauthlib>=1.0.0',
        'google-auth-httplib2>=0.1.0'
    ]
    
    for dep in dependencies:
        try:
            print(f"   Instalando {dep}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
            print(f"   ✅ {dep} instalado correctamente")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Error instalando {dep}: {e}")
            return False
    
    return True

def create_env_file():
    """Crea el archivo .env con configuración de Google OAuth"""
    print("\n📝 Creando archivo de configuración .env...")
    
    env_content = """# Configuración de Google OAuth - Plataforma Preuniversitaria
# ============================================

# Configuración de Google OAuth
# Obtén estas credenciales desde: https://console.cloud.google.com/
GOOGLE_CLIENT_ID=tu_client_id_aqui
GOOGLE_CLIENT_SECRET=tu_client_secret_aqui

# Configuración de la aplicación
SECRET_KEY=tu_clave_secreta_muy_segura_aqui_cambiala_en_produccion
FLASK_ENV=development

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URI=sqlite:///plataforma.db
SQLALCHEMY_TRACK_MODIFICATIONS=False

# Configuración de sesiones
SESSION_COOKIE_SECURE=False  # Cambiar a True en producción con HTTPS
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# Configuración de archivos
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=static/uploads

# Configuración de logging
LOG_LEVEL=INFO

# Configuración de email (opcional)
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=True
# MAIL_USERNAME=tu_email@gmail.com
# MAIL_PASSWORD=tu_password_de_aplicacion
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Archivo .env creado correctamente")
        print("   ⚠️  Recuerda configurar tus credenciales de Google OAuth")
        return True
    except Exception as e:
        print(f"❌ Error creando archivo .env: {e}")
        return False

def create_directories():
    """Crea directorios necesarios"""
    print("\n📁 Creando directorios necesarios...")
    
    directories = [
        'templates/auth',
        'logs',
        'static/uploads',
        'static/uploads/avatars'
    ]
    
    for directory in directories:
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"   ✅ Directorio {directory} creado/verificado")
        except Exception as e:
            print(f"   ❌ Error creando directorio {directory}: {e}")
            return False
    
    return True

def update_database():
    """Actualiza la base de datos con las nuevas columnas"""
    print("\n🗄️  Actualizando base de datos...")
    
    try:
        # Importar la aplicación y modelos
        sys.path.append('.')
        from app import app
        from models import db, init_db
        
        with app.app_context():
            # Crear todas las tablas
            db.create_all()
            print("   ✅ Base de datos actualizada correctamente")
            
            # Verificar si existe el usuario admin
            from models import Usuario
            admin = Usuario.query.filter_by(username='admin').first()
            if not admin:
                print("   ⚠️  Usuario admin no encontrado, ejecuta el script principal de instalación")
            else:
                print("   ✅ Usuario admin verificado")
        
        return True
    except Exception as e:
        print(f"   ❌ Error actualizando base de datos: {e}")
        return False

def create_google_config_example():
    """Crea un archivo de ejemplo para configuración de Google"""
    print("\n📋 Creando archivo de configuración de ejemplo...")
    
    config_content = """# Ejemplo de configuración para Google Cloud Console
# ============================================

# 1. Ve a https://console.cloud.google.com/
# 2. Crea un nuevo proyecto o selecciona uno existente
# 3. Habilita la API de Google+ (si no está habilitada)
# 4. Ve a "APIs & Services" > "Credentials"
# 5. Haz clic en "Create Credentials" > "OAuth 2.0 Client IDs"
# 6. Selecciona "Web application"
# 7. Configura las URLs de redirección autorizadas:
#    - http://localhost:5000/auth/google/callback (desarrollo)
#    - https://tu-dominio.com/auth/google/callback (producción)

# Después de crear las credenciales, copia los valores al archivo .env:
# GOOGLE_CLIENT_ID=tu_client_id_aqui
# GOOGLE_CLIENT_SECRET=tu_client_secret_aqui

# Para más información, consulta: config_google_oauth.md
"""
    
    try:
        with open('google_config_ejemplo.txt', 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("✅ Archivo de ejemplo creado: google_config_ejemplo.txt")
        return True
    except Exception as e:
        print(f"❌ Error creando archivo de ejemplo: {e}")
        return False

def verify_installation():
    """Verifica que la instalación sea correcta"""
    print("\n🔍 Verificando instalación...")
    
    # Verificar archivos necesarios
    required_files = [
        'app.py',
        'models.py',
        'auth.py',
        'google_oauth.py',
        'requirements.txt'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file} encontrado")
        else:
            print(f"   ❌ {file} no encontrado")
            return False
    
    # Verificar dependencias
    try:
        import google.auth
        import google_auth_oauthlib
        import requests_oauthlib
        print("   ✅ Dependencias de Google OAuth importadas correctamente")
    except ImportError as e:
        print(f"   ❌ Error importando dependencias: {e}")
        return False
    
    return True

def print_next_steps():
    """Imprime los próximos pasos"""
    print("\n" + "=" * 60)
    print("🎉 ¡INSTALACIÓN COMPLETADA!")
    print("=" * 60)
    print()
    print("📋 PRÓXIMOS PASOS:")
    print()
    print("1. 🔧 CONFIGURAR GOOGLE OAUTH:")
    print("   - Ve a https://console.cloud.google.com/")
    print("   - Crea un proyecto y configura credenciales OAuth 2.0")
    print("   - Copia el Client ID y Client Secret al archivo .env")
    print()
    print("2. 🚀 EJECUTAR LA APLICACIÓN:")
    print("   python app.py")
    print()
    print("3. 🌐 PROBAR LA FUNCIONALIDAD:")
    print("   - Ve a http://localhost:5000/auth/login")
    print("   - Haz clic en 'Continuar con Google'")
    print()
    print("4. 📚 DOCUMENTACIÓN:")
    print("   - Consulta config_google_oauth.md para más detalles")
    print("   - Revisa google_config_ejemplo.txt para configuración")
    print()
    print("⚠️  IMPORTANTE:")
    print("   - Configura las credenciales de Google antes de usar")
    print("   - En producción, usa HTTPS y credenciales seguras")
    print("   - Cambia la SECRET_KEY en el archivo .env")
    print()
    print("🔗 ENLACES ÚTILES:")
    print("   - Google Cloud Console: https://console.cloud.google.com/")
    print("   - Documentación OAuth: https://developers.google.com/identity/protocols/oauth2")
    print()

def main():
    """Función principal del script"""
    print_header()
    
    # Verificar versión de Python
    if not check_python_version():
        sys.exit(1)
    
    # Instalar dependencias
    if not install_dependencies():
        print("\n❌ Error instalando dependencias")
        sys.exit(1)
    
    # Crear archivo .env
    if not create_env_file():
        print("\n❌ Error creando archivo de configuración")
        sys.exit(1)
    
    # Crear directorios
    if not create_directories():
        print("\n❌ Error creando directorios")
        sys.exit(1)
    
    # Actualizar base de datos
    if not update_database():
        print("\n❌ Error actualizando base de datos")
        sys.exit(1)
    
    # Crear archivo de ejemplo
    if not create_google_config_example():
        print("\n❌ Error creando archivo de ejemplo")
        sys.exit(1)
    
    # Verificar instalación
    if not verify_installation():
        print("\n❌ Error en la verificación")
        sys.exit(1)
    
    # Mostrar próximos pasos
    print_next_steps()

if __name__ == '__main__':
    main() 