# DjangoProject4

Django 5 contact workflow project with server-rendered templates, form submission handling, and persistent storage through Django ORM.

## What This Project Does
- Renders a contact form UI.
- Accepts user submission (`POST`) and writes records to the database.
- Uses Django `messages` framework for submission feedback.
- Exposes Django Admin for data inspection and management.
- Adds an advanced submissions dashboard with search, quick filters, message expansion, and dense view mode.
- Supports server-side sorting and pagination for submissions.
- Supports CSV export of all submissions.

## Architecture Overview
```text
Browser
  -> Django URL Router
    -> updateData.views.customerData
      -> updateData.models.UpdateData (ORM)
        -> Database (SQLite by default, MySQL optional)
    -> updateData.views.submissions
      -> Query/filter/sort/paginate UpdateData records
  -> Template Rendering (templates/updateAPI/*.html)
  -> Static Assets (static/)
```

## Stack
- Python 3.12
- Django 5.1.x
- PyMySQL (only required when MySQL mode is enabled)
- SQLite (default) / MySQL (optional)

## Repository Layout
```text
.
├── apiLearning/
│   ├── settings.py          # Env-aware DB config and global Django settings
│   ├── urls.py              # Root routing and app include
│   ├── asgi.py
│   └── wsgi.py
├── updateData/
│   ├── models.py            # UpdateData model
│   ├── views.py             # Form handling + success rendering
│   ├── urls.py              # App routes
│   ├── admin.py
│   └── migrations/
├── templates/
│   └── updateAPI/
│       ├── base.html
│       ├── index.html
│       ├── save_data.html
│       └── submissions.html
├── static/
├── manage.py
├── requirement.txt
└── db.sqlite3               # Created after first migration in SQLite mode
```

## Setup (Development)
### 1. Virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirement.txt
```

### 3. Database migration
```bash
python manage.py migrate
```

### 4. Run server
```bash
python manage.py runserver 127.0.0.1:8001
```

Open `http://127.0.0.1:8001/`.

## Configuration Strategy
Database mode is controlled in `apiLearning/settings.py`:
- SQLite mode (default): no env vars needed.
- MySQL mode: set `USE_MYSQL=1` and provide connection values.

### Environment variables
| Variable | Required | Default | Description |
|---|---|---|---|
| `USE_MYSQL` | No | `0` | Set to `1` to enable MySQL backend |
| `MYSQL_DATABASE` | MySQL only | `userInfo` | MySQL database name |
| `MYSQL_USER` | MySQL only | `root` | MySQL user |
| `MYSQL_PASSWORD` | MySQL only | empty | MySQL password |
| `MYSQL_HOST` | MySQL only | `127.0.0.1` | MySQL host |
| `MYSQL_PORT` | MySQL only | `3306` | MySQL port |

### Example: MySQL mode
```bash
export USE_MYSQL=1
export MYSQL_DATABASE=userInfo
export MYSQL_USER=root
export MYSQL_PASSWORD='your_password'
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
python manage.py migrate
python manage.py runserver
```

## URL Map
| Method | Path | Handler | Purpose |
|---|---|---|---|
| GET | `/` | `updateData.views.customerData` | Render contact form |
| POST | `/` | `updateData.views.customerData` | Save submission and redirect |
| GET/POST | `/customer-data/` | `updateData.views.customerData` | Same handler via app route |
| GET | `/success/` | `updateData.views.success` | Render success page |
| GET | `/submissions/` | `updateData.views.submissions` | Searchable list of submissions |
| GET | `/submissions/export.csv` | `updateData.views.export_submissions_csv` | Download all submissions as CSV |
| GET | `/admin/` | Django admin | Admin console |

## Submissions Dashboard Features
- Server-side search across `name`, `email`, `phone`, and `message`.
- Server-side sort by `id`, `name`, `email` with asc/desc order.
- Server-side pagination (`10`, `25`, `50` per page).
- Client-side quick filters on current page (`All`, `Has Website`, `Long Message`).
- Expand/collapse full message rows.
- Dense/regular table density toggle.
- Keyboard shortcut: `/` focuses dashboard search input.

## Data Model
`updateData.models.UpdateData`

| Field | Type | Constraints |
|---|---|---|
| `name` | `CharField` | `max_length=50` |
| `email` | `EmailField` | required |
| `phone` | `CharField` | `max_length=10`, optional |
| `website` | `URLField` | optional |
| `message` | `TextField` | `max_length=800`, optional |

## Request Lifecycle (Contact Form)
1. User opens `/`.
2. Template `templates/updateAPI/index.html` renders form.
3. Form POST hits `customerData`.
4. View reads fields from `request.POST`.
5. ORM creates `UpdateData` record.
6. Success/error message added via Django messages.
7. User is redirected back to `/`.

## Developer Workflow
```bash
# Validate project configuration
python manage.py check

# Create migration files after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin account
python manage.py createsuperuser

# Open Django shell
python manage.py shell
```

## Data Operations
### Export submissions (JSON)
```bash
python manage.py dumpdata updateData.UpdateData --indent 2 > updatedata_backup.json
```

### Import submissions (JSON)
```bash
python manage.py loaddata updatedata_backup.json
```

## Production Readiness Checklist
- Set `DEBUG=False`.
- Configure strict `ALLOWED_HOSTS`.
- Rotate and protect `SECRET_KEY`.
- Use environment variables for sensitive config.
- Serve static files via web server/CDN.
- Use managed DB with backups.
- Add centralized logging and error tracking.

## Troubleshooting
### Port conflict
Run on a different port:
```bash
python manage.py runserver 127.0.0.1:8001
```

### MySQL connection refused
- Confirm MySQL is running.
- Verify host/port credentials.
- Test with SQLite by unsetting `USE_MYSQL` or setting `USE_MYSQL=0`.

### Missing dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirement.txt
```

## Testing Status
`updateData/tests.py` exists but currently has no implemented test coverage for form submission behavior. Add tests for:
- successful POST persistence
- invalid payload handling
- message rendering on redirect

## License
No license file is currently defined.
