# 📝 Gestor de Tareas - Parcial 2 - Programación 1

Este proyecto consiste en un **Gestor de Tareas en consola** desarrollado en Python como parte del Parcial 2 de la materia **Programación 1** de la carrera **Ciencia de Datos**.

Permite **agregar, listar, modificar, completar, eliminar y filtrar tareas**, todo desde un menú interactivo gracias al módulo `questionary`.

---

## ✅ Funcionalidades

- 📄 Listar tareas en formato de tabla.
- ➕ Agregar nueva tarea (con título, descripción, prioridad y día).
- ✏️  Modificar cualquier campo de una tarea.
- ✅ Marcar una tarea como completada.
- 🗑️  Eliminar una tarea existente.
- 🔍 Filtrar tareas por prioridad, estado o día.
- 📂 Guardado automático en archivo `tareas.json`.
- 📝 Registro de acciones en `registro.log`.

---

## 📦 Requisitos (requirements.txt)

Asegurate de instalar estas librerías antes de ejecutar el programa:

```
colorama==0.4.6
questionary==2.1.0
tabulate==0.9.0
```

Instalación rápida:

```bash
pip install -r requirements.txt
```

---

## ⚠️ Nota sobre las tablas

El programa utiliza la librería tabulate para mostrar las tareas en forma de tabla.
Se utiliza el formato fancy_grid, ya que:

Presenta un diseño visual más moderno y estético.

Usa caracteres Unicode que embellecen la presentación de los datos.

Se ve especialmente bien en pantallas amplias y configuraciones que soportan buena codificación UTF-8.

🔧 **Si ves que las tablas aparecen "desarmadas" o con líneas desalineadas**, probá:

- Agrandar la ventana de la terminal.
- Usar una fuente monoespaciada (como Consolas o Courier).
- Usar una terminal moderna con soporte completo para caracteres Unicode. (como Terminal de Windows, VS Code, etc).

---

## 📁 Archivos del proyecto

- `main.py`: Menú principal del programa.
- `tareas.py`: Lógica y funciones del sistema.
- `tareas.json`: Archivo donde se guardan las tareas.
- `registro.log`: Registro de acciones (agregar, modificar, eliminar).
- `requirements.txt`: Lista de librerías necesarias.
- `README.md`: Documentación del proyecto.

---

## 👩‍💻 Desarrollado por

Micaela Pastor  
Trabajo práctico - Parcial 2 - Programación 1  
Carrera: Tecnicatura en Ciencia de Datos
