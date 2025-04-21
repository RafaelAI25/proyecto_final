import sqlite3 # importamos el modulo SQLite3

# Función para inicializar la base de datos
def init_db():
    # Conectamos a la base de datos (o la creamos si no existe)
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Creamos la tabla Pacientes si no existe
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL,
            diagnostico TEXT NOT NULL
        )
    ''')

    # Creamos la tabla de Usuarios si no existe
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            contraseña TEXT NOT NULL
        )
    ''')
  
    conn.commit()  # Guardamos los cambios
    conn.close()   # Cerramos la conexión


# Función para agregar un nuevo paciente
def agregar_paciente(nombre, edad, diagnostico):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Pacientes (nombre, edad, diagnostico)
        VALUES (?, ?, ?)
    ''', (nombre, edad, diagnostico))
    conn.commit()
    conn.close()


import sqlite3

# Función para obtener todos los pacientes con paginación y filtro
def obtener_pacientes(filtro='', pagina=1, por_pagina=5):
    # Calcular el desplazamiento para la paginación
    offset = (pagina - 1) * por_pagina
    
    try:
        # Usar 'with' para manejar la conexión a la base de datos
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()

            # Si proporcionamos un filtro, realizamos la búsqueda filtrada por nombre o diagnóstico
            if filtro:
                consulta = '''
                    SELECT * FROM Pacientes
                    WHERE nombre LIKE ? OR diagnostico LIKE ?
                    LIMIT ? OFFSET ?
                '''
                parametros = ('%' + filtro + '%', '%' + filtro + '%', por_pagina, offset)

                cursor.execute(consulta, parametros)  # Ejecutamos la consulta con los parámetros
            else:
                # Si no proporcionamos un filtro, obtenemos todos los pacientes
                consulta = '''
                    SELECT * FROM Pacientes
                    LIMIT ? OFFSET ?
                '''
                parametros = (por_pagina, offset)
                cursor.execute(consulta, parametros)
            
            pacientes = cursor.fetchall()

            # Si proporcionamos un filtro, obtenemos el total de pacientes filtrados
            if filtro:
                cursor.execute('SELECT COUNT(*) FROM Pacientes WHERE nombre LIKE ? OR diagnostico LIKE ?', 
                               ('%' + filtro + '%', '%' + filtro + '%'))
            else:
                cursor.execute('SELECT COUNT(*) FROM Pacientes')

            total_pacientes = cursor.fetchone()[0]

            return pacientes, total_pacientes

    except sqlite3.Error as e:
        # Mejor manejo del error
        print(f"Error al conectar a la base de datos: {e}")
        return [], 0  # Retorna lista vacía y 0 pacientes en caso de error


# Función para obtener un paciente por su ID
def obtener_paciente_por_id(id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Pacientes WHERE id = ?', (id,))
    paciente = cursor.fetchone()
    conn.close()
    return paciente



# Función para actualizar un paciente
def actualizar_paciente(id, nombre, edad, diagnostico):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Pacientes
        SET nombre = ?, edad = ?, diagnostico = ?
        WHERE id = ?
    ''', (nombre, edad, diagnostico, id))
    conn.commit()
    conn.close()

# Función para eliminar un paciente
def eliminar_paciente(id):
    # Conectamos a la base de datos
    conn = sqlite3.connect('data.db')
    # Creamos un cursor para ejecutar comandos SQL
    cursor = conn.cursor()
    # Ejecutamos el comando SQL para eliminar el paciente con el ID especificado
    cursor.execute('DELETE FROM Pacientes WHERE id = ?', (id,))
    # Guardamos los cambios en la base de datos
    conn.commit()
    # Cerramos la conexión a la base de datos
    conn.close()
    
