#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración de Google OAuth - Plataforma Preuniversitaria
==========================================================

Configuración y funciones para la autenticación con Google OAuth.

Autor: Plataforma Preuniversitaria
Fecha: 2025
"""

import os
import json
from google.oauth2 import id_token
from google.auth.transport import requests
from google_auth_oauthlib.flow import Flow
from flask import current_app, session, url_for, request
from models import db, Usuario, SesionUsuario
from flask_login import login_user
from datetime import datetime

# Configuración de Google OAuth
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '')
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid_configuration"

# Configuración del flujo OAuth
SCOPES = [
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email'
]

def get_google_flow():
    """Crea y configura el flujo de OAuth de Google"""
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [
                    "http://localhost:5000/auth/google/callback",
                    "https://tu-dominio.com/auth/google/callback"  # Cambiar en producción
                ]
            }
        },
        scopes=SCOPES
    )
    
    # Configurar la URL de redirección
    flow.redirect_uri = url_for('auth.google_callback', _external=True)
    
    return flow

def verify_google_token(token):
    """Verifica el token de ID de Google"""
    try:
        # Verificar el token con Google
        idinfo = id_token.verify_oauth2_token(
            token, 
            requests.Request(), 
            GOOGLE_CLIENT_ID
        )
        
        # Verificar que el token no haya expirado
        if idinfo['aud'] != GOOGLE_CLIENT_ID:
            raise ValueError('Wrong audience.')
        
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        
        return idinfo
    except Exception as e:
        current_app.logger.error(f"Error verificando token de Google: {e}")
        return None

def create_or_get_google_user(google_data):
    """Crea un nuevo usuario o obtiene uno existente basado en datos de Google"""
    try:
        google_id = google_data['sub']
        email = google_data['email']
        nombre_completo = google_data.get('name', '')
        picture = google_data.get('picture', '')
        
        # Buscar usuario existente por Google ID
        usuario = Usuario.get_by_google_id(google_id)
        
        if usuario:
            # Usuario ya existe, actualizar información
            usuario.nombre_completo = nombre_completo
            usuario.google_picture = picture
            usuario.actualizar_ultimo_acceso()
            db.session.commit()
            return usuario
        
        # Buscar usuario existente por email
        usuario = Usuario.get_by_email(email)
        if usuario:
            # Usuario existe pero no tiene Google ID, vincular
            usuario.google_id = google_id
            usuario.google_picture = picture
            usuario.auth_provider = 'google'
            usuario.nombre_completo = nombre_completo
            usuario.actualizar_ultimo_acceso()
            db.session.commit()
            return usuario
        
        # Crear nuevo usuario
        username = email.split('@')[0]  # Usar parte del email como username
        base_username = username
        counter = 1
        
        # Asegurar username único
        while Usuario.query.filter_by(username=username).first():
            username = f"{base_username}{counter}"
            counter += 1
        
        usuario = Usuario(
            username=username,
            email=email,
            nombre_completo=nombre_completo,
            google_id=google_id,
            google_picture=picture
        )
        
        db.session.add(usuario)
        db.session.commit()
        
        return usuario
        
    except Exception as e:
        current_app.logger.error(f"Error creando/obteniendo usuario de Google: {e}")
        db.session.rollback()
        return None

def handle_google_login(google_data):
    """Maneja el proceso de login con Google"""
    try:
        usuario = create_or_get_google_user(google_data)
        
        if not usuario:
            return False, "Error al procesar datos de Google"
        
        if not usuario.es_activo:
            return False, "Tu cuenta ha sido desactivada. Contacta al administrador."
        
        # Iniciar sesión
        login_user(usuario, remember=True)
        
        # Registrar sesión
        sesion = SesionUsuario(
            usuario_id=usuario.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(sesion)
        db.session.commit()
        
        # Guardar ID de sesión
        session['sesion_id'] = sesion.id
        
        # Verificar si necesita completar perfil (usuario nuevo de Google sin institución)
        if usuario.auth_provider == 'google' and not usuario.institucion:
            return "complete_profile", f"¡Bienvenido, {usuario.nombre_completo}! Completa tu perfil para continuar."
        
        return True, f"¡Bienvenido, {usuario.nombre_completo}!"
        
    except Exception as e:
        current_app.logger.error(f"Error en login con Google: {e}")
        return False, "Error interno del servidor"

def get_google_auth_url():
    """Genera la URL de autorización de Google"""
    try:
        flow = get_google_flow()
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        # Guardar el estado en la sesión
        session['google_oauth_state'] = state
        
        return authorization_url
    except Exception as e:
        current_app.logger.error(f"Error generando URL de Google OAuth: {e}")
        return None 