from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import TabelogForm
from .models import Tabelog, AdminUser
from accounts.models import NormalUser, Station
from .app_execute import AplicationExecution


class TabelogFormView(View):
    template_name = "tabelog/index.html"

    def get(self, request, admin_id):
        form = TabelogForm()
        return render(request, self.template_name, {"form": form, "admin_id": admin_id})

    def post(self, request, admin_id):
        form = TabelogForm(request.POST)
        if form.is_valid():
            tabelog = form.save(commit=False)
            admin_user = get_object_or_404(AdminUser, id=admin_id)
            tabelog.admin_user = admin_user
            form.save()
            return redirect("tabelog:confirm", admin_id=admin_id)
        else:
            return render(
                request, self.template_name, {"form": form, "admin_id": admin_id}
            )


tabelog_index = TabelogFormView.as_view()


class ConfirmView(View):
    template_name = "tabelog/confirm.html"

    def get(self, request, admin_id):
        admin_user = get_object_or_404(AdminUser, id=admin_id)
        tabelog = admin_user.tabelog

        normal_users = admin_user.normal_users.all()
        stations = admin_user.stations.all()

        context = {
            "tabelog": tabelog,
            "admin_user": admin_user,
            "normal_users": normal_users,
            "stations": stations,
        }

        return render(request, self.template_name, context)


# URLConfで使えるビュー名
tabelog_confirm = ConfirmView.as_view()


class ExecutionView(View):
    def post(self, request, admin_id):
        execution = AplicationExecution(admin_id)
        execution.main()


tabelog_execution = ExecutionView.as_view()
