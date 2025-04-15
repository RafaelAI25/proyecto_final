from flask import Flask, request, render_template, redirect, url_for, session, flash

import db
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Genera una clave secreta segura para producción


# Inicializar la base de datos
db.init_db()


@app.route('/')
def index():
    # obtener la lista de pacientes de la base de datos
    pacientes = db.obtener_pacientes()
    return render_template('index.html', pacientes=pacientes)


@app.route('/nuevo_paciente', methods=['GET', 'POST'])
def nuevo_paciente():
    if request.method == 'POST':
        # obtener los datos del formulario
        nombre = request.form['nombre']
        edad = request.form['edad']
        diagnostico = request.form['diagnostico']
        
        if not nombre or not edad or not diagnostico:
            flash('Por favor, completa todos los campos son obligatorios.')
            return redirect(url_for('nuevo_paciente'))

        # agregar el nuevo paciente a la base de datos
        db.agregar_paciente(nombre, edad, diagnostico)
        flash('Paciente agregado exitosamente.')
                
        # redirigir a la página principal
        return redirect(url_for('index'))
      
    # Si la solicitud es GET, simplemente renderizamos el formulario
    return render_template('nuevo_paciente.html')


app.run(host= '0.0.0.0', port=5000, debug=True)

