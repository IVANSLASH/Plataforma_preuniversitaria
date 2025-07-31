#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para convertir una cuenta de Google en administrador
==========================================================

Este script convierte una cuenta de usuario de Google en administrador.
Útil cuando solo se permite autenticación por Google.

Uso: python hacer_admin.py
"""

import os
import sys
from datetime import datetime

# Agregar el directorio actual al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import db, Usuario
from app import app

def hacer_admin_google(email):
    """
    Convierte una cuenta de Google en administrador
    """
    with app.app_context():
        try:
            # Buscar el usuario por email
            usuario = Usuario.query.filter_by(email=email).first()
            
            if not usuario:
                print(f"❌ No se encontró un usuario con el email: {email}")
                print("💡 Asegúrate de haber iniciado sesión al menos una vez con Google")
                return False
            
            if usuario.auth_provider != 'google':
                print(f"⚠️  El usuario {email} no es una cuenta de Google")
                print(f"   Método de autenticación: {usuario.auth_provider}")
                return False
            
            if usuario.es_admin:
                print(f"✅ El usuario {email} ya es administrador")
                return True
            
            # Convertir en administrador
            usuario.es_admin = True
            db.session.commit()
            
            print(f"✅ Usuario {email} convertido en administrador exitosamente")
            print(f"   Nombre: {usuario.nombre_completo}")
            print(f"   Username: {usuario.username}")
            print(f"   Fecha de registro: {usuario.fecha_registro}")
            return True
            
        except Exception as e:
            print(f"❌ Error al convertir en administrador: {e}")
            db.session.rollback()
            return False

def listar_usuarios_google():
    """
    Lista todos los usuarios de Google
    """
    with app.app_context():
        try:
            usuarios_google = Usuario.query.filter_by(auth_provider='google').all()
            
            if not usuarios_google:
                print("❌ No hay usuarios de Google registrados")
                return
            
            print("📋 Usuarios de Google registrados:")
            print("-" * 80)
            
            for i, usuario in enumerate(usuarios_google, 1):
                admin_status = "👑 ADMIN" if usuario.es_admin else "👤 Usuario"
                print(f"{i:2d}. {usuario.email}")
                print(f"    Nombre: {usuario.nombre_completo}")
                print(f"    Username: {usuario.username}")
                print(f"    Estado: {admin_status}")
                print(f"    Registro: {usuario.fecha_registro.strftime('%d/%m/%Y %H:%M') if usuario.fecha_registro else 'N/A'}")
                print()
            
        except Exception as e:
            print(f"❌ Error al listar usuarios: {e}")

def main():
    """
    Función principal del script
    """
    print("🔧 Script para convertir cuenta de Google en administrador")
    print("=" * 60)
    
    # Email específico que quieres convertir
    email_objetivo = "ingivanladislao@gmail.com"
    
    print(f"🎯 Objetivo: Convertir {email_objetivo} en administrador")
    print()
    
    # Mostrar usuarios de Google disponibles
    print("📋 Usuarios de Google disponibles:")
    listar_usuarios_google()
    
    # Intentar convertir el usuario objetivo
    print(f"🔄 Intentando convertir {email_objetivo}...")
    success = hacer_admin_google(email_objetivo)
    
    if success:
        print()
        print("🎉 ¡Listo! Ahora puedes:")
        print("1. Iniciar sesión con Google usando tu cuenta")
        print("2. Ir a tu perfil")
        print("3. Hacer clic en 'Panel de Administración'")
        print("4. Gestionar usuarios y cuentas premium")
    else:
        print()
        print("💡 Si no se encontró tu cuenta, asegúrate de:")
        print("1. Haber iniciado sesión al menos una vez con Google")
        print("2. Usar el email correcto: ingivanladislao@gmail.com")
        print("3. Que la cuenta esté registrada en la base de datos")

if __name__ == "__main__":
    main() 