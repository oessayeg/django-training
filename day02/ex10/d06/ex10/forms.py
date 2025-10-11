from django import forms
from .models import People


class MovieFilterForm(forms.Form):
    min_release_date = forms.DateField(
        label="Movies minimum release date",
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    max_release_date = forms.DateField(
        label="Movies maximum release date",
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    planet_diameter = forms.IntegerField(
        label="Planet diameter greater than", required=True, min_value=0
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        gender_choices = self._get_unique_genders()
        self.fields["gender"] = forms.ChoiceField(
            label="Character gender", choices=gender_choices, required=True
        )

    def _get_unique_genders(self):
        genders = People.objects.values_list("gender", flat=True).distinct()
        genders = [g for g in genders if g]
        return [(g, g) for g in sorted(genders)]
