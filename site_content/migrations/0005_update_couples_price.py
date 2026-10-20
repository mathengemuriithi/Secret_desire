from django.db import migrations

def forwards(apps, schema_editor):
    Service = apps.get_model("site_content", "Service")
    # Update the price for Couples Massage to 12000
    Service.objects.filter(name="Couples Massage").update(price=12000)

def backwards(apps, schema_editor):
    Service = apps.get_model("site_content", "Service")
    # Revert to the old price if we roll back
    Service.objects.filter(name="Couples Massage").update(price=7000)

class Migration(migrations.Migration):
    dependencies = [
        ("site_content", "0004_update_about_and_email"),
    ]
    operations = [
        migrations.RunPython(forwards, backwards),
    ]
