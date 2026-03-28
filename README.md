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
