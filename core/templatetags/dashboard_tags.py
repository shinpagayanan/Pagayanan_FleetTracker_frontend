from django import template
from decimal import Decimal

register = template.Library()



@register.simple_tag
def is_manager(role):

    return role == "MANAGER"


@register.simple_tag
def is_auditor(role):

    return role == "AUDITOR"


@register.simple_tag
def is_staff(role):

    return role == "STAFF"





@register.filter
def peso(value):

    try:

        value = Decimal(str(value))

        return f"₱{value:,.2f}"

    except Exception:

        return "₱0.00"


@register.filter
def asset_label(asset_type):

    mapping = {

        "VEHICLE":
            "Vehicle",

        "IT":
            "IT Equipment",
    }

    return mapping.get(
        asset_type,
        asset_type
    )



@register.filter
def maintenance_due(asset):

    try:

        if asset["asset_type"] != "VEHICLE":

            return False

        return (
            asset["current_mileage"]
            >=
            asset["maintenance_interval"]
        )

    except Exception:

        return False


@register.filter
def status_color(status):
    colors = {
        "PENDING": "orange",
        "APPROVED": "green",
        "REJECTED": "red",
        "COMPLETED": "blue",
    }
    return colors.get(status, "black")

