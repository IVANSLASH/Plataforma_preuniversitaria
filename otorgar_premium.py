#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Administración - Plataforma Preuniversitaria
=====================================================

Script para otorgar/quitar premium y administrar límites diarios.

Autor: Plataforma Preuniversitaria
Fecha: 2025
"""

import os
import sys
from datetime import datetime, timedelta

# Agregar el directorio actual al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Usuario

def otorgar_premium_usuario(email, tipo='mensual', duracion_dias=30, razon='Otorgado por administrador'):
    """Otorga premium a un usuario por email"""
    with app.app_context():
        usuario = Usuario.get_by_email(email)
        if not usuario:
            print(f"❌ Usuario con email '{email}' no encontrado")
            return False
        
        usuario.grant_premium(tipo, duracion_dias, razon)
        print(f"✅ Premium otorgado a {usuario.nombre_completo} ({email})")
        print(f"   Tipo: {tipo}")
        print(f"   Duración: {duracion_dias} días")
        print(f"   Razón: {razon}")
        return True

def listar_usuarios_premium():
    """Lista todos los usuarios premium"""
    with app.app_context():
        usuarios_premium = Usuario.query.filter_by(es_premium=True).all()
        
        if not usuarios_premium:
            print("📋 No hay usuarios premium")
            return
        
        print(f"📋 Usuarios Premium ({len(usuarios_premium)}):")
        print("-" * 80)
        
        for usuario in usuarios_premium:
            estado = "Activo" if usuario.is_premium_active() else "Expirado"
            fecha_fin = usuario.fecha_premium_fin.strftime('%Y-%m-%d') if usuario.fecha_premium_fin else "N/A"
            
            print(f"👤 {usuario.nombre_completo}")
            print(f"   Email: {usuario.email}")
            print(f"   Tipo: {usuario.tipo_premium}")
            print(f"   Estado: {estado}")
            print(f"   Fecha fin: {fecha_fin}")
            print(f"   Razón: {usuario.razon_premium}")
            print("-" * 80)

def mostrar_estadisticas_limites():
    """Muestra estadísticas de límites diarios para todos los usuarios"""
    with app.app_context():
        usuarios = Usuario.query.all()
        
        print(f"📊 Estadísticas de Límites Diarios ({len(usuarios)} usuarios):")
        print("=" * 100)
        
        for usuario in usuarios:
            limites_info = usuario.get_daily_limit_info()
            simulacro_info = usuario.get_simulacro_limit_info()
            
            print(f"👤 {usuario.nombre_completo} ({usuario.email})")
            print(f"   Premium: {'Sí' if limites_info['es_premium'] else 'No'}")
            print(f"   Ejercicios vistos hoy: {limites_info['ejercicios_vistos']}/{limites_info['limite_diario']}")
            print(f"   Simulacros realizados hoy: {simulacro_info['simulacros_realizados']}/{simulacro_info['limite_diario']}")
            print("-" * 50)

def resetear_limites_usuario(email):
    """Resetea los límites diarios de un usuario específico"""
    with app.app_context():
        usuario = Usuario.get_by_email(email)
        if not usuario:
            print(f"❌ Usuario con email '{email}' no encontrado")
            return False
        
        # Resetear límites de ejercicios
        usuario.ejercicios_vistos_hoy = 0
        usuario.ultima_fecha_conteo = None
        usuario.ejercicios_vistos_ids = None
        
        # Resetear límites de simulacros
        usuario.simulacros_realizados_hoy = 0
        usuario.ultima_fecha_simulacro = None
        
        db.session.commit()
        
        print(f"✅ Límites reseteados para {usuario.nombre_completo} ({email})")
        return True

def mostrar_limites_simulacros():
    """Muestra información específica sobre límites de simulacros"""
    with app.app_context():
        usuarios = Usuario.query.all()
        
        print(f"📊 Límites de Simulacros ({len(usuarios)} usuarios):")
        print("=" * 80)
        
        for usuario in usuarios:
            simulacro_info = usuario.get_simulacro_limit_info()
            
            print(f"👤 {usuario.nombre_completo} ({usuario.email})")
            print(f"   Premium: {'Sí' if simulacro_info['es_premium'] else 'No'}")
            print(f"   Puede hacer simulacro: {'Sí' if simulacro_info['puede_hacer'] else 'No'}")
            print(f"   Simulacros realizados: {simulacro_info['simulacros_realizados']}")
            print(f"   Límite diario: {simulacro_info['limite_diario']}")
            if 'mensaje' in simulacro_info:
                print(f"   Mensaje: {simulacro_info['mensaje']}")
            print("-" * 50)

def main():
    """Función principal del script"""
    if len(sys.argv) < 2:
        print("🔧 Script de Administración - Plataforma Preuniversitaria")
        print("=" * 60)
        print("Uso:")
        print("  python otorgar_premium.py otorgar <email> [tipo] [dias] [razon]")
        print("  python otorgar_premium.py listar")
        print("  python otorgar_premium.py estadisticas")
        print("  python otorgar_premium.py resetear <email>")
        print("  python otorgar_premium.py simulacros")
        print("\nEjemplos:")
        print("  python otorgar_premium.py otorgar usuario@ejemplo.com")
        print("  python otorgar_premium.py otorgar usuario@ejemplo.com mensual 30 'Prueba'")
        print("  python otorgar_premium.py listar")
        print("  python otorgar_premium.py estadisticas")
        print("  python otorgar_premium.py resetear usuario@ejemplo.com")
        print("  python otorgar_premium.py simulacros")
        return
    
    comando = sys.argv[1].lower()
    
    if comando == "otorgar":
        if len(sys.argv) < 3:
            print("❌ Error: Debes especificar un email")
            return
        
        email = sys.argv[2]
        tipo = sys.argv[3] if len(sys.argv) > 3 else 'mensual'
        duracion = int(sys.argv[4]) if len(sys.argv) > 4 else 30
        razon = sys.argv[5] if len(sys.argv) > 5 else 'Otorgado por administrador'
        
        otorgar_premium_usuario(email, tipo, duracion, razon)
    
    elif comando == "listar":
        listar_usuarios_premium()
    
    elif comando == "estadisticas":
        mostrar_estadisticas_limites()
    
    elif comando == "resetear":
        if len(sys.argv) < 3:
            print("❌ Error: Debes especificar un email")
            return
        
        email = sys.argv[2]
        resetear_limites_usuario(email)
    
    elif comando == "simulacros":
        mostrar_limites_simulacros()
    
    else:
        print(f"❌ Comando '{comando}' no reconocido")
        print("Usa 'python otorgar_premium.py' para ver la ayuda")

if __name__ == "__main__":
    main() 