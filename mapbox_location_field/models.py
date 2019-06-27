from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from .forms import LocationField as LocationFormField


def parse_location(location_string):
    args = location_string.split(",")
    if len(args) != 2:
        raise ValidationError(_("Invalid input for a Location instance"))

    lat = args[0]
    lng = args[1]

    try:
        lat = float(lat)
    except ValueError:
        raise ValidationError(_("Invalid input for a Location instance. Latitude must be convertible to float "))
    try:
        lng = float(lng)
    except ValueError:
        raise ValidationError(_("Invalid input for a Location instance. Longitude must be convertible to float "))

    return lat, lng


class LocationField(models.CharField):
    description = _("Location field (latitude and longitude).")

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 63
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return parse_location(value)

    def to_python(self, value):
        if isinstance(value, tuple):
            return value

        if value is None:
            return value

        return parse_location(value)

    def get_prep_value(self, value):
        return "{},{}".format(value[0], value[1])

    def formfield(self, **kwargs):
        defaults = {'form_class': LocationFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)