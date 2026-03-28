# Backlog de Desarrollo - API de Leads

## Fase 1: Infraestructura y Persistencia
- [x] Configuración del Entorno
- [x] Modelo de Datos
- [ ] Timestamps: Agregar campo updated_at automático
- [x] Gestión de Base de Datos (PostgreSQL + Alembic)
- [ ] Seed Data: Script para insertar 10 leads de prueba

## Fase 2: API REST & Validaciones
- [x] POST /leads
  - [ ] Validar email único
  - [ ] Validar nombre (mínimo 2 caracteres)
  - [ ] Validar fuente permitida
- [x] GET /leads (paginación, filtros, ordenamiento)
- [x] GET /leads/:id
- [x] PATCH /leads/:id
- [ ] DELETE /leads/:id (implementar soft delete)
- [x] GET /leads/stats

## Fase 3: Inteligencia Artificial
- [ ] Filtrado de Contexto
- [ ] Integración LLM (OpenAI/Anthropic o Mock)
- [ ] POST /leads/ai/summary

## Fase 4: Documentación y Calidad
- [x] README.md
- [x] .env.example
- [ ] Manejo de Errores estandarizado
- [ ] Swagger

## Fase 5: Bonus
- [x] Dockerización
- [x] Tests
- [ ] Autenticación JWT/API Key