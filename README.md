# Task Manager API

API para manejar listas de tareas y darles seguimiento. Cada tarea tiene un
**status** (`todo`, `in_progress`, `completed`) y una **prioridad** (`low`, `medium`,
`high`).

Stack: FastAPI + PostgreSQL + SQLAlchemy. Documentación interactiva en
`http://localhost:8000/docs`.

## Levantar la app

Necesitás Docker. Desde la raíz del proyecto:

```bash
docker compose up --build
```

La API queda en `http://localhost:8000`.

> Si el contenedor `api` arranca antes que la base y falla, corré el comando de
> nuevo. La base tiene que estar lista primero.

## Tutorial de uso

### 1. Crear una lista de tareas

```bash
curl -X POST http://localhost:8000/task-lists/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Compras"}'
```

Respuesta:

```json
{
  "id": "3f9a1c2e-7b41-4d8e-9a55-0c1d2e3f4a5b",
  "name": "Compras",
  "created_at": "2026-10-03T02:50:28",
  "updated_at": "2026-10-03T02:50:28"
}
```

Guardá el `id`, es el `LIST_ID` que se usa en los próximos pasos.

### 2. Ver esa lista

```bash
curl http://localhost:8000/task-lists/<LIST_ID>
```

### 3. Renombrar la lista

```bash
curl -X PUT http://localhost:8000/task-lists/<LIST_ID> \
  -H "Content-Type: application/json" \
  -d '{"name": "Compras de la semana"}'
```

### 4. Crear una tarea dentro de la lista

El `list_id` va como parámetro en la URL. El status inicial siempre es `todo`.

```bash
curl -X POST "http://localhost:8000/tasks/?list_id=<LIST_ID>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Comprar leche", "description": "2 litros", "priority": "high"}'
```

Respuesta:

```json
{
  "id": "b7c1e5a9-2d34-4f60-8e11-9a0b1c2d3e4f",
  "list_id": "3f9a1c2e-7b41-4d8e-9a55-0c1d2e3f4a5b",
  "title": "Comprar leche",
  "description": "2 litros",
  "status": "todo",
  "priority": "high",
  "created_at": "2026-10-03T02:51:00",
  "updated_at": "2026-10-03T02:51:00"
}
```

Guardá el `id` de la tarea, es el `TASK_ID`.

### 5. Ver esa tarea

```bash
curl http://localhost:8000/tasks/<TASK_ID>
```

### 6. Actualizar la tarea completa

`PUT` reemplaza todos los campos: `title`, `description`, `status` y `priority`.

```bash
curl -X PUT http://localhost:8000/tasks/<TASK_ID> \
  -H "Content-Type: application/json" \
  -d '{"title": "Comprar leche", "description": "1 litro", "status": "in_progress", "priority": "medium"}'
```

### 7. Cambiar solo el estado de la tarea

Con `PATCH` cambiás **solo** el status, sin tocar el resto.

```bash
curl -X PATCH http://localhost:8000/tasks/<TASK_ID> \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

Los valores posibles son `todo`, `in_progress` y `completed`.

### 8. Listar las tareas de la lista

Devuelve las tareas y el porcentaje de completitud.

```bash
curl http://localhost:8000/tasks/list/<LIST_ID>
```

Respuesta:

```json
{
  "tasks": [
    {
      "id": "b7c1e5a9-2d34-4f60-8e11-9a0b1c2d3e4f",
      "title": "Comprar leche",
      "status": "completed",
      "priority": "high"
    }
  ],
  "completed_percentage": 100.0
}
```

También podés filtrar por status o prioridad:

```bash
curl "http://localhost:8000/tasks/list/<LIST_ID>?status=todo"
curl "http://localhost:8000/tasks/list/<LIST_ID>?priority=high"
curl "http://localhost:8000/tasks/list/<LIST_ID>?status=todo&priority=high"
```

El `completed_percentage` se calcula sobre las tareas que devuelve el filtro.

### 9. Eliminar una tarea

```bash
curl -X DELETE http://localhost:8000/tasks/<TASK_ID>
```

### 10. Eliminar la lista

```bash
curl -X DELETE http://localhost:8000/task-lists/<LIST_ID>
```

Al borrar una lista también se borran sus tareas.

## Endpoints

| Método | Endpoint                  | Qué hace                              |
| ------ | ------------------------- | ------------------------------------- |
| POST   | `/task-lists/`            | Crear lista                           |
| GET    | `/task-lists/{id}`        | Ver lista                             |
| PUT    | `/task-lists/{id}`        | Renombrar lista                       |
| DELETE | `/task-lists/{id}`        | Borrar lista y sus tareas             |
| POST   | `/tasks/?list_id={id}`    | Crear tarea en una lista              |
| GET    | `/tasks/{id}`             | Ver tarea                             |
| PUT    | `/tasks/{id}`             | Actualizar tarea completa             |
| PATCH  | `/tasks/{id}`             | Cambiar solo el status                |
| DELETE | `/tasks/{id}`             | Borrar tarea                          |
| GET    | `/tasks/list/{list_id}`   | Listar tareas + porcentaje completado |

Filtros opcionales en el listado: `?status=` y `?priority=`.

## Tests y linters

Los tests usan SQLite, no necesitan Docker ni la base levantada. Primero instalá
las dependencias (incluye las de desarrollo):

```bash
pip install -r requirements.txt
```

Correr los tests:

```bash
pytest
```

Formato y lint (deberían pasar sin cambios):

```bash
black .
flake8 .
```

## Estructura

```
api/             rutas y schemas
application/     casos de uso
domain/          entidades, enums y repositorios
infrastructure/  base de datos y repositorios
tests/           tests de API y de dominio
```

Las decisiones técnicas están documentadas en [DECISION_LOG.md](DECISION_LOG.md).
