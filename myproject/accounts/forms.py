from django import forms
from .models import NormalUser, AdminUser, Station


class AdminUserForm(forms.ModelForm):
    class Meta:
        model = AdminUser
        fields = ["email", "name", "lunch_or_dinner", "now_latitude", "now_longitude"]
        labels = {
            "email": "メールアドレス",
            "name": "名前",
            "lunch_or_dinner": "昼食または夕食",
            "now_latitude": "現在の緯度",
            "now_longitude": "現在の経度",
        }
        widgets = {
            "lunch_or_dinner": forms.RadioSelect,
        }


class NormalUserForm(forms.ModelForm):
    class Meta:
        model = NormalUser
        fields = ["name", "select_food", "ratio"]
        labels = {
            "name": "名前",
            "select_food": "選択した食べ物",
            "ratio": "割合（0〜1）",
        }
        widgets = {
            "ratio": forms.NumberInput(attrs={"step": "0.1", "min": "0", "max": "1"}),
        }
        


class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ["name"]
        labels = {
            "name": "駅名",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "駅名を入力してください"}),
        }