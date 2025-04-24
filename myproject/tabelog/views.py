from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import TabelogForm
from .models import Tabelog, AdminUser


class TabelogFormView(View):
    template_name = "tabelog/index.html"  # 使用するテンプレートファイル名

    def get(self, request, admin_id):
        # GETリクエスト時に空のフォームを表示
        form = TabelogForm()
        return render(request, self.template_name, {"form": form, "admin_id": admin_id})

    def post(self, request, admin_id):
        # POSTリクエスト時にフォームを処理
        form = TabelogForm(request.POST)
        if form.is_valid():
            # フォームが有効な場合、Tabelogインスタンスを作成
            tabelog = form.save(commit=False)
            # admin_idを取得し、AdminUserを取得
            admin_user = get_object_or_404(AdminUser, id=admin_id)
            # TabelogインスタンスにAdminUserを関連付け
            tabelog.admin_user = admin_user
            form.save()
            # フォームが有効であればリダイレクト
            return redirect(
                "tabelog:confirm", admin_id=admin_id
            )  # 成功後のページを指定（仮に'success'としています）
        else:
            # フォームが無効であれば再表示
            return render(
                request, self.template_name, {"form": form, "admin_id": admin_id}
            )


tabelog_index = TabelogFormView.as_view()


class ConfirmView(View):
    template_name = "tabelog/confirm.html"  # 確認画面のテンプレートファイル名

    def get(self, request, admin_id):
        # URLからadmin_idを取得し、AdminUserを取得
        admin_user = get_object_or_404(AdminUser, id=admin_id)
        tabelog = admin_user.tabelog

        # AdminUser に紐づく NormalUser 一覧と Station 一覧を取得
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
    pass


tabelog_execution = ExecutionView.as_view()
