# OMC API

API para captura de leads.

## Stack Tecnológico

- **Python**: 3.14-trixie
- **Framework**: FastAPI
- **Base de Datos**: PostgreSQL 18
- **ORM**: SQLAlchemy (async)
- **Migraciones**: Alembic
- **Contenedores**: Docker + Docker Compose

## Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/` | Root - Mensaje de bienvenida |
| `POST` | `/api/v1/leads` | Crear nuevo lead |
| `GET` | `/api/v1/leads/{id}` | Obtener lead por ID |
| `PATCH` | `/api/v1/leads/{id}` | Actualizar lead existente |
| `DELETE` | `/api/v1/leads/{id}` | Eliminar lead |
| `GET` | `/api/v1/leads` | Listar leads con paginación |
| `GET` | `/api/v1/leads/stats` | Estadísticas de leads |
| `GET` | `/api/v1/health` | Health check |

### Parámetros de Query (GET /api/v1/leads)

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `page` | int | 1 | Número de página |
| `limit` | int | 10 | Items por página (max: 100) |
| `source` | str | - | Filtrar por fuente |
| `start_date` | date | - | Filtrar desde fecha (YYYY-MM-DD) |
| `end_date` | date | - | Filtrar hasta fecha (YYYY-MM-DD) |
| `order_dir` | str | desc | Orden (asc/desc) |

## Deploy

```bash
docker-compose up -d
```

La API estará disponible a través de Nginx en: `http://localhost:10000`

## Variables de Entorno

Consultar `.env` para la configuración:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=SUp3r-pass*DB
POSTGRES_DB=omc
POSTGRES_HOST=db
```

## Puertos

| Servicio | Puerto |
|----------|--------|
| API | 8010 |
| PostgreSQL | 5432 |
| Nginx | 10000 |

## Tareas Disponibles

Este proyecto usa [taskipy](https://taskipy.readthedocs.io/) para automatizar tareas comunes.

| Comando | Descripción |
|---------|-------------|
| `task test` | Ejecutar tests |
| `task lint` | Validar linter (ruff) |
| `task docker-up` | Iniciar servicios con Docker Compose |
| `task docker-down` | Detener servicios |
| `task migrate-create` | Crear nueva migración Alembic |
| `task migrate-upgrade` | Aplicar migraciones |
| `task migrate-downgrade` | Revertir última migración |

## Acerca del Proyecto

Este proyecto fue desarrollado aplicando **Spec Driven Development (SDD)** utilizando **OpenCode**, siguiendo las mejores prácticas de desarrollo moderno:

- **Arquitectura**: Clean Architecture con separación de responsabilidades
- **Stack**: Python 3.14, FastAPI, PostgreSQL 18, SQLAlchemy Async, Alembic
- **Calidad**: Tests unitarios e integración, Linting con Ruff, Type hints
- **Infraestructura**: Docker + Docker Compose con Nginx como reverse proxy

### Proyectos de Referencia

Esta implementación toma inspiración de experiencia previa en:

- [Order Processing System](https://github.com/raskolnikov1984/order-processing-system/tree/main/order-service) - Arquitectura de microservicios con Python
- [IAM Interview](https://github.com/raskolnikov1984/iam_interview) - Manejo de agentes, chatbots y LLM con modelos open source

### Siguientes Pasos

Para completar los requerimientos del desafío, se pueden implementar las siguientes funcionalidades tomando referencia del proyecto IAM Interview:

- Integración con LLM para generar resúmenes de leads
- Manejo de agentes para automatización
- Chatbot para interacción con clientes
