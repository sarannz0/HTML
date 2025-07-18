import os

def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_panel(equipos):
    """Muestra el panel de estadísticas de los equipos."""
    print("=" * 60)
    print("PANEL DE ESTADÍSTICAS DEL TORNEO")
    print("=" * 60)
    print(f"{'Equipo':<15} | {'PJ':>3} | {'PG':>3} | {'PP':>3} | {'PE':>3} | {'GF':>3} | {'GC':>3}")
    print("-" * 60)
    for nombre, datos in equipos.items():
        print(f"{nombre:<15} | {datos['pj']:>3} | {datos['pg']:>3} | {datos['pp']:>3} | {datos['pe']:>3} | {datos['gf']:>3} | {datos['gc']:>3}")
    print("=" * 60)

def mostrar_menu():
    """Muestra el menú de opciones."""
    print("\nMENÚ DE OPCIONES:")
    print("1. Registrar equipo")
    print("2. Programar fecha")
    print("3. Registrar marcador de un partido")
    print("4. Ver equipo con más goles a favor")
    print("5. Ver equipo con más goles en contra")
    print("6. Registrar plantel de un equipo")
    print("7. Salir")

def registrar_equipo(equipos):
    """Registra un nuevo equipo."""
    nombre = input("Introduce el nombre del nuevo equipo: ").strip()
    if nombre in equipos:
        print("Error: El equipo ya está registrado.")
    elif nombre:
        equipos[nombre] = {"pj": 0, "pg": 0, "pp": 0, "pe": 0, "gf": 0, "gc": 0, "plantel": []}
        print(f"¡Equipo '{nombre}' registrado con éxito!")
    else:
        print("Error: El nombre del equipo no puede estar vacío.")

def programar_fecha(equipos, calendario):
    """Programa un nuevo partido."""
    if len(equipos) < 2:
        print("Necesitas al menos dos equipos registrados para programar una fecha.")
        return

    print("Equipos disponibles:", ", ".join(equipos.keys()))
    local = input("Introduce el nombre del equipo local: ").strip()
    visitante = input("Introduce el nombre del equipo visitante: ").strip()

    if local not in equipos or visitante not in equipos:
        print("Error: Uno o ambos equipos no están registrados.")
    elif local == visitante:
        print("Error: Un equipo no puede jugar contra sí mismo.")
    else:
        partido = {"local": local, "visitante": visitante, "marcador_local": None, "marcador_visitante": None}
        calendario.append(partido)
        print(f"Partido '{local} vs {visitante}' programado.")

def registrar_marcador(equipos, calendario):
    """Registra el marcador de un partido y actualiza las estadísticas."""
    partidos_pendientes = [p for p in calendario if p["marcador_local"] is None]
    if not partidos_pendientes:
        print("No hay partidos pendientes de registrar marcador.")
        return

    print("\nPartidos pendientes:")
    for i, partido in enumerate(partidos_pendientes):
        print(f"{i + 1}. {partido['local']} vs {partido['visitante']}")

    try:
        opcion = int(input("Selecciona el número del partido para registrar el marcador: ")) - 1
        if 0 <= opcion < len(partidos_pendientes):
            partido_seleccionado = partidos_pendientes[opcion]
            marcador_local = int(input(f"Goles de {partido_seleccionado['local']}: "))
            marcador_visitante = int(input(f"Goles de {partido_seleccionado['visitante']}: "))

            # Actualizar marcador en el calendario
            partido_seleccionado["marcador_local"] = marcador_local
            partido_seleccionado["marcador_visitante"] = marcador_visitante

            # Actualizar estadísticas
            local = partido_seleccionado["local"]
            visitante = partido_seleccionado["visitante"]

            equipos[local]["pj"] += 1
            equipos[visitante]["pj"] += 1
            equipos[local]["gf"] += marcador_local
            equipos[visitante]["gf"] += marcador_visitante
            equipos[local]["gc"] += marcador_visitante
            equipos[visitante]["gc"] += marcador_local

            if marcador_local > marcador_visitante:
                equipos[local]["pg"] += 1
                equipos[visitante]["pp"] += 1
            elif marcador_visitante > marcador_local:
                equipos[visitante]["pg"] += 1
                equipos[local]["pp"] += 1
            else:
                equipos[local]["pe"] += 1
                equipos[visitante]["pe"] += 1
            
            print("Marcador registrado y estadísticas actualizadas.")
        else:
            print("Opción no válida.")
    except ValueError:
        print("Error: Debes introducir un número.")

def equipo_mas_goles_favor(equipos):
    """Encuentra y muestra el equipo con más goles a favor."""
    if not equipos:
        print("No hay equipos registrados.")
        return
    
    equipo_max_gf = max(equipos, key=lambda e: equipos[e]['gf'])
    print(f"El equipo con más goles a favor es: {equipo_max_gf} ({equipos[equipo_max_gf]['gf']} goles).")

def equipo_mas_goles_contra(equipos):
    """Encuentra y muestra el equipo con más goles en contra."""
    if not equipos:
        print("No hay equipos registrados.")
        return
    
    equipo_max_gc = max(equipos, key=lambda e: equipos[e]['gc'])
    print(f"El equipo con más goles en contra es: {equipo_max_gc} ({equipos[equipo_max_gc]['gc']} goles).")

def registrar_plantel(equipos):
    """Registra los jugadores en la plantilla de un equipo."""
    if not equipos:
        print("No hay equipos registrados.")
        return

    print("Equipos disponibles:", ", ".join(equipos.keys()))
    nombre_equipo = input("Introduce el nombre del equipo para registrar su plantel: ").strip()

    if nombre_equipo in equipos:
        while True:
            nombre_jugador = input("Introduce el nombre del jugador (o 'fin' para terminar): ").strip()
            if nombre_jugador.lower() == 'fin':
                break
            if nombre_jugador:
                equipos[nombre_equipo]["plantel"].append(nombre_jugador)
                print(f"Jugador '{nombre_jugador}' añadido a '{nombre_equipo}'.")
            else:
                print("El nombre del jugador no puede estar vacío.")
    else:
        print("Error: El equipo no está registrado.")


def main():
    """Función principal del programa."""
    equipos = {}
    calendario = []

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input("Elige una opción: ")

        if opcion == '1':
            registrar_equipo(equipos)
        elif opcion == '2':
            programar_fecha(equipos, calendario)
        elif opcion == '3':
            registrar_marcador(equipos, calendario)
        elif opcion == '4':
            equipo_mas_goles_favor(equipos)
        elif opcion == '5':
            equipo_mas_goles_contra(equipos)
        elif opcion == '6':
            registrar_plantel(equipos)
        elif opcion == '7':
            print("Saliendo del programa. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()