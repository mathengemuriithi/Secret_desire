# Secret Desire Massage Spa (Django)

Server-rendered Django site. All content is edited in the Django admin at `/admin/`. No redeploy is needed to change content.

## 1. Local setup
```
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_content
python manage.py createsuperuser
python manage.py runserver
```
The initial migration (`0001_initial.py`) is included. Run `python manage.py makemigrations` only if you change models.

## 2. Log in and edit
Open http://127.0.0.1:8000/admin/ and sign in. "Site settings" opens directly to the single settings form (business details, phone, WhatsApp, email, socials, hero text, about text, opening hours).

## 3. Upload images
- Hero image, about image: Site settings.
- Team photos: Team members.
- Gallery: Gallery images (choose a category: massage, facials, rooms, team).
Only upload photos you own or have permission to use, especially photos of people.

## 4. Show or hide prices
Site settings, tick or untick "Show prices". When off, every price shows "Request price on WhatsApp" and booking buttons still work.

## 5. Add, reorder, deactivate
Services, Packages, Testimonials, Team members, Gallery images and FAQs all have an Order number and an Is active tick box. Edit both directly in the list view and click Save. Lower numbers appear first. Unticking Is active hides an item without deleting it.

## 6. Deploy to Render
1. Push the project to GitHub.
2. In Render, choose New, then Blueprint, and connect the repo. Render reads `render.yaml`.
3. Add `ALLOWED_HOSTS` (your Render hostname) and `CSRF_TRUSTED_ORIGINS` (`https://your-app.onrender.com`).
4. Deploy. `build.sh` installs, collects static files, migrates and seeds content.
5. Create an admin user from the Render shell: `python manage.py createsuperuser`.

## 7. Media storage
The persistent disk in `render.yaml` needs a paid Render plan. On the free tier, remove the `disk` block and set up Cloudinary (`django-cloudinary-storage`) for images, or accept that uploads reset on each redeploy. Contact form messages are stored in the database, viewable under Contact messages in the admin.
