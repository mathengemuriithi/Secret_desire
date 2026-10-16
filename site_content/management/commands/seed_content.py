from django.core.management.base import BaseCommand

from site_content.models import FAQ, Package, Service, SiteSettings, Testimonial

SERVICES = [
    ("Swedish Massage", "swedish", "60 min", 3000, "spa", "Gentle full-body relaxation."),
    ("Deep Tissue Massage", "deep-tissue", "60 min", 3500, "hand", "Firm pressure for muscle tension."),
    ("Hot Stone Massage", "hot-stone", "75 min", 4000, "fire", "Warm stones to melt stiffness."),
    ("Aromatherapy Massage", "aromatherapy", "60 min", 3500, "leaf", "Essential oils for calm and balance."),
    ("Sports Massage", "sports", "45 min", 3000, "activity", "Targeted recovery for active bodies."),
    ("Reflexology", "reflexology", "45 min", 2500, "footprints", "Pressure points on the feet."),
    ("Body Scrub and Wrap", "body-scrub", "90 min", 5000, "droplet", "Exfoliate, nourish, and hydrate."),
    ("Facial Treatment", "facial", "60 min", 3500, "smile", "Cleanse, tone, and refresh."),
    ("Couples Massage", "couples", "60 min", 6000, "heart", "Side-by-side relaxation for two."),
    ("Full Body Relaxation", "full-body", "120 min", 8000, "star", "Complete head-to-toe experience."),
]
PACKAGES = [
    ("Refresh Half Day", "2 hrs", 7000, "Massage + Facial"),
    ("Restore Full Day", "4 hrs", 12000, "Massage + Scrub + Facial"),
    ("Couples Escape", "3 hrs", 15000, "Couples Massage + Facial"),
]
TESTIMONIALS = [
    ("Wanjiru", "Best massage I have had in years. Very professional."),
    ("Brian", "Clean rooms, skilled therapists, and fair prices."),
    ("Achieng", "Booked on WhatsApp and was attended to within the hour."),
]
FAQS = [
    ("How do I book?", "Tap Book on WhatsApp, choose a service and we will confirm a time."),
    ("Can I cancel or reschedule?", "Yes. Message us at least a few hours before your slot."),
    ("Which payment methods do you accept?", "[placeholder] Cash and M-Pesa."),
    ("Which treatment should I choose?", "Swedish for relaxation, deep tissue for tight muscles. Ask us on WhatsApp if unsure."),
    ("Do you offer couples sessions?", "Yes. See the Couples Massage and the Couples Escape package."),
    ("Should I tell you about health conditions?", "Yes. Tell us about injuries, allergies or pregnancy so we can adjust your treatment."),
]


class Command(BaseCommand):
    help = "Create default site content. Safe to run more than once."

    def handle(self, *args, **options):
        SiteSettings.get_solo()
        for i, (name, slug, dur, price, icon, desc) in enumerate(SERVICES):
            Service.objects.get_or_create(slug=slug, defaults={
                "name": name, "duration": dur, "price": price,
                "icon": icon, "description": desc, "order": i,
            })
        for i, (name, dur, price, inc) in enumerate(PACKAGES):
            Package.objects.get_or_create(name=name, defaults={
                "duration": dur, "price": price, "includes": inc, "order": i,
            })
        for i, (name, text) in enumerate(TESTIMONIALS):
            Testimonial.objects.get_or_create(name=name, defaults={"text": text, "order": i})
        for i, (q, a) in enumerate(FAQS):
            FAQ.objects.get_or_create(question=q, defaults={"answer": a, "order": i})
        self.stdout.write(self.style.SUCCESS("Content seeded."))
