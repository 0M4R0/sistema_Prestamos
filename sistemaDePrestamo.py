import os
import re
from datetime import datetime

CARPETA_CLIENTES = "clientes/"  # Carpeta para almacenar datos de clientes
EXTENSION = ".txt"              # Extension de los archivos

# Validamos la fecha
def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, "%d/%m/%Y")  # Verifica el formato DD/MM/AAAA
        return True
    except ValueError:
        return False

class Cliente:
    def __init__(self, nombre, apellido, direccion, sector, provincia, telefono, celular, email):
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.sector = sector
        self.provincia = provincia
        self.telefono = telefono
        self.celular = celular
        self.email = email
        self.id_cliente = None  # Asignar un ID unico
        self.prestamos = []     # Lista para almacenar los prestamos del cliente

    # Guadar los datos del cliente en un archivo de texto
    def guardar_datos(self):
        crear_directorio() # Nos aseguramos de que la carpeta exista
        with open(CARPETA_CLIENTES + self.id_cliente + EXTENSION, 'w') as archivo:
            archivo.write(f"Nombre:     {self.nombre}\n")
            archivo.write(f"Apellido:   {self.apellido}\n")
            archivo.write(f"Direccion:  {self.direccion}\n")
            archivo.write(f"Sector:     {self.sector}\n")
            archivo.write(f"Provincia:  {self.provincia}\n")
            archivo.write(f"Telefono:   {self.telefono}\n")
            archivo.write(f"Celular:    {self.celular}\n")
            archivo.write(f"Email:      {self.email}\n")
            archivo.write("PRESTAMOS\n")
            # Guardamos los prestamos del cliente
            for prestamo in self.prestamos:
                archivo.write(f"- Numero de prestamo: {prestamo.numero_prestamo}\n")
                archivo.write(f"  Monto:              {prestamo.monto}\n")
                archivo.write(f"  Tasa de Interes:    {prestamo.tasa_interes}%\n")
                archivo.write(f"  Periodo:            {prestamo.periodo}\n")
                archivo.write(f"  Garantia:           {prestamo.garantia}\n")
                archivo.write(f"  Balance:            {prestamo.balance}\n")
                archivo.write(f"  Cuota mensual:      {prestamo.cuota}\n")

# Creamos la carpeta para los archivos
def crear_directorio():
    # Creamos el directorio en caso de que no exista
    if not os.path.exists(CARPETA_CLIENTES):
        os.makedirs(CARPETA_CLIENTES)

def cargar_cliente(id_cliente):
    try:
        with open(CARPETA_CLIENTES + id_cliente + EXTENSION, "r") as archivo:
            datos = archivo.readlines()
            nombre = datos[0].split(": ")[1].strip()
            apellido = datos[1].split(": ")[1].strip()
            direccion = datos[2].split(": ")[1].strip()
            sector = datos[3].split(": ")[1].strip()
            provincia = datos[4].split(": ")[1].strip()
            telefono = datos[5].split(": ")[1].strip()
            celular = datos[6].split(": ")[1].strip()
            email = datos[7].split(": ")[1].strip()
            cliente = Cliente(nombre, apellido, direccion, sector, provincia, telefono, celular, email)
            cliente.id_cliente = id_cliente

            # Recorre los datos de los prestamos
            for i in range(9, len(datos), 7):  # Cada préstamo ocupa 7 líneas
                numero_prestamo = datos[i].split(": ")[1].strip()
                monto = float(datos[i + 1].split(": ")[1].strip())
                tasa_interes = float(datos[i + 2].split(": ")[1].strip().replace("%", ""))
                periodo = int(datos[i + 3].split(": ")[1].strip())
                garantia = datos[i + 4].split(": ")[1].strip()
                balance = float(datos[i + 5].split(": ")[1].strip())
                cuota = float(datos[i + 6].split(": ")[1].strip())

                # Creamos un objeto Prestamo y luego lo agregamos a la lista de los prestamos del cliente
                prestamo = Prestamo(monto, tasa_interes, periodo, garantia, numero_prestamo)
                prestamo.balance = balance
                prestamo.cuota = cuota
                cliente.prestamos.append(prestamo)
            return cliente
    except FileNotFoundError:
        print('El cliente no existe.')
        return None

