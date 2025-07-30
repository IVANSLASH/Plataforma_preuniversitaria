#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelos de Base de Datos - Plataforma Preuniversitaria
=====================================================

Modelos para el sistema de autenticación y gestión de usuarios.

Autor: Plataforma Preuniversitaria
Fecha: 2025
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    """
    Modelo de usuario para el sistema de autenticación
    """
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)  # Nullable para usuarios de Google
    nombre_completo = db.Column(db.String(100), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_acceso = db.Column(db.DateTime, nullable=True)
    es_activo = db.Column(db.Boolean, default=True)
    es_admin = db.Column(db.Boolean, default=False)
    
    # Campos para autenticación con Google OAuth
    google_id = db.Column(db.String(100), unique=True, nullable=True)
    google_picture = db.Column(db.String(500), nullable=True)
    auth_provider = db.Column(db.String(20), default='local')  # 'local' o 'google'
    
    # Campos adicionales para el perfil
    institucion = db.Column(db.String(100), nullable=False)  # Obligatorio para todos
    whatsapp = db.Column(db.String(20), nullable=True)  # Opcional
    nivel_educativo = db.Column(db.String(50), nullable=True)
    materias_favoritas = db.Column(db.Text, nullable=True)  # JSON como string
    preferencias = db.Column(db.Text, nullable=True)  # JSON como string
    
    def __init__(self, username, email, password=None, nombre_completo=None, google_id=None, google_picture=None):
        self.username = username
        self.email = email
        self.nombre_completo = nombre_completo
        
        # Inicializar campos obligatorios con valores por defecto
        self.institucion = 'Sin especificar'  # Campo obligatorio
        
        if google_id:
            self.google_id = google_id
            self.google_picture = google_picture
            self.auth_provider = 'google'
            # Para usuarios de Google, no necesitamos password_hash
        else:
            self.auth_provider = 'local'
            if password:
                self.set_password(password)
            else:
                raise ValueError("Se requiere contraseña para usuarios locales")
    
    def set_password(self, password):
        """Genera un hash seguro de la contraseña"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica si la contraseña es correcta"""
        if self.auth_provider == 'google':
            return False  # Usuarios de Google no usan contraseñas locales
        return check_password_hash(self.password_hash, password)
    
    def actualizar_ultimo_acceso(self):
        """Actualiza la fecha del último acceso"""
        self.ultimo_acceso = datetime.utcnow()
        db.session.commit()
    
    @classmethod
    def get_by_google_id(cls, google_id):
        """Busca un usuario por su Google ID"""
        return cls.query.filter_by(google_id=google_id).first()
    
    @classmethod
    def get_by_email(cls, email):
        """Busca un usuario por su email"""
        return cls.query.filter_by(email=email).first()
    
    def is_google_user(self):
        """Verifica si el usuario se registró con Google"""
        return self.auth_provider == 'google'
    
    def to_dict(self):
        """Convierte el usuario a diccionario (sin información sensible)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'nombre_completo': self.nombre_completo,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'ultimo_acceso': self.ultimo_acceso.isoformat() if self.ultimo_acceso else None,
            'es_activo': self.es_activo,
            'es_admin': self.es_admin,
            'auth_provider': self.auth_provider,
            'google_picture': self.google_picture,
            'institucion': self.institucion,
            'whatsapp': self.whatsapp,
            'nivel_educativo': self.nivel_educativo
        }
    
    def __repr__(self):
        return f'<Usuario {self.username}>'

class SesionUsuario(db.Model):
    """
    Modelo para registrar sesiones de usuario (opcional, para auditoría)
    """
    __tablename__ = 'sesiones_usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_fin = db.Column(db.DateTime, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)  # IPv6 compatible
    user_agent = db.Column(db.Text, nullable=True)
    
    # Relación con el usuario
    usuario = db.relationship('Usuario', backref=db.backref('sesiones', lazy=True))
    
    def __repr__(self):
        return f'<SesionUsuario {self.usuario_id} - {self.fecha_inicio}>'

def init_db(app):
    """Inicializa la base de datos"""
    # Solo inicializar si no está ya inicializado
    if not hasattr(app, 'extensions') or 'sqlalchemy' not in app.extensions:
        db.init_app(app)
    
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        
        # Verificar que las tablas se crearon correctamente
        try:
            # Crear usuario administrador por defecto si no existe
            admin = Usuario.query.filter_by(username='admin').first()
            if not admin:
                admin = Usuario(
                    username='admin',
                    email='admin@plataforma.edu',
                    password='admin123',
                    nombre_completo='Administrador del Sistema'
                )
                admin.es_admin = True
                admin.institucion = 'Sistema'  # Campo obligatorio
                db.session.add(admin)
                db.session.commit()
                print("✅ Usuario administrador creado: admin / admin123")
            
            print(f"✅ Base de datos inicializada con {Usuario.query.count()} usuarios")
        except Exception as e:
            print(f"❌ Error al inicializar base de datos: {e}")
            # Intentar recrear las tablas
            db.drop_all()
            db.create_all()
            print("🔄 Tablas recreadas, intentando crear usuario admin...")
            
            try:
                admin = Usuario(
                    username='admin',
                    email='admin@plataforma.edu',
                    password='admin123',
                    nombre_completo='Administrador del Sistema'
                )
                admin.es_admin = True
                admin.institucion = 'Sistema'
                db.session.add(admin)
                db.session.commit()
                print("✅ Usuario administrador creado después de recrear tablas")
            except Exception as e2:
                print(f"❌ Error crítico: {e2}")
                raise 