import serial
import serial.tools.list_ports


def find_port():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if "USB" in p.description or "USB" in p.device:
            return p.device
    return None


class ArduinoClient:
    def __init__(self, port, baudrate: int = 9600) -> None:
        self.port = port or None
        self.connection = None
        self.baudrate = baudrate
        self.active = False

    def connect(self):
        """Відкриває з'єднання"""
        if self.port:
            try:
                self.connection = serial.Serial(self.port, self.baudrate, timeout=1)
                print(f"Connected to {self.port}")
                self.active = True
                return True
            except serial.SerialException as e:
                print(f"Connection error: {e}")
        else:
            print("Arduino not found")
        self.active = False
        return False

    def write(self, command):
        """Надсилає команду в порт"""
        if self.connection and self.connection.is_open:
            print(command)
            self.connection.write(command.encode('utf-8'))
            return True
        return False

    def close(self):
        """Закриває порт та скидає стан"""
        if self.connection:
            try:
                self.connection.close()
            except Exception as e:
                print(f"Error while closing: {e}")
            finally:
                self.connection = None  # Очищаємо об'єкт
                self.active = False
                self.port = None  # Дозволяємо повторний пошук
                print("Connection closed and port reset")
