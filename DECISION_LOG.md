# Decisiones

Intenté seguir una arquitectura limpia, separando el proyecto en `domain`,
`application`, `infrastructure` y `api`. La lógica de negocio vive en los casos de
uso, que no dependen de FastAPI ni de SQLAlchemy, así se pueden testear sin levantar
nada.

Para no pelearme con migraciones, las tablas se crean solas al arrancar la app. No es
lo más prolijo para producción, pero prioricé que se pueda levantar fácil.

## Pendientes

Siendo honesto, por tema de tiempos no alcancé a hacer la autenticación con JWT ni lo
de asignar un usuario responsable por tarea.
