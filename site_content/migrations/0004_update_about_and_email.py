from django.db import migrations

ABOUT_STORY = (
    "Secret Desire is a private massage spa in Lavington, Nairobi. "
    "We believe that true relaxation begins with a calm, discreet space "
    "and a therapist who listens.\n\n"
    "Every session starts with a short conversation about what your body "
    "needs — whether that is relief from tension, recovery after a long "
    "week, or simply an hour of quiet.\n\n"
    "Our rooms are quiet, warm and private. Our therapists are trained, "
    "vetted and experienced. And our oils and linen are chosen with care "
    "for your skin and comfort."
)

NEW_EMAIL = "info@secretdesiressp.co.ke"

def forwards(apps, schema_editor):
    SiteSettings = apps.get_model("site_content", "SiteSettings")
    obj = SiteSettings.objects.first()
    if obj:
        obj.about_story = ABOUT_STORY
        obj.email = NEW_EMAIL
        obj.save()

def backwards(apps, schema_editor):
    SiteSettings = apps.get_model("site_content", "SiteSettings")
    obj = SiteSettings.objects.first()
    if obj:
        obj.about_story = "[placeholder] Add the story of the spa here."
        obj.email = "info@example.com"
        obj.save()

class Migration(migrations.Migration):
    dependencies = [
        ("site_content", "0003_imani_contact"),
    ]
    operations = [
        migrations.RunPython(forwards, backwards),
    ]
