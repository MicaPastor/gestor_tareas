import os
import json
import logging
import questionary
from colorama import Fore, init
from tabulate import tabulate

init(autoreset=True)

# Configuración de logging
logging.basicConfig(
    filename="registro.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

def crear_tarea(id, titulo, descripcion, prioridad, dia):
    """
    Crea un diccionario que representa una nueva tarea pendiente.

    Args:
        id (int): Identificador único de la tarea.
        titulo (str): Título de la tarea.
        descripcion (str): Breve descripción de la tarea.
        prioridad (str): Prioridad asignada ("alta", "media" o "baja").
        dia (str): Día de la semana asignado a la tarea.

    Returns:
        dict: Diccionario con los datos de la tarea.
    """
    return {
        "id": id,
        "titulo": titulo,
        "descripcion": descripcion,
        "prioridad": prioridad,
        "dia": dia,
        "estado": "pendiente"
    }

def cargar_tareas():
    """
    Carga la lista de tareas desde el archivo 'tareas.json'.

    Si el archivo no existe, devuelve una lista vacía.

    Returns:
        list: Lista de tareas en formato diccionario.
    """
    if not os.path.exists("tareas.json"):
        return []
    with open("tareas.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

def guardar_tareas(lista_tareas):
    """
    Guarda la lista de tareas en el archivo 'tareas.json'.

    Sobrescribe el contenido anterior con la lista actualizada,
    utilizando formato JSON legible con indentación.

    Args:
        lista_tareas (list): Lista de tareas a guardar, en formato diccionario.

    Returns:
        None
    """
    with open("tareas.json", "w", encoding="utf-8") as archivo:
        json.dump(lista_tareas, archivo, indent=4, ensure_ascii=False)

def listar_tareas(lista_tareas):
    """
    Muestra la lista de tareas en formato tabla en la consola.

    Utiliza la librería 'tabulate' para dar formato a la tabla.
    Si no hay tareas cargadas, muestra un mensaje de advertencia.

    Args:
        lista_tareas (list): Lista de tareas en formato diccionario.

    Returns:
        None
    """
    if not lista_tareas:
        print(Fore.RED + "❌ No hay tareas cargadas.")
        return

    tabla = []
    for tarea in lista_tareas:
        tabla.append([
            tarea["id"],
            tarea["titulo"],
            tarea["prioridad"],
            tarea.get("dia", "-"),
            tarea["estado"]
        ])

    print(Fore.GREEN + "\n🗂️  Tareas registradas:\n")

    print(tabulate(
        tabla,
        headers=["ID", "Título", "Prioridad", "Día", "Estado"],
        tablefmt="fancy_grid",
        stralign="center",
        numalign="center"
    ))

def seleccionar_prioridad():
    """
    Muestra un menú interactivo para seleccionar la prioridad de una tarea.

    Returns:
        str: Prioridad seleccionada por el usuario ("alta", "media" o "baja").
    """
    return questionary.select(
        "Seleccioná la prioridad:",
        choices=["alta", "media", "baja"]
    ).ask()

def seleccionar_dia():
    """
    Muestra un menú interactivo para seleccionar un día de la semana.

    Returns:
        str: Día seleccionado por el usuario.
    """
    return questionary.select(
        "Seleccioná el día de la semana:",
        choices=["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    ).ask()

def confirmar_si_no(pregunta):
    """
    Muestra una pregunta cerrada con opciones "Sí" y "No" y devuelve el resultado.

    Convierte la respuesta a minúsculas y devuelve True si la opción elegida es afirmativa.

    Args:
        pregunta (str): Texto de la pregunta que se mostrará al usuario.

    Returns:
        bool: True si el usuario selecciona "Sí", False en caso contrario.
    """
    return questionary.select(
        pregunta,
        choices=["Sí", "No"]
    ).ask().lower() in ["sí", "si"]

def pedir_id(lista_tareas, mensaje="Seleccioná el ID de la tarea"):
    """
    Solicita al usuario un ID de tarea existente y valida que sea correcto.

    Muestra un mensaje personalizado, espera la entrada del usuario,
    verifica que sea un número válido y que el ID exista en la lista.

    Args:
        lista_tareas (list): Lista de tareas en formato diccionario.
        mensaje (str, opcional): Mensaje que se muestra al usuario. Por defecto: "Seleccioná el ID de la tarea".

    Returns:
        dict: Tarea correspondiente al ID ingresado.
    """
    while True:
        try:
            id_str = questionary.text(f"{mensaje} (de la tabla mostrada):").ask()
            id_int = int(id_str)
            tarea = next((t for t in lista_tareas if t["id"] == id_int), None)
            if tarea:
                return tarea
            print(Fore.RED + "❌ No se encontró ninguna tarea con ese ID.")
        except ValueError:
            print(Fore.RED + "❌ Ingresá un número válido.")

def agregar_tarea(lista_tareas):
    """
    Solicita los datos al usuario y agrega una nueva tarea a la lista.

    Pide título, descripción, prioridad y día. Genera un ID único,
    crea la tarea, la agrega a la lista, la guarda en el archivo
    y registra la acción en el archivo de logs.

    Args:
        lista_tareas (list): Lista actual de tareas.

    Returns:
        None
    """
    titulo = questionary.text("📌 Ingresá el título de la tarea:").ask()
    descripcion = questionary.text("📝 Ingresá la descripción de la tarea:").ask()
    prioridad = seleccionar_prioridad()
    dia = seleccionar_dia()

    nuevo_id = max((t["id"] for t in lista_tareas), default=0) + 1
    nueva_tarea = crear_tarea(nuevo_id, titulo, descripcion, prioridad, dia)
    lista_tareas.append(nueva_tarea)
    guardar_tareas(lista_tareas)
    print(Fore.GREEN + "✅ Tarea agregada con éxito.")
    logging.info(f"Tarea agregada: ID {nuevo_id} - {titulo}")

def completar_tarea(lista_tareas):
    """
    Marca una tarea como completada a partir del ID seleccionado por el usuario.

    Muestra la lista de tareas, solicita el ID, y si la tarea no está ya completada,
    actualiza su estado, la guarda en el archivo y registra la acción en el log.

    Args:
        lista_tareas (list): Lista actual de tareas.

    Returns:
        None
    """
    if not lista_tareas:
        print(Fore.RED + "❌ No hay tareas disponibles.")
        return
    listar_tareas(lista_tareas)
    tarea = pedir_id(lista_tareas, "Seleccioná el ID de la tarea que querés completar")
    if tarea["estado"] == "completada":
        print(Fore.YELLOW + "⚠️  La tarea ya estaba completada.")
    else:
        tarea["estado"] = "completada"
        guardar_tareas(lista_tareas)
        print(Fore.GREEN + "✅ Tarea marcada como completada.")
        logging.info(f"Tarea completada: ID {tarea['id']} - {tarea['titulo']}")

def modificar_tarea(lista_tareas):
    """
    Permite al usuario modificar los campos de una tarea existente.

    Muestra la lista de tareas, solicita el ID a modificar y permite
    cambiar el título, descripción, prioridad o día. Pregunta si desea
    seguir modificando más campos. Guarda los cambios y los registra en el log.

    Args:
        lista_tareas (list): Lista actual de tareas.

    Returns:
        None
    """
    if not lista_tareas:
        print(Fore.RED + "❌ No hay tareas para modificar.")
        return
    listar_tareas(lista_tareas)
    tarea = pedir_id(lista_tareas, "Seleccioná el ID de la tarea que querés modificar")

    while True:
        opcion = questionary.select(
            "¿Qué campo querés modificar?",
            choices=["Título", "Descripción", "Prioridad", "Día", "Cancelar"]
        ).ask().lower()

        if opcion == "título":
            tarea["titulo"] = questionary.text("Nuevo título:").ask()
        elif opcion == "descripción":
            tarea["descripcion"] = questionary.text("Nueva descripción:").ask()
        elif opcion == "prioridad":
            tarea["prioridad"] = seleccionar_prioridad()
        elif opcion == "día":
            tarea["dia"] = seleccionar_dia()
        elif opcion == "cancelar":
            print(Fore.BLUE + "⏪ Modificación cancelada.")
            return

        if not confirmar_si_no("¿Deseás modificar otro campo?"):
            break

    guardar_tareas(lista_tareas)
    print(Fore.GREEN + "✅ Tarea modificada con éxito.")
    logging.info(f"Tarea modificada: ID {tarea['id']} - {tarea['titulo']}")

def eliminar_tarea(lista_tareas):
    """
    Elimina una tarea seleccionada por el usuario de la lista.

    Muestra la lista de tareas, solicita el ID a eliminar y pide confirmación.
    Si el usuario confirma, elimina la tarea, guarda los cambios y registra la acción en el log.

    Args:
        lista_tareas (list): Lista actual de tareas.

    Returns:
        None
    """
    if not lista_tareas:
        print(Fore.RED + "❌ No hay tareas para eliminar.")
        return
    listar_tareas(lista_tareas)
    tarea = pedir_id(lista_tareas, "Seleccioná el ID de la tarea que querés eliminar")

    if confirmar_si_no(f"¿Estás segura de eliminar la tarea '{tarea['titulo']}'?"):
        lista_tareas.remove(tarea)
        guardar_tareas(lista_tareas)
        print(Fore.WHITE + "🗑️  Tarea eliminada con éxito.")
        logging.info(f"Tarea eliminada: ID {tarea['id']} - {tarea['titulo']}")
    else:
        print(Fore.GREEN + "❎ Eliminación cancelada.")

def filtrar_tareas(lista_tareas):
    """
    Filtra la lista de tareas según prioridad, estado o día.

    Muestra un menú de opciones al usuario para elegir el criterio de filtrado.
    Luego muestra las tareas que coinciden con ese criterio o un mensaje si no hay resultados.

    Args:
        lista_tareas (list): Lista actual de tareas.

    Returns:
        None
    """
    if not lista_tareas:
        print("❌ No hay tareas cargadas.")
        return

    opcion = questionary.select(
        "¿Cómo querés filtrar las tareas?",
        choices=["Por prioridad", "Por estado", "Por día", "Cancelar"]
    ).ask()

    if opcion == "Por prioridad":
        criterio = seleccionar_prioridad()
        filtradas = [t for t in lista_tareas if t["prioridad"] == criterio]
    elif opcion == "Por estado":
        criterio = questionary.select("Seleccioná el estado:", choices=["pendiente", "completada"]).ask()
        filtradas = [t for t in lista_tareas if t["estado"] == criterio]
    elif opcion == "Por día":
        criterio = seleccionar_dia()
        filtradas = [t for t in lista_tareas if t.get("dia") == criterio]
    elif opcion == "Cancelar":
        print("⏪ Filtro cancelado.")
        return
    else:
        print("❌ Opción inválida.")
        return

    if not filtradas:
        print(f"⚠️ No se encontraron tareas con ese criterio: '{criterio}'.")
    else:
        print(f"\n📋 Tareas filtradas por '{criterio}':")
        listar_tareas(filtradas)

