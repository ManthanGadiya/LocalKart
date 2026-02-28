# LocalKart

LocalKart is a starter project for product-material discovery and nearby shop lookup.

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python, FastAPI
- Database: SQLite + SQLAlchemy

## Project Layout

- `app/main.py` - FastAPI routes and app configuration
- `app/database.py` - SQLAlchemy engine/session/base
- `app/models.py` - SQLAlchemy models
- `app/schemas.py` - Pydantic response schemas
- `app/seed.py` - sample seed data
- `database/schema.sql` - SQLite schema (DDL)
- `frontend/index.html` - Login page
- `frontend/home.html` - Dashboard/Home page
- `frontend/select.html` - Select utensil page
- `frontend/materials.html` - Dynamic material comparison page
- `frontend/nearby.html` - Nearby shops page
- `frontend/about.html` - About page
- `frontend/static/styles.css` - styles
- `frontend/static/site.js` - top bar interactions
- `frontend/static/login.js` - login page behavior
- `frontend/static/select.js` - utensil selection and flow control
- `frontend/static/materials.js` - dynamic material rendering
- `frontend/static/nearby.js` - nearby shops rendering
- `requirements.txt` - dependencies
- `test_main.http` - endpoint test requests

## Frontend Pages

Final recommended flow:
- `index.html` - Center login card (LocalKart + subtitle + username/password + green login button + sign up action)
- `home.html` - Sticky navbar + hero + orange CTA + 3 feature cards
- `select.html` - Utensil card grid (2 per row) with hover lift and click-to-compare flow
- `materials.html` - Card-based material comparison (2 per row), with pros/cons/health/best-for
- `nearby.html` - Clean nearby shops table (`Shop Name | Area | Contact | Rating`) with green borders and row hover
- `about.html` - Project objective/problem statement
- Nearby UX is user-friendly:
  - Use My Current Location button
  - preset locations for major cities
  - no need to manually type latitude/longitude
  - clicking area opens Google Maps

Material comparison behavior:
- After selecting a utensil, `materials.html` loads material variants from backend.
- Comparison is shown as cards (2 per row) with pros/cons/health/best-for.
- Each product has 4 material options.

Top bar behavior:
- Present on all pages after login.
- Right side links: `Home | Compare | Nearby | About | Logout`.

Footer behavior:
- Consistent footer on all main pages:
`© 2026 LocalKart - Smart Utensil Guide`

## Database Schema First

Schema file: `database/schema.sql`

Main tables:
- `users`
- `categories`
- `products`
- `materials`
- `product_varieties`
- `variety_features`
- `shops`
- `shop_inventory`

## API Endpoints

- `GET /api/health`
- `GET /api/categories`
- `GET /api/products?category_id=<id>`
- `GET /api/products/{product_id}/varieties`
- `GET /api/shops/nearby?lat=<x>&lng=<y>&radius_km=<r>&product_id=<id>`

## Run

1. Install dependencies
```bash
pip install -r requirements.txt
```

2. Start server
```bash
uvicorn app.main:app --reload
```

3. Open UI
- `http://127.0.0.1:8000/`

4. Open API docs
- `http://127.0.0.1:8000/docs`

## Frontend On 63342 + Backend On 8000

If frontend is opened from JetBrains built-in server:
- `http://localhost:63342/LocalKart/frontend/index.html`

Backend runs on:
- `http://127.0.0.1:8000`

Integration notes:
- CORS is enabled in FastAPI for `localhost:63342` and `127.0.0.1:63342`.
- Frontend JS auto-targets `http://127.0.0.1:8000` when running on port `63342`.

## Seed Data

On startup, tables are created and seed data is enforced for development.
Current seed target:
- `users`: 5
- `categories`: 12
- `products`: 60
- `materials`: 12
- `product_varieties`: 240
- `variety_features`: 720
- `shops`: 130
- `shop_inventory`: 520

## Changelog

- 2026-02-27: Rebuilt project from scratch with FastAPI + SQLite/SQLAlchemy + HTML/CSS/JS.
- 2026-02-27: Removed root `main.py`; app now runs directly with `uvicorn app.main:app --reload`.
- 2026-02-27: Updated seeding to keep up to 10 records in every current table.
- 2026-02-27: Redesigned frontend to a vibrant 6-page site with shared top bar and hidden-at-start signup/login menu.
- 2026-02-27: Added explicit CORS + frontend API base handling for separate frontend (63342) and backend (8000) setup.
- 2026-02-27: Refactored to final 6-page flow (`index`, `home`, `select`, `materials`, `nearby`, `about`) and expanded database seed significantly.
- 2026-02-27: Added 4 materials per product and converted selected utensil comparison to a pros/cons table format.
- 2026-02-27: Added users seed (5 users) and first page now asks for both Sign Up and Login.
- 2026-02-27: Applied full UI redesign with sticky navbar, login-card style, utensil grid cards, material comparison cards, styled nearby table, and consistent footer.


- 2026-02-27: Added many more shop locations (8 cities), clickable map links from nearby results, and geolocation/preset-based nearby search UX.



## LocalKart Theme

Applied premium project theme:
- Dark default (`#0f0f0f`) with neon green (`#00ff9d`) and electric orange (`#ff6b00`) accents
- Glass UI cards with blur/glow effects
- Cinematic hero section with animated gradient
- Sticky navbar with theme toggle (light mode optional)
- Smooth hover effects, page fade-in, loading pulse, scroll-reveal animations
- Subtle background particle animation
- Floating `Compare Now` action button

Page upgrades:
- Home: cinematic hero + neon CTA + glass feature cards
- Select: search + filter chips + 3-column utensil grid with hover/zoom/score indicators
- Comparison: split power-panel layout with neon vertical tabs + animated metric bars
- Nearby: dark map placeholder + store cards with call button and map open action
- 2026-02-27: Upgraded to LocalKart premium dark-neon glass UI with animations, theme toggle, and startup-style interface.


- 2026-02-27: Expanded Pune and Mumbai coverage significantly (Pune 40 areas, Mumbai 30 areas) and added many Pune-area presets in nearby selection.

