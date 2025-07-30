#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script que simula exactamente la inicialización de la base de datos de app.py
"""

from flask import Flask
from models import db, Usuario, init_db

# Crear aplicación exactamente como en app.py
app = Flask(__name__)

# Configuración de la aplicación (igual que en app.py)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configuración de la base de datos (igual que en app.py)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plataforma.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de sesiones (igual que en app.py)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui_cambiala_en_produccion'

# Inicializar extensiones (igual que en app.py)
db.init_app(app)

print("🚀 Simulando inicialización de app.py...")
print("📚 Cargando ejercicios desde nueva estructura jerárquica...")

# Inicializar base de datos (igual que en app.py)
with app.app_context():
    init_db(app)

print("✅ Inicialización completada") 