#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Instalación - Sistema de Autenticación
===============================================

Script para instalar y configurar rápidamente el sistema de autenticación
en la Plataforma Preuniversitaria.

Autor: Plataforma Preuniversitaria
Fecha: 2025
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def print_header():
    """Imprimir encabezado del script"""
    print("=" * 60)
    print("🔐 INSTALADOR DEL SISTEMA DE AUTENTICACIÓN")
    print("   Plataforma Preuniversitaria v2.0.0")
    print("=" * 60)
    print()

def check_python_version():
    """Verificar versión de Python"""
    print("🐍 Verificando versión de Python...")
    if sys.version_info < (3, 7):
        print("❌ Error: Se requiere Python 3.7 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def install_dependencies():
    """Instalar dependencias"""
    print("\n📦 Instalando dependencias...")
    
    dependencies = [
        'flask-login==0.6.3',
        'flask-sqlalchemy==3.0.5',
        'werkzeug==2.3.7'
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

def create_database():
    """Crear base de datos inicial"""
    print("\n🗄️  Configurando base de datos...")
    
    try:
        # Importar después de instalar dependencias
        from models import db, Usuario
        from app import app
        
        with app.app_context():
            # Crear tablas
            db.create_all()
            
            # Verificar si ya existe un admin
            admin = Usuario.query.filter_by(username='admin').first()
            if not admin:
                # Crear usuario administrador
                admin = Usuario(
                    username='admin',
                    email='admin@plataforma.edu',
                    password='admin123',
                    nombre_completo='Administrador del Sistema'
                )
                admin.es_admin = True
                db.session.add(admin)
                db.session.commit()
                print("   ✅ Usuario administrador creado")
                print("      Usuario: admin")
                print("      Contraseña: admin123")
            else:
                print("   ✅ Usuario administrador ya existe")
        
        print("   ✅ Base de datos configurada correctamente")
        return True
        
    except Exception as e:
        print(f"   ❌ Error configurando base de datos: {e}")
        return False

def create_directories():
    """Crear directorios necesarios"""
    print("\n📁 Creando directorios...")
    
    directories = [
        'templates/auth',
        'logs',
        'uploads'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Directorio {directory} creado/verificado")

def create_env_file():
    """Crear archivo .env de ejemplo"""
    print("\n⚙️  Configurando variables de entorno...")
    
    env_content = """# Configuración de la Plataforma Preuniversitaria
# Cambia estos valores en producción

# Clave secreta para sesiones (¡CÁMBIALA EN PRODUCCIÓN!)
SECRET_KEY=tu_clave_secreta_muy_segura_aqui

# Base de datos
DATABASE_URL=sqlite:///plataforma.db

# Nivel de logging
LOG_LEVEL=INFO

# Configuración de email (opcional)
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=true
# MAIL_USERNAME=tu_email@gmail.com
# MAIL_PASSWORD=tu_contraseña_de_aplicacion
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("   ✅ Archivo .env creado")
        print("   ⚠️  Recuerda cambiar SECRET_KEY en producción")
    except Exception as e:
        print(f"   ❌ Error creando .env: {e}")

def verify_installation():
    """Verificar que todo esté funcionando"""
    print("\n🔍 Verificando instalación...")
    
    try:
        # Verificar archivos necesarios
        required_files = [
            'app.py',
            'models.py',
            'auth.py',
            'config.py',
            'templates/auth/login.html',
            'templates/auth/register.html'
        ]
        
        for file in required_files:
            if os.path.exists(file):
                print(f"   ✅ {file} encontrado")
            else:
                print(f"   ❌ {file} no encontrado")
                return False
        
        # Verificar base de datos
        if os.path.exists('plataforma.db'):
            print("   ✅ Base de datos creada")
        else:
            print("   ❌ Base de datos no encontrada")
            return False
        
        print("   ✅ Verificación completada")
        return True
        
    except Exception as e:
        print(f"   ❌ Error en verificación: {e}")
        return False

def print_success():
    """Imprimir mensaje de éxito"""
    print("\n" + "=" * 60)
    print("🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 60)
    print()
    print("📋 Próximos pasos:")
    print("   1. Ejecuta: python app.py")
    print("   2. Abre: http://localhost:5000")
    print("   3. Inicia sesión con:")
    print("      Usuario: admin")
    print("      Contraseña: admin123")
    print()
    print("🔐 Rutas de autenticación:")
    print("   - /auth/login - Iniciar sesión")
    print("   - /auth/register - Registrarse")
    print("   - /auth/profile - Mi perfil")
    print("   - /auth/admin/users - Administrar usuarios (solo admin)")
    print()
    print("📚 Documentación:")
    print("   - SISTEMA_AUTENTICACION.md - Guía completa")
    print("   - README.md - Documentación general")
    print()
    print("⚠️  IMPORTANTE:")
    print("   - Cambia la SECRET_KEY en producción")
    print("   - Cambia la contraseña del admin por defecto")
    print("   - Configura HTTPS en producción")
    print()
    print("🚀 ¡Disfruta tu nueva plataforma con autenticación!")

def main():
    """Función principal"""
    print_header()
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Instalar dependencias
    if not install_dependencies():
        print("\n❌ Error instalando dependencias")
        sys.exit(1)
    
    # Crear directorios
    create_directories()
    
    # Crear archivo .env
    create_env_file()
    
    # Crear base de datos
    if not create_database():
        print("\n❌ Error configurando base de datos")
        sys.exit(1)
    
    # Verificar instalación
    if not verify_installation():
        print("\n❌ Error en verificación")
        sys.exit(1)
    
    # Mensaje de éxito
    print_success()

if __name__ == '__main__':
    main() 