from urllib.parse import quote

from django.db import models

ICON_CHOICES = [
    ("spa", "Spa"), ("hand", "Hand"), ("fire", "Fire"), ("leaf", "Leaf"),
    ("activity", "Activity"), ("footprints", "Footprints"), ("droplet", "Droplet"),
    ("smile", "Smile"), ("heart", "Heart"), ("star", "Star"),
]

ICON_PATHS = {
    "spa": "M12 3c3 4 5 7 5 10a5 5 0 0 1-10 0c0-3 2-6 5-10z",
    "hand": "M8 13V5a1.5 1.5 0 0 1 3 0v6m0-7a1.5 1.5 0 0 1 3 0v7m0-5a1.5 1.5 0 0 1 3 0v8a6 6 0 0 1-6 6h-1a6 6 0 0 1-5-3l-2-4a1.5 1.5 0 0 1 3-1l2 2",
    "fire": "M12 3c1 4 5 5 5 10a5 5 0 0 1-10 0c0-2 1-3 2-4 0 2 1 3 2 3 0-3-1-5 1-9z",
    "leaf": "M5 19c0-9 5-14 14-14 0 9-5 14-14 14zM5 19l8-8",
    "activity": "M3 12h4l3-8 4 16 3-8h4",
    "footprints": "M8 4c2 0 3 2 3 5s-1 4-3 4-3-1-3-4 1-5 3-5zM16 11c2 0 3 2 3 5s-1 4-3 4-3-1-3-4 1-5 3-5z",
    "droplet": "M12 3c4 5 6 8 6 11a6 6 0 0 1-12 0c0-3 2-6 6-11z",
    "smile": "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM8 14c1 2 3 3 4 3s3-1 4-3M9 9h.01M15 9h.01",
    "heart": "M12 20s-8-5-8-11a4.5 4.5 0 0 1 8-3 4.5 4.5 0 0 1 8 3c0 6-8 11-8 11z",
    "star": "M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z",
}

DEFAULT_HOURS = (
    "Monday to Friday|9:00 am - 9:00 pm\n"
    "Saturday|9:00 am - 10:00 pm\n"
    "Sunday|11:00 am - 7:00 pm"
)


class SiteSettings(models.Model):
    business_name = models.CharField(max_length=120, default="Secret Desire Massage Spa")
    tagline = models.CharField(max_length=160, default="Relax. Restore. Renew.")
    location = models.CharField(max_length=160, default="Town, Kenya")
    phone = models.CharField(max_length=30, default="+254XXXXXXXXX")
    whatsapp = models.CharField(
        max_length=20, default="254XXXXXXXXX",
        help_text="Digits only, with country code, e.g. 2547XXXXXXXX",
    )
    email = models.EmailField(default="info@example.com")
    instagram_url = models.URLField(blank=True, default="https://instagram.com/")
    tiktok_url = models.URLField(blank=True, default="https://tiktok.com/")
    facebook_url = models.URLField(blank=True, default="https://facebook.com/")
    show_prices = models.BooleanField(default=True)
    currency = models.CharField(max_length=10, default="KES")
    price_note = models.CharField(max_length=200, default="Prices may change. Confirm on WhatsApp.")
    booking_message_template = models.CharField(
        max_length=250, default="Hello Secret Desire, I would like to book: {service}",
        help_text="Use {service} where the service name should appear.",
    )
    hero_headline = models.CharField(max_length=160, default="Unwind in a space made for quiet.")
    hero_subheadline = models.CharField(
        max_length=250, default="Professional massage and body care, by appointment.",
    )
    hero_image = models.ImageField(upload_to="hero/", blank=True)
    home_intro = models.TextField(default=(
        "Secret Desire is a private massage spa where trained therapists focus on one thing: "
        "helping your body let go. Every session starts with a short chat about what you need. "
        "Rooms are quiet, clean and warm. Book in minutes on WhatsApp."
    ))
    about_story = models.TextField(default="[placeholder] Add the story of the spa here.")
    about_mission = models.TextField(
        default="To give every client a safe, respectful and restorative experience.",
    )
    about_values = models.TextField(
        default="Respect and privacy.\nSkilled, honest care.\nCleanliness in every detail.\nFair, clear pricing.",
        help_text="One value per line.",
    )
    about_image = models.ImageField(upload_to="about/", blank=True)
    hygiene_note = models.TextField(default=(
        "Linen is changed for every client. Surfaces and tools are cleaned between sessions. "
        "Therapists wash their hands before and after each treatment."
    ))
    business_hours = models.TextField(
        default=DEFAULT_HOURS, help_text="One line per row, in the form: Day|Hours",
    )

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.business_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def whatsapp_link(self, service=""):
        text = self.booking_message_template.replace("{service}", service or "a massage")
        return f"https://wa.me/{self.whatsapp}?text={quote(text)}"

    def hours_rows(self):
        rows = []
        for line in self.business_hours.splitlines():
            if "|" in line:
                day, hours = line.split("|", 1)
                rows.append((day.strip(), hours.strip()))
        return rows

    def values_list(self):
        return [v.strip() for v in self.about_values.splitlines() if v.strip()]


class Service(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    duration = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default="spa")
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    @property
    def icon_path(self):
        return ICON_PATHS.get(self.icon, ICON_PATHS["spa"])


class Package(models.Model):
    name = models.CharField(max_length=120)
    duration = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    includes = models.CharField(max_length=250)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="team/", blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ("massage", "Massage"), ("facials", "Facials"),
        ("rooms", "Rooms"), ("team", "Team"),
    ]
    image = models.ImageField(upload_to="gallery/")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="massage")
    caption = models.CharField(max_length=160, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or f"Gallery image {self.pk}"


class FAQ(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    service = models.CharField(max_length=120, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.created_at:%Y-%m-%d})"

    def whatsapp_text(self):
        parts = [f"Hello Secret Desire, I am {self.name}."]
        if self.service:
            parts.append(f"Service: {self.service}.")
        if self.message:
            parts.append(self.message)
        return " ".join(parts)
