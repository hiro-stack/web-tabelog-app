from django import forms
from .models import Tabelog


class TabelogForm(forms.ModelForm):
    class Meta:
        model = Tabelog
        fields = [
            "location_priority",
            "price_priority",
            "store_rating_priority",
            "decision_power_priority",
        ]
        labels = {
            "location_priority": "現在地からの距離のの重要度",
            "price_priority": "価格の重要度",
            "store_rating_priority": "お店の評価の重要度",
            "decision_power_priority": "決定権の重要度の反映度合いの重要度",
        }
        widgets = {
            "location_priority": forms.NumberInput(
                attrs={"step": "0.1", "min": "0", "max": "1"}
            ),
            "price_priority": forms.NumberInput(
                attrs={"step": "0.1", "min": "0", "max": "1"}
            ),
            "store_rating_priority": forms.NumberInput(
                attrs={"step": "0.1", "min": "0", "max": "1"}
            ),
            "decision_power_priority": forms.NumberInput(
                attrs={"step": "0.1", "min": "0", "max": "1"}
            ),
        }
