import socket
import threading

# 192.168.1.72

class PeerToPeerChat:
    def __init__(self, own_ip, own_port):
        self.own_ip = own_ip
        self.own_port = own_port
        self.neighbours = {}  # Almacena los nombres de los vecinos y sus direcciones IP y puertos
        self.server_socket = None
        self.is_running = True  # Bandera para indicar si el servidor está en ejecución

    def send_message(self, destination_name, message):
        try:
            destination_ip, destination_port = self.neighbours.get(destination_name, (None, None))
            if destination_ip and destination_port:
                # Verifica si la conexión con el vecino está activa
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)  # Establece un tiempo de espera de 1 segundo
                    result = s.connect_ex((destination_ip, destination_port))
                    # result = self.check_neighbours_connection(destination_ip, destination_port)
                    if result == 0:
                        s.send(message.encode())
                        print(f"Mensaje enviado a {destination_name}: {message}")
                    else:
                        print(f"Error: No hay conexión con {destination_name}")
            else:
                print(f"Error: No se encontró el vecino {destination_name}")
        except ConnectionRefusedError:
            print(f"Error: No se pudo conectar con {destination_name}")

    def handle_client(self, client_socket, client_address):
        
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    print(f"\nMensaje recibido de {client_address[0]}:{client_address[1]}: {message}")
                    
                    # Verifica si el mensaje ya se ha recibido antes
                    # if message not in self.received_messages:
                    #     self.received_messages.add(message)

            except ConnectionResetError:
                print(f"Conexión perdida con {client_address}")
                break

    def start_listening(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.own_ip, self.own_port))
            server_socket.listen()
            print(f"Servidor escuchando en {self.own_ip}:{self.own_port}")

            while self.is_running:
                client_socket, client_address = server_socket.accept()
                thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                thread.start()
                print(f'Conexion establecida con {client_address}')

        server_socket.close()  # Cerramos el socket del servidor al salir del bucle

    def add_neighbour(self, neighbour_name, neighbour_ip, neighbour_port):
        self.neighbours[neighbour_name] = (neighbour_ip, neighbour_port)
        print(f"Vecino añadido: {neighbour_name} ({neighbour_ip}:{neighbour_port})")

    def start_chat(self):
        destination_name = input("Ingrese el nombre del destino: ")
        message = input("Ingrese su mensaje: ")
        self.send_message(destination_name, message)

    def stop_server(self):
        message = f'{self.own_ip}:{self.own_port} SHUTDOWN' 
        for neighbour_name, (neighbour_ip, neighbour_port) in self.neighbours.items():
            self.send_message(neighbour_name, message)

        self.is_running = False  # Establecemos la bandera en False para detener el servidor
        print('Servidor Apagado')

    def list_neighbours(self):
        print("--- Lista de Vecinos ---")
        for name, (ip, port) in self.neighbours.items():
            result = self.check_neighbours_connection(ip, port)
            if result:
                print(f"{name}: {ip}:{port} - En linea")
            else:
                print(f"{name}: {ip}:{port} - Sin conexion")

    def check_neighbours_connection(self, ip, port):    
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Establece un tiempo de espera de 1 segundo
            result = s.connect_ex((ip, port))
            if result == 0:
                return True
            else:
                return False


    def scan_local_network(self, start_port, end_port):
        # own_ip = socket.gethostbyname(socket.gethostname())
        local_network_prefix = self.own_ip.rsplit('.', 1)[0] + '.'

        # neighbours = []

        for i in range(1, 255):
            ip = local_network_prefix + str(i)
            if ip != self.own_ip:
                for port in range(start_port, end_port + 1):
                    # print(f"Analizando IP: {ip} Port: {port}")
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(0.05)  # Establece un tiempo de espera corto
                        result = s.connect_ex((ip, port))
                        if result == 0:
                            choice = input(f'Vecino {ip}:{port} encontrado ¿Desea guardar este vecino? S/N: ').upper()
                            if choice == 'S':
                                name = input('Nombre del vecino: ')
                                self.add_neighbour(name, ip, port)
                            break  # Si el puerto está abierto, pasa a la siguiente IP


if __name__ == "__main__":
    own_ip = input("Ingrese su dirección IP: ")
    own_port = int(input("Ingrese su puerto: "))
    peer = PeerToPeerChat(own_ip, own_port)
    
    t1 = threading.Thread(target=peer.start_listening)
    t1.start()

    while (choice := input(
        "\n--- Menú ---\n1. Agregar vecino\n2. Buscar vecinos\n3. Ver lista de vecinos\n4. Enviar mensaje\n5. Apagar servidor\nSeleccione una opción: "
    )) != "6":
        match choice:
            case "1":
                while True:
                    if len(peer.neighbours) > 0:
                        choice = input("¿Desea agregar un vecino? (S/N): ").upper()
                    else:
                        choice = 'S'
                        
                    if choice == "S":
                        while True:
                            num_neighbors_input = input("Ingrese el número de vecinos que desea agregar: ")
                            try:
                                num_neighbors = int(num_neighbors_input)
                                break  # Si se puede convertir a entero, salimos del bucle
                            except ValueError:
                                print("Por favor, ingrese un número válido.")
                        for _ in range(num_neighbors):
                            neighbour_name = input("Ingrese el nombre del vecino: ")
                            neighbour_ip = input("Ingrese la dirección IP del vecino: ")
                            neighbour_port = int(input("Ingrese el puerto del vecino: "))
                            peer.add_neighbour(neighbour_name, neighbour_ip, neighbour_port)
                    elif choice == "N":
                        break
                    
            case "2":
                start_port = int(input('Ingrese el puerto inicial: '))
                end_port = int(input('Ingrese el puerto final: '))
                peer.scan_local_network(start_port, end_port)

            case "3":
                peer.list_neighbours()
                # print("--- Lista de Vecinos ---")
                # for name, (ip, port) in peer.neighbours.items():
                #         print(f"{name}: {ip}:{port}")

            case "4":
                while True:
                    choice = input("¿Desea enviar un mensaje? (S/N): ").upper()
                    if choice == "S":
                        peer.start_chat()
                    elif choice == "N":
                        break

            case "5":
                # peer.notify_neighbours("El servidor se apagará.")
                peer.stop_server()
                t1.join()  # Esperamos a que el hilo termine antes de salir del programa
                break

            case _:
                print("Opción no válida. Intente nuevamente.")