# Generated for Imani's contact details + location

from django.db import migrations

WHATSAPP = "254714635585"           # digits only, no +, no 0
PHONE    = "+254 714 635 585"       # display format
LOCATION = "Lavington, Nairobi, Kenya"   # ← change if Imani wants different

def forwards(apps, schema_editor):
    SiteSettings = apps.get_model("site_content", "SiteSettings")
    obj = SiteSettings.objects.first()
    if not obj:
        obj = SiteSettings(pk=1)
    obj.whatsapp = WHATSAPP
    obj.phone = PHONE
    obj.location = LOCATION
    obj.save()

def backwards(apps, schema_editor):
    SiteSettings = apps.get_model("site_content", "SiteSettings")
    obj = SiteSettings.objects.first()
    if obj:
        obj.whatsapp = "254XXXXXXXXX"
        obj.phone = "+254XXXXXXXXX"
        obj.location = "Town, Kenya"
        obj.save()

class Migration(migrations.Migration):
    dependencies = [
        ("site_content", "0002_update_prices"),
    ]
    operations = [
        migrations.RunPython(forwards, backwards),
    ]
