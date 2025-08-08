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
    
    # Campos para sistema de límites diarios
    ejercicios_vistos_hoy = db.Column(db.Integer, default=0)  # Contador de ejercicios vistos hoy
    ultima_fecha_conteo = db.Column(db.Date, nullable=True)  # Última fecha en que se contaron ejercicios
    ejercicios_vistos_ids = db.Column(db.Text, nullable=True)  # IDs de ejercicios vistos hoy (JSON)
    
    # Campos para sistema de límites de simulacros
    simulacros_realizados_hoy = db.Column(db.Integer, default=0)  # Contador de simulacros realizados hoy
    ultima_fecha_simulacro = db.Column(db.Date, nullable=True)  # Última fecha en que se realizó un simulacro
    
    def __init__(self, username, email, password=None, nombre_completo=None, google_id=None, google_picture=None):
        self.username = username
        self.email = email
        self.nombre_completo = nombre_completo
        
        # Inicializar campos con valores por defecto
        self.acepta_anuncios = False
        self.es_admin = False  # Explícitamente establecer como no admin
        
        # Lista de emails que siempre deben ser admin (backup de seguridad)
        admin_emails = ['ingivanladislao@gmail.com']
        
        if google_id:
            self.google_id = google_id
            self.google_picture = google_picture
            self.auth_provider = 'google'
            # Para usuarios de Google, no necesitamos password_hash
            
            # Verificar si este email debe ser admin
            if email in admin_emails:
                self.es_admin = True
        else:
            # Solo permitir usuarios de Google
            raise ValueError("Solo se permite registro mediante Google OAuth")
    
    def actualizar_ultimo_acceso(self):
        """Actualiza la fecha del último acceso"""
        self.ultimo_acceso = datetime.utcnow()
        
        # Verificar y preservar admin status para emails específicos
        self.verificar_admin_status()
        
        db.session.commit()
    
    def verificar_admin_status(self):
        """Verifica y preserva el admin status para emails específicos"""
        admin_emails = ['ingivanladislao@gmail.com']
        
        if self.email in admin_emails and not self.es_admin:
            self.es_admin = True
            print(f"🔧 Admin status restaurado para: {self.email}")
    
    @classmethod
    def get_by_google_id(cls, google_id):
        """Busca un usuario por su Google ID"""
        return cls.query.filter_by(google_id=google_id).first()
    
    @classmethod
    def get_by_email(cls, email):
        """Busca un usuario por su email"""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def create_google_user(cls, username, email, nombre_completo, google_id, google_picture):
        """Crea un nuevo usuario de Google con verificación de admin status"""
        # Lista de emails que siempre deben ser admin
        admin_emails = ['ingivanladislao@gmail.com']
        
        # Crear el usuario
        usuario = cls(
            username=username,
            email=email,
            nombre_completo=nombre_completo,
            google_id=google_id,
            google_picture=google_picture
        )
        
        # Verificar si debe ser admin
        if email in admin_emails:
            usuario.es_admin = True
            print(f"👑 Usuario admin creado: {email}")
        
        return usuario
    
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
    
    def reset_daily_count(self):
        """Reinicia el contador diario de ejercicios"""
        from datetime import date
        today = date.today()
        
        if self.ultima_fecha_conteo != today:
            self.ejercicios_vistos_hoy = 0
            self.ultima_fecha_conteo = today
            self.ejercicios_vistos_ids = '[]'
            db.session.commit()
    
    def can_view_exercise(self, ejercicio_id):
        """Verifica si el usuario puede ver un ejercicio específico"""
        import json
        
        # Si es premium, puede ver todo
        if self.is_premium_active():
            return True
        
        # Reiniciar contador si es un nuevo día
        self.reset_daily_count()
        
        # Obtener límite según tipo de usuario
        limite_diario = 15 if self.is_authenticated else 5
        
        # Verificar si ya vio este ejercicio hoy
        ejercicios_vistos = []
        if self.ejercicios_vistos_ids:
            try:
                ejercicios_vistos = json.loads(self.ejercicios_vistos_ids)
            except:
                ejercicios_vistos = []
        
        # Si ya vio este ejercicio, puede verlo
        if ejercicio_id in ejercicios_vistos:
            return True
        
        # Verificar si no ha alcanzado el límite
        return self.ejercicios_vistos_hoy < limite_diario
    
    def mark_exercise_as_viewed(self, ejercicio_id):
        """Marca un ejercicio como visto"""
        import json
        
        # Si es premium, no necesita contar
        if self.is_premium_active():
            return True
        
        # Reiniciar contador si es un nuevo día
        self.reset_daily_count()
        
        # Obtener límite según tipo de usuario
        limite_diario = 15 if self.is_authenticated else 5
        
        # Verificar si ya vio este ejercicio hoy
        ejercicios_vistos = []
        if self.ejercicios_vistos_ids:
            try:
                ejercicios_vistos = json.loads(self.ejercicios_vistos_ids)
            except:
                ejercicios_vistos = []
        
        # Si ya vio este ejercicio, no contar de nuevo
        if ejercicio_id in ejercicios_vistos:
            return True
        
        # Verificar si no ha alcanzado el límite
        if self.ejercicios_vistos_hoy >= limite_diario:
            return False
        
        # Marcar como visto
        ejercicios_vistos.append(ejercicio_id)
        self.ejercicios_vistos_hoy += 1
        self.ejercicios_vistos_ids = json.dumps(ejercicios_vistos)
        db.session.commit()
        
        return True
    
    def get_daily_limit_info(self):
        """Obtiene información sobre los límites diarios"""
        self.reset_daily_count()
        
        limite_diario = 15 if self.is_authenticated else 5
        ejercicios_restantes = max(0, limite_diario - self.ejercicios_vistos_hoy)
        
        return {
            'limite_diario': limite_diario,
            'ejercicios_vistos': self.ejercicios_vistos_hoy,
            'ejercicios_restantes': ejercicios_restantes,
            'es_premium': self.is_premium_active(),
            'tipo_usuario': 'registrado' if self.is_authenticated else 'sin_registro'
        }
    
    def reset_simulacro_count(self):
        """Reinicia el contador de simulacros si es un nuevo día"""
        from datetime import date
        hoy = date.today()
        
        if self.ultima_fecha_simulacro != hoy:
            self.simulacros_realizados_hoy = 0
            self.ultima_fecha_simulacro = hoy
            db.session.commit()
    
    def can_do_simulacro(self):
        """Verifica si el usuario puede realizar un simulacro hoy"""
        # Usuarios premium tienen simulacros ilimitados
        if self.is_premium_active():
            return True
        
        # Usuarios no registrados no pueden hacer simulacros
        if not self.is_authenticated:
            return False
        
        self.reset_simulacro_count()
        
        # Usuarios registrados pueden hacer 1 simulacro por día
        return self.simulacros_realizados_hoy < 1
    
    def mark_simulacro_as_done(self):
        """Marca que el usuario ha realizado un simulacro hoy"""
        if not self.can_do_simulacro():
            return False
        
        self.reset_simulacro_count()
        self.simulacros_realizados_hoy += 1
        db.session.commit()
        return True
    
    def get_simulacro_limit_info(self):
        """Obtiene información sobre los límites de simulacros"""
        self.reset_simulacro_count()
        
        if self.is_premium_active():
            return {
                'limite_diario': 'ilimitado',
                'simulacros_realizados': self.simulacros_realizados_hoy,
                'simulacros_restantes': 'ilimitado',
                'es_premium': True,
                'puede_hacer': True
            }
        
        if not self.is_authenticated:
            return {
                'limite_diario': 0,
                'simulacros_realizados': 0,
                'simulacros_restantes': 0,
                'es_premium': False,
                'puede_hacer': False,
                'mensaje': 'Debes registrarte para realizar simulacros'
            }
        
        limite_diario = 1
        simulacros_restantes = max(0, limite_diario - self.simulacros_realizados_hoy)
        
        return {
            'limite_diario': limite_diario,
            'simulacros_realizados': self.simulacros_realizados_hoy,
            'simulacros_restantes': simulacros_restantes,
            'es_premium': False,
            'puede_hacer': simulacros_restantes > 0
        }
    
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

class EjercicioVisto(db.Model):
    """
    Modelo para registrar ejercicios vistos por usuarios (para auditoría y análisis)
    """
    __tablename__ = 'ejercicios_vistos'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)  # Nullable para usuarios sin registro
    ejercicio_id = db.Column(db.String(50), nullable=False)  # ID del ejercicio
    fecha_visto = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    session_id = db.Column(db.String(100), nullable=True)  # Para usuarios sin registro
    
    # Relación con el usuario (opcional)
    usuario = db.relationship('Usuario', backref=db.backref('ejercicios_vistos', lazy=True))
    
    def __repr__(self):
        return f'<EjercicioVisto {self.ejercicio_id} - {self.fecha_visto}>'

class VisitaPagina(db.Model):
    """Registro de visitas a la plataforma (para métricas de acceso global)."""
    __tablename__ = 'visitas_pagina'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(512), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)

    # Relación opcional con usuario
    usuario = db.relationship('Usuario', backref=db.backref('visitas', lazy=True))

    def __repr__(self):
        return f'<Visita {self.path} - {self.fecha}>'

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