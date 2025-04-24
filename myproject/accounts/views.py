from django.views import View
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .models import AdminUser, NormalUser, Station
from .forms import AdminUserForm, NormalUserForm, StationForm


class AdminListView(View):
    template_name = "accounts/list.html"

    def get(self, request):
        admin_user = AdminUser.objects.first()  # 最初のAdminUserを取得（仮）
        users = admin_user.normal_users.all()
        stations = admin_user.stations.all()

        return render(
            request,
            self.template_name,
            {
                "admin_user": admin_user,
                "users": users,
                "stations": stations,
            },
        )


admin_list = AdminListView.as_view()


class AdminUserCreateView(View):
    template_name = "accounts/index.html"

    def get(self, request):
        admin_form = AdminUserForm()

        return render(
            request,
            self.template_name,
            {"admin_form": admin_form},
        )

    def post(self, request):
        admin_form = AdminUserForm(request.POST)

        if admin_form.is_valid():
            admin_form.save()
            return redirect("accounts:list")
        return render(request, self.template_name, {"admin_form": admin_form})


admin_create = AdminUserCreateView.as_view()


class NormalUserCreateView(View):
    template_name = "accounts/add_user.html"

    def get(self, request, admin_id):
        user_form = NormalUserForm()
        return render(
            request, self.template_name, {"user_form": user_form, "admin_id": admin_id}
        )

    def post(self, request, admin_id):
        user_form = NormalUserForm(request.POST)
        if user_form.is_valid():
            normal_user = user_form.save(commit=False)
            normal_user.admin_user = AdminUser.objects.get(id=admin_id)  # 紐づけ
            normal_user.save()
            return redirect("accounts:list")

        return render(
            request, self.template_name, {"user_form": user_form, "admin_id": admin_id}
        )


normal_create = NormalUserCreateView.as_view()


class StationCreateView(View):
    template_name = "accounts/add_station.html"

    def get(self, request, admin_id):
        station_form = StationForm()
        return render(
            request,
            self.template_name,
            {"station_form": station_form, "admin_id": admin_id},
        )

    def post(self, request, admin_id):
        station_form = StationForm(request.POST)

        if station_form.is_valid():

            station = station_form.save(commit=False)
            station.admin_user = AdminUser.objects.get(id=admin_id)
            station.save()
            return redirect("accounts:list")  # 駅一覧ページに戻る（元の画面）

        return render(
            request,
            self.template_name,
            {"station_form": station_form, "admin_id": admin_id},
        )


station_create = StationCreateView.as_view()
