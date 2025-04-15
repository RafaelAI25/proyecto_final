import hashlib # generar los hashes de las contraseñas

# Función para generar un hash de la contraseña
def hash_password(password):
    # Usamos SHA-256 para hashear la contraseña
    return hashlib.sha256(password.encode()).hexdigest()

def verificar_password(password, hashed_password):
    # Verificamos si la contraseña ingresada coincide con el hash almacenado
    return hash_password(password) == hashed_password
