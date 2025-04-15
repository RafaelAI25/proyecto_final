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


# Función para obtener todos los pacientes
def obtener_pacientes():
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Pacientes')
        pacientes = cursor.fetchall()
        conn.close()
        return pacientes
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return []
    

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
    