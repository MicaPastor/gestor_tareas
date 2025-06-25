import questionary
from tareas import (
    cargar_tareas,
    listar_tareas,
    agregar_tarea,
    completar_tarea,
    modificar_tarea,
    filtrar_tareas,
    eliminar_tarea
)

def menu():
    """
    Muestra el menú principal del gestor de tareas en consola.

    Presenta al usuario una lista de opciones interactivas para
    visualizar, agregar, modificar, completar, filtrar o eliminar tareas.
    Ejecuta la función correspondiente según la opción seleccionada.

    Returns:
        None
    """
    while True:
        tareas = cargar_tareas()

        opcion = questionary.select(
            "📋 ¿Qué acción querés realizar?",
            choices=[
                "📄 Listar tareas",
                "➕ Agregar nueva tarea",
                "✏️  Modificar tarea",
                "✅ Marcar tarea como completada",
                "🗑️  Eliminar tarea",
                "🔍 Filtrar tareas",
                "🚪 Salir"
            ]
        ).ask()

        if opcion == "📄 Listar tareas":
            listar_tareas(tareas)
        elif opcion == "➕ Agregar nueva tarea":
            agregar_tarea(tareas)
        elif opcion == "✏️  Modificar tarea":
            modificar_tarea(tareas)
        elif opcion == "✅ Marcar tarea como completada":
            completar_tarea(tareas)
        elif opcion == "🗑️  Eliminar tarea":
            eliminar_tarea(tareas)
        elif opcion == "🔍 Filtrar tareas":
            filtrar_tareas(tareas)
        elif opcion == "🚪 Salir":
            print("👋 Saliendo del programa... ¡Hasta la próxima!")
            break

if __name__ == "__main__":
    menu()

