
import os
import json
from flask import Blueprint, redirect, url_for, flash, render_template, request, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from authlib.integrations.flask_client import OAuth
from models import db, Usuario

# Blueprint para la autenticación
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Configuración de OAuth
oauth = OAuth()

def init_oauth(app):
    """Inicializa el cliente OAuth con la configuración de la app."""
    oauth.init_app(app)
    oauth.register(
        name='google',
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_id=os.environ.get("GOOGLE_CLIENT_ID"),
        client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

@auth_bp.route('/login')
def login():
    """
    Redirige al usuario a la autenticación de Google OAuth.
    Esta es la única forma de autenticación permitida.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # El redirect_uri debe ser la URL absoluta de la ruta 'authorize'
    redirect_uri = url_for('auth.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/authorize')
def authorize():
    """
    Callback de Google después de la autenticación.
    Aquí se intercambia el código por un token y se obtiene la información del usuario.
    """
    try:
        # Intercambia el código de autorización por un token de acceso
        token = oauth.google.authorize_access_token()
        
        # Obtiene la información del usuario desde Google usando el endpoint de userinfo
        resp = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo')
        user_info = resp.json()
        
        if not user_info:
            flash("No se pudo obtener la información del usuario desde Google.", "danger")
            return redirect(url_for('index'))

    except Exception as e:
        flash(f"Error al autenticar con Google: {e}", "danger")
        return redirect(url_for('index'))

    # Busca o crea un nuevo usuario en la base de datos
    google_id = user_info.get('id')  # El endpoint userinfo usa 'id' en lugar de 'sub'
    email = user_info.get('email')
    nombre_completo = user_info.get('name')
    google_picture = user_info.get('picture')

    usuario = Usuario.query.filter_by(google_id=google_id).first()

    if not usuario:
        # Si no existe, crea un nuevo usuario
        usuario = Usuario(
            google_id=google_id,
            email=email,
            nombre_completo=nombre_completo,
            google_picture=google_picture,
            username=email.split('@')[0] # Usar parte del email como username inicial
        )
        db.session.add(usuario)
        db.session.commit()
        flash("¡Bienvenido! Tu cuenta ha sido creada.", "success")
    
    # Inicia sesión con Flask-Login
    login_user(usuario, remember=True)
    
    # Actualiza el último acceso
    usuario.actualizar_ultimo_acceso()

    # Redirige a completar el perfil si es necesario
    if not usuario.profile_completed:
        return redirect(url_for('auth.complete_profile'))
    
    return redirect(url_for('index'))

@auth_bp.route('/logout')
@login_required
def logout():
    """
    Cierra la sesión del usuario.
    """
    logout_user()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for('index'))

@auth_bp.route('/complete_profile', methods=['GET', 'POST'])
@login_required
def complete_profile():
    """
    Página para que los usuarios completen su perfil después del registro.
    """
    if request.method == 'POST':
        current_user.ultima_unidad_educativa = request.form.get('institucion_educativa_secundaria')
        current_user.nivel_academico_actual = request.form.get('nivel_academico_actual')
        if current_user.nivel_academico_actual == 'otro':
            current_user.nivel_academico_otro = request.form.get('nivel_academico_otro')
        current_user.ciudad = request.form.get('ciudad')
        current_user.whatsapp = request.form.get('whatsapp')
        current_user.carrera_interes = request.form.get('carrera_interes')
        current_user.profile_completed = True
        
        db.session.commit()
        
        flash("¡Perfil completado! Gracias por la información.", "success")
        return redirect(url_for('index'))
        
    return render_template('auth/complete_profile.html')

@auth_bp.route('/profile')
@login_required
def profile():
    """
    Página del perfil del usuario.
    """
    from datetime import datetime
    now = datetime.now()
    return render_template('auth/profile.html', usuario=current_user, now=now)

@auth_bp.route('/admin/users')
@login_required
def admin_users():
    """
    Página para administrar usuarios (solo para administradores).
    """
    if not current_user.es_admin:
        flash("No tienes permisos para acceder a esta página.", "danger")
        return redirect(url_for('index'))
    
    usuarios = Usuario.query.all()
    
    # Estadísticas adicionales
    total_usuarios = len(usuarios)
    usuarios_activos = len([u for u in usuarios if u.es_activo])
    usuarios_premium = len([u for u in usuarios if u.is_premium_active()])
    usuarios_google = len([u for u in usuarios if u.auth_provider == 'google'])
    
    return render_template('auth/admin_users.html', 
                         usuarios=usuarios,
                         total_usuarios=total_usuarios,
                         usuarios_activos=usuarios_activos,
                         usuarios_premium=usuarios_premium,
                         usuarios_google=usuarios_google)

@auth_bp.route('/admin/toggle_user/<int:user_id>')
@login_required
def admin_toggle_user(user_id):
    """
    Activa o desactiva un usuario (solo para administradores).
    """
    if not current_user.es_admin:
        flash("No tienes permisos para realizar esta acción.", "danger")
        return redirect(url_for('index'))
    
    usuario = Usuario.query.get_or_404(user_id)
    
    # No permitir desactivar tu propia cuenta
    if usuario.id == current_user.id:
        flash("No puedes desactivar tu propia cuenta.", "danger")
        return redirect(url_for('auth.admin_users'))
    
    # Cambiar estado
    usuario.es_activo = not usuario.es_activo
    db.session.commit()
    
    estado = "activada" if usuario.es_activo else "desactivada"
    flash(f"Cuenta de {usuario.username} {estado} correctamente.", "success")
    
    return redirect(url_for('auth.admin_users'))





@auth_bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    """
    Actualiza el perfil del usuario mediante AJAX.
    """
    try:
        # Obtener datos del formulario
        nombre_completo = request.form.get('nombre_completo', '').strip()
        ultima_unidad_educativa = request.form.get('ultima_unidad_educativa', '').strip()
        nivel_academico_actual = request.form.get('nivel_academico_actual', '').strip()
        nivel_academico_otro = request.form.get('nivel_academico_otro', '').strip()
        ciudad = request.form.get('ciudad', '').strip()
        whatsapp = request.form.get('whatsapp', '').strip()
        carrera_interes = request.form.get('carrera_interes', '').strip()
        intereses = request.form.get('intereses', '').strip()
        acepta_anuncios = 'acepta_anuncios' in request.form
        
        # Validaciones básicas
        if not nombre_completo:
            return {'success': False, 'message': 'El nombre completo es obligatorio'}
        
        # Actualizar campos del usuario
        current_user.nombre_completo = nombre_completo
        current_user.ultima_unidad_educativa = ultima_unidad_educativa or None
        
        # Manejar nivel académico
        if nivel_academico_actual == 'otro':
            current_user.nivel_academico_actual = nivel_academico_otro
            current_user.nivel_academico_otro = nivel_academico_otro
        else:
            current_user.nivel_academico_actual = nivel_academico_actual
            current_user.nivel_academico_otro = None
        
        current_user.ciudad = ciudad or None
        current_user.whatsapp = whatsapp or None
        current_user.carrera_interes = carrera_interes or None
        current_user.intereses = intereses or None
        current_user.acepta_anuncios = acepta_anuncios
        
        # Marcar perfil como completado si no lo estaba
        if not current_user.profile_completed:
            current_user.profile_completed = True
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Perfil actualizado correctamente'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error al actualizar perfil: {str(e)}'})

@auth_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    """
    Elimina la cuenta del usuario.
    """
    try:
        # Obtener el ID del usuario antes de eliminarlo
        user_id = current_user.id
        
        # Eliminar todas las sesiones del usuario
        from models import SesionUsuario
        sesiones = SesionUsuario.query.filter_by(usuario_id=user_id).all()
        for sesion in sesiones:
            db.session.delete(sesion)
        
        # Eliminar el usuario
        db.session.delete(current_user)
        db.session.commit()
        
        # Cerrar sesión
        logout_user()
        
        return jsonify({'success': True, 'message': 'Cuenta eliminada correctamente'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error al eliminar cuenta: {str(e)}'})

@auth_bp.route('/admin/toggle_admin/<int:user_id>')
@login_required
def admin_toggle_admin(user_id):
    """
    Convierte un usuario en administrador o viceversa (solo para administradores).
    """
    if not current_user.es_admin:
        flash("No tienes permisos para realizar esta acción.", "danger")
        return redirect(url_for('index'))
    
    usuario = Usuario.query.get_or_404(user_id)
    
    # No permitir desactivar tu propia cuenta de admin
    if usuario.id == current_user.id:
        flash("No puedes cambiar tu propio estado de administrador.", "danger")
        return redirect(url_for('auth.admin_users'))
    
    # Cambiar estado de administrador
    usuario.es_admin = not usuario.es_admin
    db.session.commit()
    
    estado = "administrador" if usuario.es_admin else "usuario normal"
    flash(f"{usuario.username} ahora es {estado}.", "success")
    
    return redirect(url_for('auth.admin_users'))

@auth_bp.route('/admin/grant_premium/<int:user_id>', methods=['POST'])
@login_required
def admin_grant_premium(user_id):
    """
    Otorga premium a un usuario (solo para administradores).
    """
    if not current_user.es_admin:
        return jsonify({'success': False, 'message': 'No tienes permisos para realizar esta acción.'})
    
    try:
        usuario = Usuario.query.get_or_404(user_id)
        tipo = request.form.get('tipo', 'mensual')
        duracion = int(request.form.get('duracion', 30))
        razon = request.form.get('razon', 'Otorgado por administrador')
        
        # Validar tipo de premium
        tipos_validos = ['mensual', 'anual', 'permanente']
        if tipo not in tipos_validos:
            return jsonify({'success': False, 'message': 'Tipo de premium inválido.'})
        
        # Otorgar premium
        usuario.grant_premium(tipo=tipo, duracion_dias=duracion, razon=razon)
        
        return jsonify({
            'success': True, 
            'message': f'Premium {tipo} otorgado a {usuario.username} exitosamente.'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error al otorgar premium: {str(e)}'})

@auth_bp.route('/admin/revoke_premium/<int:user_id>', methods=['POST'])
@login_required
def admin_revoke_premium(user_id):
    """
    Revoca premium a un usuario (solo para administradores).
    """
    if not current_user.es_admin:
        return jsonify({'success': False, 'message': 'No tienes permisos para realizar esta acción.'})
    
    try:
        usuario = Usuario.query.get_or_404(user_id)
        razon = request.form.get('razon', 'Revocado por administrador')
        
        usuario.revoke_premium(razon=razon)
        
        return jsonify({
            'success': True, 
            'message': f'Premium revocado a {usuario.username} exitosamente.'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error al revocar premium: {str(e)}'})

@auth_bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    """
    Elimina un usuario (solo para administradores).
    """
    if not current_user.es_admin:
        return jsonify({'success': False, 'message': 'No tienes permisos para realizar esta acción.'})
    
    try:
        usuario = Usuario.query.get_or_404(user_id)
        
        # No permitir eliminar tu propia cuenta
        if usuario.id == current_user.id:
            return jsonify({'success': False, 'message': 'No puedes eliminar tu propia cuenta.'})
        
        # No permitir eliminar otros administradores
        if usuario.es_admin:
            return jsonify({'success': False, 'message': 'No puedes eliminar cuentas de administrador.'})
        
        # Eliminar sesiones del usuario
        from models import SesionUsuario
        sesiones = SesionUsuario.query.filter_by(usuario_id=user_id).all()
        for sesion in sesiones:
            db.session.delete(sesion)
        
        # Eliminar usuario
        db.session.delete(usuario)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Usuario {usuario.username} eliminado exitosamente.'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error al eliminar usuario: {str(e)}'})

@auth_bp.route('/admin/bulk_actions', methods=['POST'])
@login_required
def admin_bulk_actions():
    """
    Realiza acciones masivas en usuarios (solo para administradores).
    """
    if not current_user.es_admin:
        return jsonify({'success': False, 'message': 'No tienes permisos para realizar esta acción.'})
    
    try:
        action = request.form.get('action')
        user_ids = request.form.getlist('user_ids[]')
        
        if not user_ids:
            return jsonify({'success': False, 'message': 'No se seleccionaron usuarios.'})
        
        usuarios = Usuario.query.filter(Usuario.id.in_(user_ids)).all()
        
        if action == 'activate':
            for usuario in usuarios:
                if not usuario.es_admin or usuario.id != current_user.id:
                    usuario.es_activo = True
            db.session.commit()
            return jsonify({'success': True, 'message': f'{len(usuarios)} usuarios activados.'})
            
        elif action == 'deactivate':
            for usuario in usuarios:
                if not usuario.es_admin or usuario.id != current_user.id:
                    usuario.es_activo = False
            db.session.commit()
            return jsonify({'success': True, 'message': f'{len(usuarios)} usuarios desactivados.'})
            
        elif action == 'delete':
            # Solo eliminar usuarios no admin
            usuarios_a_eliminar = [u for u in usuarios if not u.es_admin and u.id != current_user.id]
            
            for usuario in usuarios_a_eliminar:
                # Eliminar sesiones
                from models import SesionUsuario
                sesiones = SesionUsuario.query.filter_by(usuario_id=usuario.id).all()
                for sesion in sesiones:
                    db.session.delete(sesion)
                # Eliminar usuario
                db.session.delete(usuario)
            
            db.session.commit()
            return jsonify({'success': True, 'message': f'{len(usuarios_a_eliminar)} usuarios eliminados.'})
            
        else:
            return jsonify({'success': False, 'message': 'Acción no válida.'})
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error en acción masiva: {str(e)}'})
