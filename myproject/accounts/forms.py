from django import forms
from .models import NormalUser, Station, AdminUser
from django.contrib.auth.hashers import make_password


class AdminUserForm(forms.ModelForm):

    new_station = forms.CharField(max_length=100, required=False, label="New Station")

    class Meta:
        model = AdminUser
        fields = ["email", "name", "password", "lunch_or_dinner"]

        # フォームが保存されるときにパスワードをハッシュ化する

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(
            self.cleaned_data["password"]
        )  # パスワードのハッシュ化
        if commit:
            user.save()  # AdminUserの保存
            self.save_m2m()  # ManyToManyField の保存

            # 新しい駅を作成してAdminUserに関連付ける処理
            new_station_name = self.cleaned_data.get("new_station")
            if new_station_name:
                station, created = Station.objects.get_or_create(name=new_station_name)
                user.stations.add(station)  # 新しい駅をAdminUserに関連付ける
        return user


class NormalUserForm(forms.ModelForm):
    class Meta:
        model = NormalUser
        fields = ["name", "select_food", "ratio"]
