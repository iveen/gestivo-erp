# Gestivo ERP

A modern, multi-tenant ERP system built with Django 5.2 + Vue 3.

## Tech Stack

**Backend:** Django 5.2, Django REST Framework, PostgreSQL 17, Redis, Celery  
**Frontend:** Vue 3, Vite, Tailwind CSS, Pinia, Chart.js  
**Infrastructure:** Docker, Nginx, GitHub Actions CI/CD

## Modules

- **Finance** — Chart of accounts, journal entries, AP/AR, aging reports, balance sheet, P&L
- **Inventory** — Products, warehouses, stock moves, low stock alerts
- **Sales** — Quotations, sales orders, customers
- **Purchases** — Purchase orders, approval workflow, vendors
- **Manufacturing** — Bill of materials, work centers, manufacturing orders
- **CRM** — Lead pipeline, kanban board

## Quick Start (Development)
```bash
# Clone and setup
git clone <repo>
cd gestivo
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run migrations and create superuser
python manage.py migrate
python manage.py createsuperuser

# Start backend
python manage.py runserver

# Start frontend (separate terminal)
cd frontend
npm install
npm run dev
```

## Production Deployment
```bash
# Build Docker image
docker build -t gestivo:latest .

# Configure environment
cp .env.example .env.prod
# Edit .env.prod with production values

# Start all services
SECRET_KEY=your-secret-key DB_PASSWORD=your-db-pass docker compose -f docker-compose.prod.yml up -d
```

## Running Tests
```bash
pytest apps/ --cov=apps --cov-report=term-missing
```

**Coverage targets:**
- Overall: ≥ 85% (current: 92%)
- Finance module: ≥ 95% (current: 95%)

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/api/docs/`
- Health check: `http://localhost:8000/api/health/`

## Architecture

- **Multi-tenancy:** Row-level via `tenant` FK on every model
- **Auth:** JWT (1hr access, 7day refresh with rotation)
- **Middleware:** `TenantMiddleware` reads `X-Tenant-Slug` header, `CompanyMiddleware` reads `X-Company-ID` header
- **Pagination:** 50 records per page

## Project Structure
```
gestivo/
├── apps/
│   ├── core/          # BaseModel
│   ├── tenants/       # Tenant model + middleware
│   ├── accounts/      # Users, companies, RBAC
│   ├── finance/       # GL, AP, AR, reports
│   ├── inventory/     # Products, stock
│   ├── sales/         # Quotations, orders
│   ├── purchases/     # PO, approval workflow
│   ├── manufacturing/ # BOM, work centers, MO
│   └── crm/           # Lead pipeline
├── frontend/          # Vue 3 + Vite
├── nginx/             # Nginx config
├── Dockerfile
├── docker-compose.prod.yml
└── .github/workflows/ # CI/CD
```
