import socket
import sys
from datetime import datetime
import threading

def scan_port(target, port):
    """Escanea un puerto específico en el host objetivo"""
    try:
        # Crea un objeto socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Establece un timeout para la conexión
        s.settimeout(1)
        # Intenta conectarse al puerto
        result = s.connect_ex((target, port))
        # Si el resultado es 0, el puerto está abierto
        if result == 0:
            print(f"Puerto {port}: Abierto")
        s.close()
    except:
        pass

def scan_range(target, start_port, end_port):
    """Escanea un rango de puertos usando múltiples hilos"""
    print(f"Escaneando puertos en {target} desde {start_port} hasta {end_port}")
    print("Iniciando escaneo a las " + str(datetime.now()))
    print("-" * 50)

    threads = []
    for port in range(start_port, end_port + 1):
        # Crea un hilo para cada puerto
        t = threading.Thread(target=scan_port, args=(target, port))
        threads.append(t)
        t.start()

    # Espera a que todos los hilos terminen
    for t in threads:
        t.join()

    print("-" * 50)
    print("Escaneo completado a las " + str(datetime.now()))

if __name__ == "__main__":
    # Obtiene el host objetivo
    if len(sys.argv) == 2:
        target = socket.gethostbyname(sys.argv[1])
    else:
        print("Uso: python port_scanner.py <host>")
        sys.exit()

    try:
        # Escanea los puertos comunes (1-1024)
        scan_range(target, 1, 1024)
    except KeyboardInterrupt:
        print("\nEscaneo interrumpido por el usuario")
        sys.exit()
    except socket.gaierror:
        print("\nNo se pudo resolver el nombre del host")
        sys.exit()
    except socket.error:
        print("\nNo se pudo conectar al servidor")
        sys.exit()
