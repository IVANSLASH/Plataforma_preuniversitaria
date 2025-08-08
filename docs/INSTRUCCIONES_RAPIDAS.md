# ⚡ INSTRUCCIONES RÁPIDAS - Plataforma Preuniversitaria

## 🚀 **INICIO RÁPIDO DE LA APLICACIÓN WEB**

### 1. **Instalar y Configurar (PRIMERA VEZ)**
```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (crear archivo .env)
cp .env.example .env  # Editar con tus credenciales de Google OAuth
```

### 2. **Ejecutar la Aplicación**
```bash
# Iniciar servidor Flask
python app.py
```
**Aplicación disponible en:** http://localhost:5000

### 3. **Primer Uso**
1. **Registrarse**: Usar Google OAuth en la página principal
2. **Explorar ejercicios**: Navegar por las materias disponibles
3. **Resolver ejercicios**: Hacer clic en cualquier ejercicio para ver detalle
4. **Generar simulacros**: Crear exámenes personalizados

---

## 👤 **TIPOS DE USUARIOS Y LÍMITES**

### **Sin Registro**
- ✅ **5 ejercicios por día** gratis
- ❌ Sin descarga de PDFs
- ❌ Sin seguimiento de progreso

### **Usuario Registrado** (Google OAuth)
- ✅ **15 ejercicios por día**
- ✅ Seguimiento de progreso
- ✅ Historial de ejercicios vistos
- ❌ Descargas limitadas

### **Usuario Premium**
- ✅ **Ejercicios ilimitados**
- ✅ Descargas de PDFs sin límite
- ✅ Estadísticas avanzadas
- ✅ Soporte prioritario
- ✅ Contenido exclusivo

---

## 🔧 **COMANDOS DE ADMINISTRACIÓN**

| Acción | Comando |
|--------|---------|
| Iniciar aplicación | `python app.py` |
| Crear administrador | `python hacer_admin.py` |
| Otorgar premium | `python otorgar_premium.py` |
| Exportar ejercicios | `python exportador/exportar_json_nuevo.py` |
| Generar simulacro | Usar interfaz web en `/simulacro` |

---

## 📁 **MATERIAS Y EJERCICIOS DISPONIBLES**

### **Matemáticas Preuniversitaria (MATU)**
- 📐 **Álgebra**: 6 ejercicios disponibles
- 📊 **Funciones**: 2 ejercicios disponibles  
- 📏 **Geometría**: 2 ejercicios disponibles

### **Física Preuniversitaria (FISU)**
- ⚡ **Dinámica**: 2 ejercicios disponibles

```
ejercicios_nuevo/
├── matematicas_preuniversitaria/
│   ├── algebra/     (MATU_ALG_001-006)
│   ├── funciones/   (MATU_FUN_007-008)
│   └── geometria/   (MATU_GEO_010-011)
└── fisica_preuniversitaria/
    └── dinamica/    (FISU_DIN_001, FISU_CIN_009)
```

---

## 🌐 **NAVEGACIÓN DE LA APLICACIÓN WEB**

### **Páginas Principales:**
| Página | URL | Descripción |
|--------|-----|-------------|
| **Inicio** | `/` | Lista de ejercicios con filtros |
| **Ejercicio** | `/ejercicio/<id>` | Detalle y solución |
| **Simulacros** | `/simulacro` | Generar examen personalizado |
| **Teoría** | `/teoria` | Contenido teórico por materias |
| **Formularios** | `/formularios` | Fórmulas descargables |
| **Premium** | `/premium` | Planes de suscripción |
| **Perfil** | `/profile` | Configuración de usuario |

### **Panel de Administración** (Solo admins):
- **Usuarios**: `/admin/users` - Gestión de usuarios
- **Estadísticas**: `/estadisticas` - Métricas de uso

---

## ⚠️ **FUNCIONALIDADES CLAVE**

### ✅ **Para Estudiantes:**
- 🔐 **Autenticación Google**: Registro e inicio de sesión seguro
- 📊 **Límites diarios**: Sistema de restricción transparente
- 🎯 **Simulacros personalizados**: Exámenes por materia y capítulo
- 📚 **Teoría integrada**: Contenido de apoyo
- 📱 **Interfaz responsive**: Compatible con móviles

### 🛠️ **Para Administradores:**
- 👥 **Gestión de usuarios**: Panel completo de administración
- 💎 **Sistema premium**: Otorgar y revocar suscripciones
- 📈 **Estadísticas**: Métricas de uso detalladas
- 🔧 **Scripts de utilidad**: Herramientas de mantenimiento

---

## 🆘 **SOLUCIÓN DE PROBLEMAS**

### **Problemas Comunes de la Aplicación:**
| Problema | Solución |
|----------|----------|
| "OAuth Error" | Verificar credenciales Google en `.env` |
| "Base de datos no encontrada" | Se crea automáticamente al iniciar |
| "Puerto ocupado" | Cambiar puerto con `FLASK_RUN_PORT=5001` |
| "Límite alcanzado" | Registrarse o adquirir premium |
| "Ejercicio no carga" | Verificar ID en base de datos |

### **Problemas de Google OAuth:**
1. ✅ Verificar `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET`
2. ✅ Verificar URIs autorizadas en Google Console
3. ✅ Verificar APIs habilitadas (Google+ API)

---

## 📚 **RECURSOS ADICIONALES**

### **Documentación:**
- **Instalación completa**: `docs/INSTALACION.md`
- **Códigos de materias**: `docs/CODIGOS_MATERIAS.md`
- **Sistema de límites**: `docs/SISTEMA_LIMITES_DIARIOS.md`
- **Guía de incorporación**: `docs/GUIA_INCORPORAR_PROBLEMAS.md`

### **Scripts de Utilidad:**
- `hacer_admin.py` - Crear administrador
- `otorgar_premium.py` - Gestionar cuentas premium  
- `exportador/exportar_json_nuevo.py` - Exportar ejercicios

### **Archivos de Configuración:**
- `requirements.txt` - Dependencias Python
- `.env` - Variables de entorno (crear manualmente)
- `config.py` - Configuraciones Flask

---

## 🎯 **CHECKLIST DE INSTALACIÓN**

### **Configuración Inicial:**
- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` creado con credenciales Google OAuth
- [ ] Credenciales Google OAuth configuradas
- [ ] Aplicación iniciada (`python app.py`)

### **Verificación:**
- [ ] Página principal carga correctamente
- [ ] Autenticación Google funciona
- [ ] Ejercicios se muestran correctamente
- [ ] Límites diarios funcionan
- [ ] Simulacros se generan

### **Para Administradores:**
- [ ] Cuenta de administrador creada
- [ ] Panel admin accesible
- [ ] Estadísticas funcionan

---

## 🚀 **PRÓXIMOS PASOS**

1. **Usar la aplicación**: Explorar ejercicios y funcionalidades
2. **Configurar premium**: Si necesitas acceso ilimitado
3. **Administrar usuarios**: Panel de administración
4. **Personalizar**: Modificar estilos y contenido según necesidades

**¡Tu Plataforma Preuniversitaria está lista! 🎉** 