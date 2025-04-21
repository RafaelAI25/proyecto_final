from flask import Flask, request, render_template, redirect, url_for, session, flash

import db
import secrets

""" import logging

# Configurar el logger
logging.basicConfig(level=logging.DEBUG)  # Puedes cambiar el nivel a INFO, WARNING, ERROR, etc. """

app = Flask(__name__)
print(secrets.token_hex(32))  # Genera una clave secreta segura para producción
app.secret_key = secrets.token_hex(32)  # Genera una clave secreta segura para producción


# Inicializar la base de datos
db.init_db()


@app.route('/')
def index():
    # Obtener el valor del parámetro filtro de la URL, (por ejemplo para buscar pacientes por nombre o diagnóstico)
    # si no se proporciona un filtro se usa una cadena vacia con valor predeterminado
    filtro = request.args.get('filtro', '')

    # Obtener el valor del parametro 'pagina' de la URL, que indica la página actual de los resultados
    # Si no se proporciona, se establece en 1 por defecto
    pagina = int(request.args.get('pagina', 1))

    # definir el número de resultados por página
    por_pagina = 7

    # obtener la lista de pacientes de la base de datos
    pacientes, total = db.obtener_pacientes(filtro=filtro, pagina=pagina, por_pagina=por_pagina)

    # calcula el total de páginas necesarias para mosotrar los resultados, redondeando hacia arriba
    total_paginas = (total + por_pagina - 1) // por_pagina

    # Renderiza la plantilla index, pasando los datos necesarios para mostrar la vista
    return render_template('index.html', pacientes=pacientes, 
                           filtro=filtro, 
                           pagina=pagina, 
                           total_paginas=total_paginas)


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


# Ruta editar un paciente. acepta metodos GET y POST
@app.route('/editar_paciente/<int:id>', methods=['GET', 'POST'])
def editar_paciente(id):
    # obtener el paciente de la base de datos
    paciente = db.obtener_paciente_por_id(id)
    
    # si el formulario fué enviado con el método POST
    if request.method == 'POST':
        # obtener los datos del formulario
        nombre = request.form['nombre']
        edad = request.form['edad']
        diagnostico = request.form['diagnostico']

        # verificar si los campos no están vacios
        if not nombre or not edad or not diagnostico:
            flash('Por favor, completa todos los campos son obligatorios.')
            return redirect(url_for('editar_paciente', id=id))

        # actualizar el paciente en la base de datos
        db.actualizar_paciente(id, nombre, int(edad), diagnostico)
        flash('Paciente actualizado exitosamente.')
        
        # redirigir a la página principal
        return redirect(url_for('index'))
    
    # Si la solicitud es GET, simplemente renderizamos el formulario
    return render_template('editar_paciente.html', paciente=paciente)


# define una ruta que responda a solicitudes POST para eliminar un paciente con un ID específico
@app.route('/eliminar_paciente/<int:id>', methods=['POST'])
def eliminar_paciente(id):
    # llamamos a la función eliminar_paciente de db.py
    db.eliminar_paciente(id)
    flash('Paciente eliminado exitosamente.')
    # redirigir a la página principal
    return redirect(url_for('index'))


app.run(host= '0.0.0.0', port=5000, debug=True)

