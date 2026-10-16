from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def wa_link(context, service=""):
    return context["site_settings"].whatsapp_link(service)


@register.simple_tag(takes_context=True)
def price(context, value):
    s = context["site_settings"]
    if not s.show_prices:
        return "Request price on WhatsApp"
    return f"{s.currency} {value:,.0f}"
