#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar la creación de la base de datos
"""

from flask import Flask
from models import db, Usuario, init_db

# Crear aplicación de prueba
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_plataforma.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'test_key'

print("🔧 Inicializando base de datos de prueba...")

with app.app_context():
    # Inicializar la base de datos
    db.init_app(app)
    db.create_all()
    
    print("✅ Tablas creadas correctamente")
    
    # Verificar que las tablas existen
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"📋 Tablas creadas: {tables}")
    
    # Verificar estructura de la tabla usuarios
    if 'usuarios' in tables:
        columns = inspector.get_columns('usuarios')
        print("📊 Columnas de la tabla usuarios:")
        for col in columns:
            print(f"   - {col['name']}: {col['type']}")
        
        # Verificar específicamente la columna whatsapp
        column_names = [col['name'] for col in columns]
        if 'whatsapp' in column_names:
            print("✅ Columna whatsapp encontrada")
        else:
            print("❌ Columna whatsapp NO encontrada")
            print(f"Columnas disponibles: {column_names}")
    
    # Intentar crear un usuario de prueba
    try:
        test_user = Usuario(
            username='test',
            email='test@test.com',
            password='test123',
            nombre_completo='Usuario de Prueba'
        )
        db.session.add(test_user)
        db.session.commit()
        print("✅ Usuario de prueba creado correctamente")
        
        # Verificar que se puede consultar
        user = Usuario.query.filter_by(username='test').first()
        if user:
            print(f"✅ Usuario encontrado: {user.username} - {user.institucion}")
        else:
            print("❌ No se pudo encontrar el usuario creado")
            
    except Exception as e:
        print(f"❌ Error al crear usuario de prueba: {e}")
        db.session.rollback()

print("🏁 Prueba completada") 