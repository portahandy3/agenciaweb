import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

# ✅ 1. Crear la app principal
app = Flask(__name__)

# ✅ 2. Configuración de base de datos (local)
# ⚠️ Render no podrá conectarse a tu SQL Server local (solo funciona en tu PC)
# Por eso, cuando lo uses en Render, deberías cambiar a una base de datos online (PostgreSQL, MySQL, etc.)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@DESKTOP-9L8VD9R\\SQLEXPRESS/bd1?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ✅ 3. Configuración de Flask-Mail (usa tu clave de aplicación de Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'portahandy3@gmail.com'
app.config['MAIL_PASSWORD'] = 'kaupsmluydlcdjyb'
app.config['MAIL_DEFAULT_SENDER'] = 'portahandy3@gmail.com'
mail = Mail(app)

# ✅ 4. Modelo de base de datos


class Contacto(db.Model):
    __tablename__ = 'contactos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    empresa = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(50))
    mensaje = db.Column(db.Text)

# ✅ 5. Rutas principales


@app.route('/')
def home():
    return "🚀 Bienvenido a AgenciaWeb — Flask corriendo correctamente en Render!"


@app.route('/inicio')
def index():
    return render_template('index.html')


@app.route('/servicios')
def servicios():
    return render_template('servicios.html')


@app.route('/contactos', methods=['GET', 'POST'])
def contactos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        empresa = request.form['empresa']
        email = request.form['email']
        telefono = request.form['telefono']
        mensaje = request.form['mensaje']

        # Guardar en base de datos
        nuevo_contacto = Contacto(
            nombre=nombre, empresa=empresa, email=email, telefono=telefono, mensaje=mensaje
        )
        db.session.add(nuevo_contacto)
        db.session.commit()

        # Enviar correo
        msg = Message(
            "Nuevo mensaje de contacto recibido",
            recipients=["portahandy3@gmail.com"]
        )
        msg.body = f"""
        ¡Nuevo mensaje desde la web!

        Nombre: {nombre}
        Empresa: {empresa}
        Email: {email}
        Teléfono: {telefono}

        Mensaje:
        {mensaje}
        """
        mail.send(msg)

        return redirect(url_for('gracias'))

    return render_template('contactos.html')


@app.route('/gracias')
def gracias():
    return render_template('gracias.html')


@app.route('/admin')
def admin():
    contactos = Contacto.query.all()
    return render_template('admin.html', contactos=contactos)

# ✅ No incluir app.run() para Render (Gunicorn lo maneja)
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port, debug=False)
