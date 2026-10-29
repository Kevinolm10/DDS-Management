# DDS Football Management

**Live site:** [www.ddsfootballmanagement.com](https://www.ddsfootballmanagement.com)

Website and management platform for DDS Football Management, a football agency handling player representation, contract negotiations and transfers. The site presents the agency and its services publicly, and lets staff manage player profiles and blog content through a custom interface and the Django admin.

---

## Tech stack

| Area       | Tools |
|------------|-------|
| Backend    | Python 3.12, Django 5.1 |
| Database   | PostgreSQL (AWS RDS), SQLite for local development |
| Media      | Cloudinary |
| Frontend   | Django templates, Bootstrap 5, custom CSS, vanilla JavaScript |
| Content    | django-summernote (rich text for blog posts) |
| Hosting    | AWS EC2, nginx (reverse proxy, HTTPS), Gunicorn |
| Static     | WhiteNoise, `collectstatic` |

## Features

- Public agency site with services, team and contact form
- Player profiles (add, update, remove) with UUID-based URLs
- Blog with rich-text editing
- SEO: per-page titles and descriptions, canonical URLs, Open Graph tags, JSON-LD structured data, `sitemap.xml` and `robots.txt`
- Custom 404 and 500 error pages

## Environments and workflow

- **`main`**: production
- **`staging`**: separate server and database for testing new features
- Feature branches (e.g. `feature/custom-error-pages`) are merged through pull requests

Configuration lives in environment variables (`.env`, see `.env.example`), including `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`, `USE_POSTGRES`, `USE_CLOUDINARY` and `SECURE_HTTPS`.

## Running locally

```bash
git clone https://github.com/Kevinolm10/DDS-Management.git
cd DDS-Management
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # fill in values
python manage.py migrate
python manage.py runserver
```

## Styling

- Bootstrap 5 for layout and components, with `static/css/style.css` loaded last so site styles always override Bootstrap
- Fonts: Inter (body) and Playfair Display (headings)
- Icons: Font Awesome, loaded asynchronously since they aren't layout-critical

## Error pages

Custom templates in `templates/`:

- `404.html` extends the base layout so visitors keep the site navigation
- `500.html` is standalone HTML with inline styles, so it still renders if the database or other parts of the app are failing

To test locally, run with `DEBUG=False SECURE_HTTPS=False python manage.py runserver --insecure` and visit a URL that doesn't exist.

## Bugs and fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| App failed on Python 3.14 | Dependencies not yet compatible | Pinned the project to Python 3.12 via pyenv |
| Large image uploads rejected | nginx default upload limit | Raised `client_max_body_size` |
| Dependency conflict on install | django-summernote / bleach versions | Aligned package versions |
| Local server redirected to HTTPS | SSL redirect tied to `DEBUG` | Added a separate `SECURE_HTTPS` setting |
| Error pages showed browser default | Templates were empty | Wrote proper 404/500 templates |
| Site styles overridden by Bootstrap | Bootstrap loaded async after `style.css` | Load Bootstrap first, site CSS last |
| Gunicorn failed to start after deploy | Virtualenv renamed, scripts kept old path | Rewrote script paths in `venv/bin/` |

## Planned

- [ ] Agents model and admin management (on staging)
- [ ] Dynamic structured data generated from the database
- [ ] Gunicorn as a systemd service

## Author

Kevin – [GitHub](https://github.com/Kevinolm10)