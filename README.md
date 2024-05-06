
# PeerToPeerChat
- Sting Orlando Búritica.
- Bryan Cardona Valencia.
- Juan Felipe Salazar Muñoz.

## Descripción
PeerToPeerChat es una aplicación de chat punto a punto que permite a los usuarios enviar mensajes entre ellos utilizando conexiones TCP directas..

## Funcionalidades
- **Agregar vecinos:** Permite a los usuarios agregar los nombres, direcciones IP y puertos de otros usuarios para establecer conexiones de chat.
- **Buscar vecinos:** Escanea la red local en busca de otros usuarios que estén ejecutando la aplicación y permite agregarlos como vecinos.
- **Ver lista de vecinos:** Muestra una lista de los vecinos actuales y su estado de conexión.
- **Enviar mensaje:** Permite a los usuarios enviar mensajes de chat a sus vecinos.
- **Apagar servidor:** Detiene el servidor de chat y notifica a los vecinos que se va a apagar.

## Uso
1. Ingrese su dirección IP y puerto al iniciar la aplicación.
2. Seleccione una opción del menú:
   - **Agregar vecino:** Agregue manualmente vecinos especificando su nombre, dirección IP y puerto.
   - **Buscar vecinos:** Escanee la red local en busca de vecinos disponibles para agregar.
   - **Ver lista de vecinos:** Muestra una lista de los vecinos actuales y su estado de conexión.
   - **Enviar mensaje:** Envíe mensajes de chat a sus vecinos.
   - **Apagar servidor:** Detiene el servidor de chat y notifica a los vecinos.

## Requisitos
- Python 3.6 o superior
- Librerías estándar de Python (no se requieren instalaciones adicionales)

## Ejecución
1. Clone el repositorio: `git clone https://github.com/tu_usuario/PeerToPeerChat.git`
2. Navegue al directorio del proyecto: `cd PeerToPeerChat`
3. Ejecute la aplicación: `python PeerToPeerChat.py`

## RSA

Para integrar RSA en tu código, primero necesitarás generar un par de claves RSA: una clave privada y una clave pública. Luego, podrás usar estas claves para cifrar y descifrar los mensajes que se envían entre los nodos. Aquí te muestro cómo puedes hacerlo:

Generar un par de claves RSA: Puedes usar la biblioteca cryptography de Python para generar las claves. Aquí te muestro cómo hacerlo:
python


from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

class PeerToPeerChat:
    def __init__(self, own_ip, own_port):
        self.own_ip = own_ip
        self.own_port = own_port
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        
        # Resto del código...

    def get_public_key(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def load_public_key(self, pem_data):
        self.peer_public_key = serialization.load_pem_public_key(pem_data, backend=default_backend())
        
Cifrar y descifrar mensajes: Una vez que tengas las claves generadas, puedes usarlas para cifrar y descifrar mensajes. Aquí te muestro cómo puedes modificar el método send_message para cifrar los mensajes antes de enviarlos y el método handle_client para descifrar los mensajes recibidos:
python


class PeerToPeerChat:

    # Resto del código...

    def send_message(self, destination_name, message):
        try:
            destination_ip, destination_port = self.neighbours.get(destination_name, (None, None))
            if destination_ip and destination_port:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex((destination_ip, destination_port))
                    if result == 0:
                        encrypted_message = self.peer_public_key.encrypt(
                            message.encode(),
                            padding.OAEP(
                                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                algorithm=hashes.SHA256(),
                                label=None
                            )
                        )
                        s.send(encrypted_message)
                        print(f"Mensaje enviado a {destination_name}")
                    else:
                        print(f"Error: No hay conexión con {destination_name}")
            else:
                print(f"Error: No se encontró el vecino {destination_name}")
        except ConnectionRefusedError:
            print(f"Error: No se pudo conectar con {destination_name}")

    def handle_client(self, client_socket, client_address):
        while True:
            try:
                encrypted_message = client_socket.recv(2048)
                if encrypted_message:
                    decrypted_message = self.private_key.decrypt(
                        encrypted_message,
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    )
                    print(f"\nMensaje recibido de {client_address[0]}:{client_address[1]}: {decrypted_message.decode()}")
            except ConnectionResetError:
                print(f"Conexión perdida con {client_address}")
                break
                
Estas modificaciones te permitirán cifrar los mensajes antes de enviarlos y descifrar los mensajes recibidos utilizando RSA. Además, asegúrate de cargar la clave pública del vecino antes de enviar mensajes. Esto es solo un ejemplo básico, y puedes ajustarlo según tus necesidades específicas.