class Prestamo:
    def __init__(self, monto, tasa_interes, periodo, garantia, numero_prestamo=None):
        self.monto = monto
        self.tasa_interes = tasa_interes
        self.periodo = periodo
        self.garantia = garantia
        self.numero_prestamo = numero_prestamo or input("Ingrese el número del préstamo: ").strip()
        # Calcula los valores del prestamo
        self.interes, self.monto_total, self.cuota = self.calcular()
        self.balance = self.monto_total
        self.pagos = [] # Lista para registrar los pagos realizados

    # Calculamos el interes, monto total y cuota mensual del prestamo
    def calcular(self):
        monto_interes_mensual = self.monto * (self.tasa_interes / 100)
        monto_total_interes = monto_interes_mensual * self.periodo
        monto_total_prestamo = self.monto + monto_total_interes
        cuota = monto_total_prestamo / self.periodo
        return monto_total_interes, monto_total_prestamo, cuota
    
    # Realizamos el pago y actualizamos el balance
    def realizar_pago(self, monto_pago):
        if monto_pago > self.balance:
            print("El pago no pudo ser efectuado, ya que no tiene el balance suficiente.")
        else:
            self.pagos.append(monto_pago)
            self.balance -= monto_pago
            if self.balance < 0:
                self.balance = 0

    # Mostramos el balance
    def mostrar_balance(self):
        return f"Balance préstamo: RD${self.balance:.2f}"

# Validamos que el numero de telefono no tenga mas de 10 digitos
def validar_telefono(telefono):
    return telefono.isdigit() and len(telefono) == 10 # Verifica que tenga exactamente 10 digitos

# Validamos que el correo tenga un buen formato
def validar_email(email):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron,email) is not None

# Solicitamos los datos al registrar
def registrar_cliente():
    # Utilizamos .strip() para eliminar espacios en blanco
    # Nombre
    nombre = input("Ingrese el nombre del cliente: ")
    while not nombre.strip():
        print("El nombre no puede estar vacio. Intente nuevamente.")
        nombre = input("Ingrese el nombre del cliente: ")

    # Apellido
    apellido = input("Ingrese el apellido del cliente: ")
    while not apellido.strip():
        print("El apellido no puede estar vacio. Intente nuevamente.")
        apellido = input("Ingrese el apellido del cliente: ")

    # Direccion
    direccion = input("Ingrese la dirección del cliente: ")
    while not direccion.strip():
        print("La direccion no puede estar vacia. Intente nuevamente")
        direccion = input("Ingrese la dirección del cliente: ")
    
    # Sector 
    sector = input("Ingrese el sector del cliente: ") 
    while not sector.strip():
        print("El sector no puede estar vacío. Intente nuevamente.")
        sector = input("Ingrese el sector del cliente: ")

    # Provincia
    provincia = input("Ingrese la provincia del cliente: ")
    while not provincia.strip():
        print("La provincia no puede estar vacía. Intente nuevamente.")
        provincia = input("Ingrese la provincia del cliente: ")

    # Telefono
    telefono = input("Ingrese el teléfono del cliente (10 dígitos): ")
    while not validar_telefono(telefono):
        print("El teléfono debe contener solo números y tener exactamente 10 dígitos. Intente nuevamente.")
        telefono = input("Ingrese el teléfono del cliente (10 dígitos): ")

    # Celular
    celular = input("Ingrese el celular del cliente (10 dígitos): ")
    while not validar_telefono(celular):
        print("El celular debe contener solo números y tener exactamente 10 dígitos. Intente nuevamente.")
        celular = input("Ingrese el celular del cliente (10 dígitos): ")

    # Email
    email = input("Ingrese el email del cliente: ")
    while not validar_email(email):
        print("El email no tiene un formato válido. Intente nuevamente.")
        email = input("Ingrese el email del cliente: ")

    cliente = Cliente(nombre, apellido, direccion, sector, provincia, telefono, celular, email)
    cliente.id_cliente = input("Ingrese el ID del cliente: ")

    print(f"\nCliente registrado: {cliente.nombre} {cliente.apellido} (ID del cliente: {cliente.id_cliente})")
    return cliente

