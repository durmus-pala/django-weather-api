from django import forms
from .models import City


class CityForm(forms.ModelForm):
    name = forms.CharField(label="Enter A City Name Here:")

    class Meta:
        model = City
        fields = (
            "name",
        )
