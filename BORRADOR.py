import random

# Clase que representa un dado
class Dado:
    def __init__(self):
        self.valor = 0  # Valor actual del dado

    def lanzar(self):
        # Genera un valor aleatorio entre 1 y 6
        self.valor = random.randint(1, 6)
        return self.valor

# Clase que representa a un jugador
class Jugador:
    def __init__(self, nombre, saldo):
        self.nombre = nombre  # Nombre del jugador
        self.saldo = saldo  # Saldo actual del jugador
        self.historial = []  # Historial de apuestas del jugador

    def apostar(self, cantidad):
        # Verifica si el jugador tiene suficiente saldo para la apuesta
        if cantidad > self.saldo:
            raise ValueError("Saldo insuficiente para la apuesta.")
        self.saldo -= cantidad  # Deduce la cantidad apostada del saldo
        return cantidad

    def ganar(self, cantidad):
        # Aumenta el saldo del jugador con la cantidad ganada
        self.saldo += cantidad

    def registrar_historial(self, apuesta, resultado, gano):
        # Registra una entrada en el historial de apuestas
        self.historial.append({
            'apuesta': apuesta,
            'resultado': resultado,
            'gano': gano
        })

    def obtener_historial(self):
        # Devuelve el historial completo de apuestas
        return self.historial

# Clase que representa el juego Lucky Dice
class JuegoLuckyDice:
    def __init__(self, jugador):
        self.jugador = jugador  # Instancia del jugador
        self.dado1 = Dado()  # Primer dado
        self.dado2 = Dado()  # Segundo dado
        self.jackpot_cantidad = 0.2  # Porcentaje del saldo que se otorga como jackpot
        self.limite_min_apuesta = 10  # Límite mínimo para apuestas
        self.limite_max_apuesta = 500  # Límite máximo para apuestas

    def jugar(self, apuesta, tipo_apuesta):
        # Verifica si la apuesta está dentro de los límites permitidos
        if not self.verificar_limites(apuesta):
            print("La apuesta está fuera de los límites permitidos.")
            return

        cantidad_apostada = self.jugador.apostar(apuesta)  # Realiza la apuesta
        resultado1 = self.dado1.lanzar()  # Lanza el primer dado
        resultado2 = self.dado2.lanzar()  # Lanza el segundo dado
        resultado = (resultado1, resultado2)  # Guarda los resultados de los dados
        gano = self.evaluar_apuesta(tipo_apuesta, resultado)  # Evalúa si el jugador ganó
        
        if gano:
            cantidad_ganada = cantidad_apostada * 2  # Calcula la cantidad ganada (doble de la apuesta)
            self.jugador.ganar(cantidad_ganada)  # Actualiza el saldo del jugador
            self.jugador.registrar_historial(tipo_apuesta, resultado, True)  # Registra la apuesta ganadora
            if self.verificar_jackpot(resultado1, resultado2):
                bonificacion = self.jackpot_cantidad * self.jugador.saldo  # Calcula la bonificación por jackpot
                self.jugador.ganar(bonificacion)  # Añade la bonificación al saldo
                print(f"¡Jackpot ganado! Bonificación de {bonificacion:.2f} agregada.")
        else:
            self.jugador.registrar_historial(tipo_apuesta, resultado, False)  # Registra la apuesta perdida

        # Muestra el resultado y el saldo actual
        print(f"Resultado: {resultado}")
        print(f"Saldo actual: {self.jugador.saldo}")

    def evaluar_apuesta(self, tipo_apuesta, resultado):
        # Evalúa si el resultado de los dados cumple con el tipo de apuesta
        if tipo_apuesta == "Alto":
            return resultado[0] + resultado[1] > 7
        elif tipo_apuesta == "Bajo":
            return resultado[0] + resultado[1] <= 7
        elif tipo_apuesta == "Número Específico":
            num = int(input("Ingresa el número específico (1-6): "))
            return resultado[0] == num or resultado[1] == num
        elif tipo_apuesta == "Dobles":
            return resultado[0] == resultado[1]
        return False

    def verificar_jackpot(self, resultado1, resultado2):
        # Verifica si se ha ganado el jackpot
        return resultado1 == 6 and resultado2 == 6  # Jackpot si ambos dados muestran 6

    def otorgar_bonificacion(self):
        # Lógica para otorgar bonificaciones adicionales (por definir)
        pass

    def verificar_limites(self, apuesta):
        # Verifica si la apuesta está dentro del rango permitido
        return self.limite_min_apuesta <= apuesta <= self.limite_max_apuesta

    def mostrar_historial(self):
        # Muestra el historial de apuestas del jugador
        historial = self.jugador.obtener_historial()
        for entry in historial:
            print(f"Apuesta: {entry['apuesta']}, Resultado: {entry['resultado']}, Ganó: {entry['gano']}")

# Ejemplo de uso del juego
if __name__ == "__main__":
    nombre = input("Ingresa el nombre del jugador: ")
    saldo_inicial = int(input("Ingresa el saldo inicial del jugador: "))
    
    jugador = Jugador(nombre, saldo_inicial)  # Crea una instancia del jugador
    juego = JuegoLuckyDice(jugador)  # Crea una instancia del juego

    while True:
        # Menú de opciones para el usuario
        print("\nOpciones:")
        print("1. Realizar apuesta")
        print("2. Mostrar historial")
        print("3. Salir")
        opcion = input("Elige una opción (1/2/3): ")

        if opcion == "1":
            apuesta = int(input("Ingresa la cantidad a apostar: "))
            tipo_apuesta = input("Ingresa el tipo de apuesta (Alto, Bajo, Número Específico, Dobles): ")
            juego.jugar(apuesta, tipo_apuesta)  # Realiza la apuesta
        elif opcion == "2":
            juego.mostrar_historial()  # Muestra el historial de apuestas
        elif opcion == "3":
            print("Gracias por jugar. ¡Hasta luego!")  # Mensaje de despedida
            break
        else:
            print("Opción no válida. Por favor, elige nuevamente.")  # Mensaje de opción inválida
