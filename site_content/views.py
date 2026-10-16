from urllib.parse import quote

from django.shortcuts import redirect, render

from .forms import ContactForm
from .models import (FAQ, ContactMessage, GalleryImage, Package, Service,
                     SiteSettings, TeamMember, Testimonial)


def _active(model):
    return model.objects.filter(is_active=True)


def home(request):
    return render(request, "home.html", {
        "page_title": "Private Massage Spa",
        "page_desc": "Professional massage, facials and body treatments in a calm, private setting. Book on WhatsApp.",
        "services": _active(Service)[:6],
        "testimonials": _active(Testimonial)[:3],
        "gallery": _active(GalleryImage)[:6],
    })


def about(request):
    return render(request, "about.html", {
        "page_title": "About",
        "page_desc": "Learn about our spa, our therapists, our values and our hygiene standards.",
        "team": _active(TeamMember),
    })


def services(request):
    return render(request, "services.html", {
        "page_title": "Services",
        "page_desc": "Browse massage, facial and body treatments. Book any service on WhatsApp.",
        "services": _active(Service),
    })


def pricing(request):
    return render(request, "pricing.html", {
        "page_title": "Pricing",
        "page_desc": "Clear prices for every massage, facial, body treatment and package.",
        "services": _active(Service),
        "packages": _active(Package),
    })


def gallery(request):
    return render(request, "gallery.html", {
        "page_title": "Gallery",
        "page_desc": "Photos of our rooms, treatments and team.",
        "images": _active(GalleryImage),
    })


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            request.session["last_contact"] = msg.pk
            return redirect("/contact/?sent=1")
    else:
        form = ContactForm()

    sent_wa = None
    if request.GET.get("sent") and request.session.get("last_contact"):
        msg = ContactMessage.objects.filter(pk=request.session["last_contact"]).first()
        if msg:
            sent_wa = f"https://wa.me/{SiteSettings.get_solo().whatsapp}?text={quote(msg.whatsapp_text())}"

    return render(request, "contact.html", {
        "page_title": "Contact",
        "page_desc": "Contact us by WhatsApp, phone, email or form. See opening hours and answers to common questions.",
        "form": form,
        "sent": bool(sent_wa),
        "sent_wa": sent_wa,
        "faqs": _active(FAQ),
    })
