import datetime

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.tamano = 0

    def esta_vacia(self):
        return self.cabeza is None

    def agregar(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.tamano += 1

    def obtener(self, indice):
        if indice < 0 or indice >= self.tamano:
            raise IndexError("Índice fuera del rango")
        
        actual = self.cabeza
        for _ in range(indice):
            actual = actual.siguiente
        return actual.dato

    def modificar(self, indice, nuevo_dato):
        if indice < 0 or indice >= self.tamano:
            raise IndexError("Índice fuera del rango")
        
        actual = self.cabeza
        for _ in range(indice):
            actual = actual.siguiente
        actual.dato = nuevo_dato

    def intercambiar_nodos(self, indice1, indice2):
        if indice1 < 0 or indice2 < 0 or indice1 >= self.tamano or indice2 >= self.tamano:
            raise IndexError("Índice fuera del rango")
        
        if indice1 == indice2:
            return
    
        anterior1 = None
        actual1 = self.cabeza
        for _ in range(indice1):
            anterior1 = actual1
            actual1 = actual1.siguiente
        
        anterior2 = None
        actual2 = self.cabeza
        for _ in range(indice2):
            anterior2 = actual2
            actual2 = actual2.siguiente
        if anterior1 is not None:
            anterior1.siguiente = actual2
        else:
            self.cabeza = actual2
        
        if anterior2 is not None:
            anterior2.siguiente = actual1
        else:
            self.cabeza = actual1
        
        variable_temp = actual1.siguiente
        actual1.siguiente = actual2.siguiente
        actual2.siguiente = variable_temp

    def mover_n_posiciones(self, indice_actual, n):
        nuevo_indice = indice_actual - n
        
        if nuevo_indice < 0:
            nuevo_indice = 0
        elif nuevo_indice >= self.tamano:
            nuevo_indice = self.tamañno - 1
        
        if nuevo_indice != indice_actual:
            self.intercambiar_nodos(indice_actual, nuevo_indice)
            if abs(n) > 1:
                self.mover_n_posiciones(nuevo_indice, n - (indice_actual - nuevo_indice))

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def __len__(self):
        return self.tamano

class Producto:
    def __init__(self, tipo, fecha_produccion, cantidad):
        self._tipo = tipo
        self._fecha_produccion = fecha_produccion
        self._cantidad = cantidad

    @property
    def tipo(self):
        return self._tipo

    @property
    def fecha_produccion(self):
        return self._fecha_produccion

    @property
    def cantidad(self):
        return self._cantidad

    def mostrar_detalles(self):
        raise NotImplementedError("Método abstracto: debe implementarse en clases hijas")

class Prenda(Producto):
    ESTADOS = ['PROCESO', 'FINALIZADA', 'DEFECTUOSA']
    def __init__(self, tipo, fecha_produccion, cantidad, costo_unidad, estado='PROCESO'):
        super().__init__(tipo, fecha_produccion, cantidad)
        self._costo_unidad = costo_unidad
        self.estado = estado

    @property
    def costo_unidad(self):
        return self._costo_unidad

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        if valor not in self.ESTADOS:
            raise ValueError(f"Estado inválido. Debe ser uno de: {', '.join(self.ESTADOS)}")
        self._estado = valor

    def mostrar_detalles(self):
        return (f"Tipo: {self.tipo}, Fecha: {self.fecha_produccion}, "
                f"Cantidad: {self.cantidad}, CostoXunidad: ${self.costo_unidad:.2f}, "
                f"Estado: {self.estado}")

    def __str__(self):
        return self.mostrar_detalles()

class Fabrica_confecciones:
    def __init__(self):
        self.produccion = ListaEnlazada()
        self.ventas = ListaEnlazada()
        self.total_recaudado = 0.0

    def registrar_prenda(self, tipo, fecha, cantidad, costo_unidad):
        nueva_prenda = Prenda(tipo, fecha, cantidad, costo_unidad)
        self.produccion.agregar(nueva_prenda)
        return nueva_prenda

    def modificar_estado(self, indice, nuevo_estado):
        prenda = self.produccion.obtener(indice)
        prenda.estado = nuevo_estado

    def mover_prenda(self, indice_actual, n_posiciones):
        self.produccion.mover_n_posiciones(indice_actual, n_posiciones)

    def registrar_venta(self, indices):
        total_venta = 0.0 
        prendas_vendidas = []
        
        for indice in sorted(indices, reverse=True):
            if indice < 0 or indice >= len(self.produccion):
                continue
            
            prenda = self.produccion.obtener(indice)
            if prenda.estado == 'FINALIZADA':
                total_venta += prenda.cantidad * prenda.costo_unidad
                prendas_vendidas.append(prenda)
                
        self.total_recaudado += total_venta
        
        if prendas_vendidas:
            self.ventas.agregar({
                'prendas': prendas_vendidas,
                'total': total_venta,
                'fecha': datetime.date.today()
            })
        
        return total_venta

    def mostrar_produccion(self):
        for i, prenda in enumerate(self.produccion):
            print(f"{i}: {prenda}")

    def mostrar_ventas(self):
        for venta in self.ventas:
            print(f"Fecha: {venta['fecha']}, Total: ${venta['total']:.2f}")
            for prenda in venta['prendas']:
                print(f"  - {prenda.tipo} x{prenda.cantidad}")

    def calcular_estadisticas(self):
        estadisticas = {
            'total_ingresos': self.total_recaudado,
            'total_producidas': 0,
            'total_finalizadas': 0,
            'total_defectuosas': 0,
            'promedio_por_tipo': {},
            'ingresos_por_tipo': {}
        }

        contador_tipos = {}
        cantidad_tipos = {}

        for prenda in self.produccion:
            estadisticas['total_producidas'] += prenda.cantidad
            
            if prenda.estado == 'FINALIZADA':
                estadisticas['total_finalizadas'] += prenda.cantidad
            elif prenda.estado == 'DEFECTUOSA':
                estadisticas['total_defectuosas'] += prenda.cantidad

            if prenda.tipo not in contador_tipos:
                contador_tipos[prenda.tipo] = 0
                cantidad_tipos[prenda.tipo] = 0
                estadisticas['ingresos_por_tipo'][prenda.tipo] = 0.0

            contador_tipos[prenda.tipo] += 1
            cantidad_tipos[prenda.tipo] += prenda.cantidad
            if prenda.estado == 'FINALIZADA':
                estadisticas['ingresos_por_tipo'][prenda.tipo] += prenda.cantidad * prenda.costo_unidad

        for tipo in contador_tipos:
            estadisticas['promedio_por_tipo'][tipo] = cantidad_tipos[tipo] / contador_tipos[tipo]

        if estadisticas['ingresos_por_tipo']:
            estadisticas['tipo_mas_rentable'] = max(
                estadisticas['ingresos_por_tipo'].items(), 
                key=lambda x: x[1]
            )[0]
        else:
            estadisticas['tipo_mas_rentable'] = "Ninguno"

        return estadisticas

class Menu:
    def __init__(self, fabrica):
        self.fabrica = fabrica

    def mostrar_menu(self):
        while True:
            print("\n--- MENÚ FÁBRICA DE CONFECCIONES ---")
            print("1. Registrar nueva prenda")
            print("2. Modificar estado de prenda")
            print("3. Mover prenda en producción")
            print("4. Registrar venta")
            print("5. Mostrar producción actual")
            print("6. Mostrar ventas")
            print("7. Ver estadísticas")
            print("8. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.registrar_prenda()
            elif opcion == "2":
                self.modificar_estado()
            elif opcion == "3":
                self.mover_prenda()
            elif opcion == "4":
                self.registrar_venta()
            elif opcion == "5":
                self.fabrica.mostrar_produccion()
            elif opcion == "6":
                self.fabrica.mostrar_ventas()
            elif opcion == "7":
                self.mostrar_estadisticas()
            elif opcion == "8":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    def registrar_prenda(self):
        print("\n--- Registrar Nueva Prenda ---")
        tipo = input("Tipo de prenda: ")
        
        while True:
            fecha_str = input("Fecha de producción (Año-Mes-Día): ")
            try:
                fecha = datetime.date.fromisoformat(fecha_str)
                break
            except ValueError:
                print("Formato de fecha incorrecto. Use (Año-Mes-Día)")
        
        while True:
            cantidad = input("Cantidad producida: ")
            if cantidad.isdigit():
                cantidad = int(cantidad)
                break
            print("Debe ingresar un número entero.")
        
        while True:
            costo = input("Costo por unidad: ")
            try:
                costo = float(costo)
                break
            except ValueError:
                print("Debe ingresar un número válido.")

        self.fabrica.registrar_prenda(tipo, fecha, cantidad, costo)
        print("Prenda registrada exitosamente.")

    def modificar_estado(self):
        print("\n--- Modificar Estado de Prenda ---")
        self.fabrica.mostrar_produccion()
        
        try:
            indice = int(input("Índice de la prenda a modificar: "))
            print("Estados disponibles:", Prenda.ESTADOS)
            nuevo_estado = input("Nuevo estado: ").upper()
            
            self.fabrica.modificar_estado(indice, nuevo_estado)
            print("Estado modificado exitosamente.")
        except (IndexError, ValueError) as e:
            print(f"Error: {e}")

    def mover_prenda(self):
        print("\n--- Mover Prenda en Producción ---")
        self.fabrica.mostrar_produccion()
        
        try:
            indice = int(input("Índice de la prenda a mover: "))
            n_posiciones = int(input("Número de posiciones a mover: "))
            
            self.fabrica.mover_prenda(indice, n_posiciones)
            print("Prenda movida exitosamente.")
        except (IndexError, ValueError) as e:
            print(f"Error: {e}")

    def registrar_venta(self):
        print("\n--- Registrar Venta ---")
        self.fabrica.mostrar_produccion()
        print("Ingrese los índices de las prendas vendidas (separados por comas)")
        
        try:
            indices_str = input("Índices: ")
            indices = [int(i.strip()) for i in indices_str.split(",")]
            
            total = self.fabrica.registrar_venta(indices)
            print(f"Venta registrada. Total: ${total:.2f}")
        except ValueError:
            print("Error: Ingrese índices válidos (números separados por comas)")

    def mostrar_estadisticas(self):
        print("\n--- Estadísticas ---")
        stats = self.fabrica.calcular_estadisticas()
        print(f"Total ingresos por ventas: ${stats['total_ingresos']:.2f}")
        print(f"Total prendas producidas: {stats['total_producidas']}")
        print(f"Total prendas finalizadas: {stats['total_finalizadas']}")
        print(f"Total prendas defectuosas: {stats['total_defectuosas']}")
        print("\nPromedio de unidades por tipo:")
        for tipo, promedio in stats['promedio_por_tipo'].items():
            print(f"  {tipo}: {promedio:.1f}")
        print(f"\nTipo que generó más ingresos: {stats['tipo_mas_rentable']}")

if __name__ == "__main__":
    fabrica = Fabrica_confecciones()
    menu = Menu(fabrica)
    menu.mostrar_menu()