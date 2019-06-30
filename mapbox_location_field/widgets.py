from django.forms.widgets import TextInput
from django.conf import settings


class MapInput(TextInput):
    template_name = "mapbox_location_field\map_input.html"

    def __init__(self, attrs=None, map_attrs=None):
        self.map_attrs = map_attrs
        super().__init__(attrs)

    class Media:
        js = ("js\map_input.js",)
        css = {
            "all": ("css\map_input.css",)
        }

    def get_context(self, name, value, attrs):
        must_be_attrs = {
            "maxlenght": 63,
            "readonly": True,
            "placeholder": "Pick a location on map below"
        }

        attrs.update(must_be_attrs)
        attrs["class"] = attrs.get("class", "") + " js-mapbox-input-location-field"

        return super().get_context(name, value, attrs)

    def render(self, name, value, attrs=None, renderer=None):
        rend = super().render(name, value, attrs, renderer)
        rend += self.get_config_settings()
        return rend

    def get_config_settings(self):
        default_map_attrs = {
            "style": "mapbox://styles/mapbox/outdoors-v11",
            "zoom": 13,
            "center": [17.031645, 51.106715],
            "cursor_style": 'pointer',
            "marker_color": "blue",
            "rotate": False,
            "geocoder": True,
            "fullscreen_button": True,
            "navigation_buttons": True,
            "track_location_button": True,
        }
        default_map_attrs.update(self.map_attrs)
        xd = "<script>mapboxgl.accessToken = '{}';{}</script>".format(settings.MAPBOX_KEY,
                                                                      self.map_attrs_to_javascript(default_map_attrs))
        print(xd)
        return xd

    @staticmethod
    def map_attrs_to_javascript(map_attrs):
        js = ""
        js_pattern = "var map_attr_{key} = '{value}';"
        js_pattern_literally = "var map_attr_{key} = {value};"
        for key, value in map_attrs.items():
            if type(value) == list or type(value) == tuple:
                js += js_pattern_literally.format(key=key, value=list(value))
            elif type(value) == bool:
                val = str(value).lower()
                js += js_pattern_literally.format(key=key, value=val)
            else:
                js += js_pattern.format(key=key, value=value)
        return js
