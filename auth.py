#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Autenticación - Plataforma Preuniversitaria
=====================================================

Rutas y funciones para el sistema de autenticación de usuarios.

Autor: Plataforma Preuniversitaria
Fecha: 2025
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, Usuario, SesionUsuario
from google_oauth import get_google_auth_url, handle_google_login, get_google_flow
import re
from datetime import datetime

auth = Blueprint('auth', __name__)

def validar_email(email):
    """Valida el formato del email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validar_password(password):
    """Valida que la contraseña cumpla con los requisitos mínimos"""
    if len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres"
    return True, ""

def validar_username(username):
    """Valida el formato del nombre de usuario"""
    if len(username) < 3:
        return False, "El nombre de usuario debe tener al menos 3 caracteres"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "El nombre de usuario solo puede contener letras, números y guiones bajos"
    return True, ""

def validar_nombre_completo(nombre_completo):
    """Valida el formato del nombre completo"""
    if not nombre_completo or not nombre_completo.strip():
        return False, "El nombre completo es obligatorio"
    if len(nombre_completo.strip()) < 2:
        return False, "El nombre completo debe tener al menos 2 caracteres"
    if len(nombre_completo.strip()) > 100:
        return False, "El nombre completo no puede exceder 100 caracteres"
    # Verificar que contenga al menos un espacio (nombre y apellido)
    if ' ' not in nombre_completo.strip():
        return False, "El nombre completo debe incluir nombre y apellido"
    return True, ""

def validar_institucion(institucion):
    """Valida que la institución sea obligatoria"""
    if not institucion or not institucion.strip():
        return False, "La institución educativa es obligatoria"
    if len(institucion.strip()) < 2:
        return False, "La institución debe tener al menos 2 caracteres"
    if len(institucion.strip()) > 100:
        return False, "La institución no puede exceder 100 caracteres"
    return True, ""

def validar_whatsapp(whatsapp):
    """Valida el formato del número de WhatsApp (opcional)"""
    if not whatsapp or not whatsapp.strip():
        return True, ""  # Es opcional
    
    # Limpiar el número (quitar espacios, guiones, paréntesis)
    numero_limpio = re.sub(r'[\s\-\(\)]', '', whatsapp.strip())
    
    # Verificar que solo contenga números y posiblemente un +
    if not re.match(r'^\+?[0-9]{7,15}$', numero_limpio):
        return False, "Formato de WhatsApp inválido (ej: +591 12345678 o 12345678)"
    
    return True, ""

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        # Validaciones básicas
        if not username or not password:
            flash('Por favor completa todos los campos', 'error')
            return render_template('auth/login.html')
        
        # Buscar usuario por username o email
        usuario = Usuario.query.filter(
            (Usuario.username == username) | (Usuario.email == username)
        ).first()
        
        if usuario and usuario.check_password(password):
            if not usuario.es_activo:
                flash('Tu cuenta ha sido desactivada. Contacta al administrador.', 'error')
                return render_template('auth/login.html')
            
            # Iniciar sesión
            login_user(usuario, remember=remember)
            
            # Actualizar último acceso
            usuario.actualizar_ultimo_acceso()
            
            # Registrar sesión (opcional)
            sesion = SesionUsuario(
                usuario_id=usuario.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent')
            )
            db.session.add(sesion)
            db.session.commit()
            
            # Guardar ID de sesión para cerrar sesión
            session['sesion_id'] = sesion.id
            
            flash(f'¡Bienvenido de vuelta, {usuario.nombre_completo}!', 'success')
            
            # Redirigir a la página solicitada o al inicio
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro de usuarios"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        nombre_completo = request.form.get('nombre_completo', '').strip()
        institucion = request.form.get('institucion', '').strip()
        whatsapp = request.form.get('whatsapp', '').strip()
        nivel_educativo = request.form.get('nivel_educativo', '').strip()
        
        # Validaciones
        errores = []
        
        # Validar username
        username_valido, msg = validar_username(username)
        if not username_valido:
            errores.append(msg)
        
        # Validar email
        if not validar_email(email):
            errores.append('Email inválido')
        
        # Validar nombre completo (OBLIGATORIO)
        nombre_valido, msg = validar_nombre_completo(nombre_completo)
        if not nombre_valido:
            errores.append(msg)
        
        # Validar institución (OBLIGATORIA)
        institucion_valida, msg = validar_institucion(institucion)
        if not institucion_valida:
            errores.append(msg)
        
        # Validar WhatsApp (OPCIONAL)
        whatsapp_valido, msg = validar_whatsapp(whatsapp)
        if not whatsapp_valido:
            errores.append(msg)
        
        # Validar contraseña
        password_valido, msg = validar_password(password)
        if not password_valido:
            errores.append(msg)
        
        # Confirmar contraseña
        if password != confirm_password:
            errores.append('Las contraseñas no coinciden')
        
        # Verificar si el usuario ya existe
        if Usuario.query.filter_by(username=username).first():
            errores.append('El nombre de usuario ya está en uso')
        
        if Usuario.query.filter_by(email=email).first():
            errores.append('El email ya está registrado')
        
        if errores:
            for error in errores:
                flash(error, 'error')
            return render_template('auth/register.html')
        
        # Crear nuevo usuario
        try:
            nuevo_usuario = Usuario(
                username=username,
                email=email,
                password=password,
                nombre_completo=nombre_completo.strip()  # Ya validado que no esté vacío
            )
            nuevo_usuario.institucion = institucion.strip()
            nuevo_usuario.whatsapp = whatsapp.strip() if whatsapp else None
            nuevo_usuario.nivel_educativo = nivel_educativo
            
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al crear la cuenta. Intenta nuevamente.', 'error')
            print(f"Error en registro: {e}")
    
    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    """Cerrar sesión del usuario"""
    # Marcar sesión como terminada
    sesion_id = session.get('sesion_id')
    if sesion_id:
        sesion = SesionUsuario.query.get(sesion_id)
        if sesion:
            sesion.fecha_fin = datetime.utcnow()
            db.session.commit()
    
    # Limpiar sesión
    session.pop('sesion_id', None)
    
    # Cerrar sesión de Flask-Login
    logout_user()
    
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))

@auth.route('/profile')
@login_required
def profile():
    """Página del perfil del usuario"""
    return render_template('auth/profile.html', usuario=current_user)

@auth.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Editar perfil del usuario"""
    if request.method == 'POST':
        nombre_completo = request.form.get('nombre_completo', '').strip()
        institucion = request.form.get('institucion', '').strip()
        nivel_educativo = request.form.get('nivel_educativo', '').strip()
        
        # Actualizar datos
        current_user.nombre_completo = nombre_completo or current_user.username
        current_user.institucion = institucion
        current_user.nivel_educativo = nivel_educativo
        
        db.session.commit()
        
        flash('Perfil actualizado correctamente', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/edit_profile.html', usuario=current_user)

@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Cambiar contraseña del usuario"""
    # Verificar si es usuario de Google
    if current_user.auth_provider == 'google':
        flash('Los usuarios de Google no pueden cambiar su contraseña desde aquí. Debes hacerlo desde tu cuenta de Google.', 'info')
        return redirect(url_for('auth.profile'))
    
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validar contraseña actual
        if not current_user.check_password(current_password):
            flash('La contraseña actual es incorrecta', 'error')
            return render_template('auth/change_password.html')
        
        # Validar nueva contraseña
        password_valido, msg = validar_password(new_password)
        if not password_valido:
            flash(msg, 'error')
            return render_template('auth/change_password.html')
        
        # Confirmar nueva contraseña
        if new_password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('auth/change_password.html')
        
        # Cambiar contraseña
        current_user.set_password(new_password)
        db.session.commit()
        
        flash('Contraseña cambiada correctamente', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/change_password.html')

# Rutas de administración (solo para admins)
@auth.route('/admin/users')
@login_required
def admin_users():
    """Lista de usuarios (solo para administradores)"""
    if not current_user.es_admin:
        flash('No tienes permisos para acceder a esta página', 'error')
        return redirect(url_for('index'))
    
    usuarios = Usuario.query.all()
    return render_template('auth/admin_users.html', usuarios=usuarios)

@auth.route('/admin/user/<int:user_id>/toggle')
@login_required
def admin_toggle_user(user_id):
    """Activar/desactivar usuario (solo para administradores)"""
    if not current_user.es_admin:
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('index'))
    
    usuario = Usuario.query.get_or_404(user_id)
    usuario.es_activo = not usuario.es_activo
    db.session.commit()
    
    estado = "activada" if usuario.es_activo else "desactivada"
    flash(f'Cuenta de {usuario.username} {estado}', 'success')
    
    return redirect(url_for('auth.admin_users'))

# ============================================
# RUTAS DE GOOGLE OAUTH
# ============================================

@auth.route('/google/login')
def google_login():
    """Iniciar el proceso de login con Google"""
    try:
        auth_url = get_google_auth_url()
        if auth_url:
            return redirect(auth_url)
        else:
            flash('Error al configurar la autenticación con Google', 'error')
            return redirect(url_for('auth.login'))
    except Exception as e:
        flash('Error al iniciar sesión con Google', 'error')
        return redirect(url_for('auth.login'))

@auth.route('/google/callback')
def google_callback():
    """Callback de Google OAuth"""
    try:
        # Obtener el código de autorización
        code = request.args.get('code')
        state = request.args.get('state')
        
        # Verificar el estado para prevenir CSRF
        if state != session.get('google_oauth_state'):
            flash('Error de seguridad en la autenticación', 'error')
            return redirect(url_for('auth.login'))
        
        if not code:
            flash('Error en la autorización de Google', 'error')
            return redirect(url_for('auth.login'))
        
        # Intercambiar código por token
        flow = get_google_flow()
        flow.fetch_token(code=code)
        
        # Obtener información del usuario
        session_info = flow.authorized_session()
        user_info = session_info.get('https://www.googleapis.com/oauth2/v2/userinfo').json()
        
        # Procesar login
        result, message = handle_google_login(user_info)
        
        if result == "complete_profile":
            flash(message, 'info')
            return redirect(url_for('auth.complete_profile'))
        elif result is True:
            flash(message, 'success')
            # Redirigir a la página solicitada o al inicio
            next_page = session.get('next')
            if next_page and next_page.startswith('/'):
                session.pop('next', None)
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash(message, 'error')
            return redirect(url_for('auth.login'))
            
    except Exception as e:
        flash('Error al procesar la autenticación con Google', 'error')
        return redirect(url_for('auth.login'))

@auth.route('/google/register')
def google_register():
    """Registro con Google (redirige al login de Google)"""
    # Guardar que el usuario quiere registrarse
    session['google_register'] = True
    return redirect(url_for('auth.google_login'))

@auth.route('/complete_profile', methods=['GET', 'POST'])
@login_required
def complete_profile():
    """Completar perfil después del registro con Google"""
    # Solo permitir si el usuario es de Google y no tiene institución
    if current_user.auth_provider != 'google' or current_user.institucion:
        return redirect(url_for('auth.profile'))
    
    if request.method == 'POST':
        institucion = request.form.get('institucion', '').strip()
        whatsapp = request.form.get('whatsapp', '').strip()
        nivel_educativo = request.form.get('nivel_educativo', '').strip()
        
        # Validaciones
        errores = []
        
        # Validar institución (OBLIGATORIA)
        institucion_valida, msg = validar_institucion(institucion)
        if not institucion_valida:
            errores.append(msg)
        
        # Validar WhatsApp (OPCIONAL)
        whatsapp_valido, msg = validar_whatsapp(whatsapp)
        if not whatsapp_valido:
            errores.append(msg)
        
        if errores:
            for error in errores:
                flash(error, 'error')
            return render_template('auth/complete_profile.html')
        
        # Actualizar perfil
        try:
            current_user.institucion = institucion.strip()
            current_user.whatsapp = whatsapp.strip() if whatsapp else None
            current_user.nivel_educativo = nivel_educativo
            
            db.session.commit()
            
            flash('¡Perfil completado exitosamente!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar el perfil. Intenta nuevamente.', 'error')
            print(f"Error en completar perfil: {e}")
    
    return render_template('auth/complete_profile.html') 