def registrar_prestamo(cliente):
    # Ingresamos el monto del prestamo
    while True:
        try:
            monto = float(input("Ingrese el monto del prestamo: "))
            #Verificamos que el monto no sea negativo
            if monto < 0:
                raise ValueError("El monto no puede ser menor a 0. Intente nuevamente.")
            break
        except ValueError as e:
            print("\nError: ", e)

    # Ingresamos la tasa de interes
    while True:
        tasa_interes_input = input("Ingrese la tasa de interes (%): ")
        # Si el usuario pone % lo cambiamos a ""
        if "%" in tasa_interes_input:
            tasa_interes_input = tasa_interes_input.replace("%","")
        try:
            tasa_interes = float(tasa_interes_input)
            if tasa_interes < 0:
                raise ValueError("La tasa de interes no puede ser negativa. Intente nuevamente.")
            break
        except ValueError as e:
            print("\nError: ", e)

    # Preguntamos el periodo del prestamo
    while True:
        try:
            periodo = int(input("Ingrese el periodo del prestamo (en meses): "))
            if periodo < 0:
                raise ValueError("El periodo no puede ser menor a 0. Intente nuevamente")
            break
        except ValueError as e:
            print("\nError: ", e)

    # Preguntamos la garantia del prestamo
    garantia = input("Ingrese la garantia del prestamo (ejemplo: automovil, propiedad, etc.): ")
    while not garantia.strip():
        print("\nLa garantia no puede estar vacia. Intente nuevamente.")
        garantia = input("Ingrese la garantia del prestamo: ")

    # Crear el préstamo
    prestamo = Prestamo(monto, tasa_interes, periodo, garantia)
    prestamo.numero_prestamo = input("Ingrese el número del préstamo: ").strip()
    while not prestamo.numero_prestamo:
        print("El número de préstamo no puede estar vacío. Intente nuevamente.")
        prestamo.numero_prestamo = input("Ingrese el número del préstamo: ").strip()

    cliente.prestamos.append(prestamo)

    # Imprimimos el monto y la cuota 
    print(f"Monto total del prestamo: RD${prestamo.monto_total:.2f}")
    print(f"Cuota mensual: RD${prestamo.cuota:.2f}")

    # Esto para validar si sea hecho un pago 
    pago_realizado = False
    while True:
        if pago_realizado:
            opcion = input("Desea realizar otro pago (s/n): ")
        else:
            opcion = input("Desea realizar un pago (s/n): ")
        
        if opcion.lower() == "s":
            while True:
                try:
                    monto_pago = float(input("Ingrese el monto del pago: "))
                    if monto_pago < 0:
                        raise ValueError("El monto de pago no puede ser menor a 0. Intente nuevamente.")
                    prestamo.realizar_pago(monto_pago)
                    print(prestamo.mostrar_balance())
                    pago_realizado = True
                    break # Salir del bucle si el pago se realizo correctamente
                except ValueError as e:
                    print("\nError: ", e)
        elif opcion.lower() == "n":
            break
        else:
            print("Opcion invalida, por favor elija 's' o 'n'. ")

def registrar_recibo(cliente):
    try:
        if not cliente.prestamos:
            raise ValueError("No hay préstamos registrados para este cliente.")
        
        # Mostrar los préstamos disponibles para que el usuario pueda escoger uno
        print("\nPréstamos disponibles para este cliente:")
        for prestamo in cliente.prestamos:
            print(f" - Número de préstamo: {prestamo.numero_prestamo}")

        numero_prestamo = input("Ingrese el número del préstamo: ")
        fecha = input("Fecha (DD/MM/AAAA): ").strip()
        
        # Validar la fecha
        while not validar_fecha(fecha):
            print("La fecha ingresada no es válida. Intente nuevamente.")
            fecha = input("Fecha (DD/MM/AAAA): ").strip()

        # Busca el préstamo con el número especificado
        prestamo_encontrado = None
        for prestamo in cliente.prestamos:
            if prestamo.numero_prestamo == numero_prestamo:
                prestamo_encontrado = prestamo
                break

        # Si se encuentra el préstamo, se muestran sus detalles
        if prestamo_encontrado:
            print(f"\n--- DETALLES DEL PRÉSTAMO ---")
            print(f"- ID del cliente:             {cliente.id_cliente}")
            print(f"- Fecha:                      {fecha}")
            print(f"- Nombre:                     {cliente.nombre} {cliente.apellido}")
            print(f"- Préstamo:                   RD${prestamo_encontrado.monto:.2f}")
            print(f"- Tasa de interés:            {prestamo_encontrado.tasa_interes}%")
            print(f"- Periodo:                    {prestamo_encontrado.periodo} meses")
            print(f"- Cuota mensual:              RD${prestamo_encontrado.cuota:.2f}")
            print(f"- Monto total del préstamo:   RD${prestamo_encontrado.monto_total:.2f}")
            print(f"- Garantía:                   {prestamo_encontrado.garantia}")
            print(f"- Balance restante:           RD${prestamo_encontrado.balance:.2f}")
        else:
            print("Número de préstamo no encontrado.")

    except ValueError as e:
        print("\nError: ", e)


def main():
    clientes = []
    while True:
        print("\nOpciones:")
        print("1. Nuevo Cliente")
        print("2. Grabar Prestamo")
        print("3. Registrar Recibo")
        print("4. Salir")
        opcion = input("\nSeleccione una opcion (utilizando numero entre 1 y 4): ")

        # Opcion 1: Nuevo Cliente
        if opcion == '1':
            cliente = registrar_cliente()
            clientes.append(cliente)
            cliente.guardar_datos()

        # Opcion 2: Grabar prestamo
        elif opcion == '2':
            id_cliente = input("Ingrese el ID del cliente: ")
            cliente = cargar_cliente(id_cliente)
            if cliente:
                registrar_prestamo(cliente)
                cliente.guardar_datos()
            else:
                print("Cliente no encontrado.")

        # Opcion 3: Registrar Recibo
        elif opcion == '3':
            id_cliente = input("Ingrese el ID del cliente: ")
            cliente = cargar_cliente(id_cliente)
            if cliente:
                registrar_recibo(cliente)
            else:
                print("\nCliente no encontrado")

        # Opcion 4: Salir del sistema
        elif opcion == '4':
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Fuera de rango")

# Llamar a la función principal
main()