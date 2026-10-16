from django import forms

from .models import ContactMessage, Service

FIELD_CLASS = (
    "w-full rounded border border-ink/30 bg-white px-4 py-3 text-ink "
    "focus:border-gold focus:outline-none focus:ring-2 focus:ring-gold"
)


class ContactForm(forms.ModelForm):
    service = forms.ChoiceField(required=False)

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "service", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        names = Service.objects.filter(is_active=True).values_list("name", flat=True)
        self.fields["service"].choices = [("", "Select a service")] + [(n, n) for n in names]
        for field in self.fields.values():
            field.widget.attrs["class"] = FIELD_CLASS
