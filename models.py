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
    
    # Campos adicionales para el perfil universitario
    ultima_unidad_educativa = db.Column(db.String(100), nullable=True)  # Última institución educativa
    nivel_academico_actual = db.Column(db.String(50), nullable=True)  # Nivel académico actual
    nivel_academico_otro = db.Column(db.String(100), nullable=True) # Especificación para 'otro' nivel
    intereses = db.Column(db.Text, nullable=True)  # Intereses académicos/profesionales
    whatsapp = db.Column(db.String(20), nullable=True)  # Opcional - para ofertas y anuncios
    ciudad = db.Column(db.String(50), nullable=True)  # Ciudad
    carrera_interes = db.Column(db.String(100), nullable=True)  # Carrera de interés
    materias_favoritas = db.Column(db.Text, nullable=True)  # JSON como string
    preferencias = db.Column(db.Text, nullable=True)  # JSON como string
    acepta_anuncios = db.Column(db.Boolean, default=False)  # Si acepta recibir anuncios
    profile_completed = db.Column(db.Boolean, default=False) # Si el perfil ha sido completado
    
    # Campos para sistema premium
    es_premium = db.Column(db.Boolean, default=False)  # Si tiene cuenta premium
    fecha_premium_inicio = db.Column(db.DateTime, nullable=True)  # Fecha de inicio de premium
    fecha_premium_fin = db.Column(db.DateTime, nullable=True)  # Fecha de fin de premium
    tipo_premium = db.Column(db.String(20), nullable=True)  # 'mensual', 'anual', 'permanente'
    razon_premium = db.Column(db.String(100), nullable=True)  # Razón por la que se otorgó premium
    
    def __init__(self, username, email, password=None, nombre_completo=None, google_id=None, google_picture=None):
        self.username = username
        self.email = email
        self.nombre_completo = nombre_completo
        
        # Inicializar campos con valores por defecto
        self.acepta_anuncios = False
        
        if google_id:
            self.google_id = google_id
            self.google_picture = google_picture
            self.auth_provider = 'google'
            # Para usuarios de Google, no necesitamos password_hash
        else:
            # Solo permitir usuarios de Google
            raise ValueError("Solo se permite registro mediante Google OAuth")
    
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
    
    def is_premium_active(self):
        """Verifica si el usuario tiene premium activo"""
        if not self.es_premium:
            return False
        
        # Si es premium permanente
        if self.tipo_premium == 'permanente':
            return True
        
        # Si tiene fecha de fin y ya expiró
        if self.fecha_premium_fin and datetime.utcnow() > self.fecha_premium_fin:
            self.es_premium = False
            db.session.commit()
            return False
        
        return True
    
    def grant_premium(self, tipo='mensual', duracion_dias=30, razon='Otorgado por administrador'):
        """Otorga premium al usuario"""
        from datetime import timedelta
        
        self.es_premium = True
        self.fecha_premium_inicio = datetime.utcnow()
        self.tipo_premium = tipo
        self.razon_premium = razon
        
        if tipo == 'permanente':
            self.fecha_premium_fin = None
        else:
            self.fecha_premium_fin = datetime.utcnow() + timedelta(days=duracion_dias)
        
        db.session.commit()
    
    def revoke_premium(self, razon='Revocado por administrador'):
        """Revoca premium al usuario"""
        self.es_premium = False
        self.fecha_premium_inicio = None
        self.fecha_premium_fin = None
        self.tipo_premium = None
        self.razon_premium = razon
        db.session.commit()
    
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
            'ultima_unidad_educativa': self.ultima_unidad_educativa,
            'nivel_academico_actual': self.nivel_academico_actual,
            'intereses': self.intereses,
            'whatsapp': self.whatsapp,
            'ciudad': self.ciudad,
            'carrera_interes': self.carrera_interes,
            'acepta_anuncios': self.acepta_anuncios,
            'es_premium': self.es_premium,
            'premium_activo': self.is_premium_active(),
            'tipo_premium': self.tipo_premium,
            'fecha_premium_fin': self.fecha_premium_fin.isoformat() if self.fecha_premium_fin else None
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
            print(f"✅ Base de datos inicializada con {Usuario.query.count()} usuarios")
            print("🔒 Sistema configurado para autenticación exclusiva con Google OAuth")
        except Exception as e:
            print(f"❌ Error al inicializar base de datos: {e}")
            # Intentar recrear las tablas
            db.drop_all()
            db.create_all()
            print("🔄 Tablas recreadas")
            print("🔒 Sistema configurado para autenticación exclusiva con Google OAuth") 