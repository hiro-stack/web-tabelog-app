from .tabelog_app.app import Application
from .models import Tabelog
from accounts.models import NormalUser, AdminUser, Station


class AplicationExecution:
    def __init__(self, admin_id):
        self.admin_id = admin_id

    def main(self):

        # 食べ物の重要度が同じときに（votes = {"ラーメン": [0.5, 0.5],"カレー": [1.0],}　合計は同じ1）人数が大きいほうをどれだけ優先させる課を決める変数
        alpha = 0.5

        # モデルに追加し忘れたので、仮で定義
        max_minutes = 30
        price_max = 1000

        areas, menus = self.get_areas_and_menus(self.admin_id)
        current_location = self.get_now_location(self.admin_id)
        votes_result = self.get_votes_result(self.admin_id)
        weight = self.get_weight(self.admin_id)
        time_is = self.get_time_is(self.admin_id)

        app = Application(
            current_location=current_location,
            areas=areas,
            menus=menus,
            max_minutes=max_minutes,
            price_max=price_max,
            time_is=time_is,
            weight=weight,
            votes_result=votes_result,
            alpha=alpha,
        )
        app.main()

    def get_areas_and_menus(self, admin_id):
        areas = list(
            Station.objects.filter(admin_user_id=admin_id)
            .values_list("name", flat=True)
            .distinct()
        )

        menus = list(
            NormalUser.objects.filter(admin_user_id=admin_id)
            .exclude(select_food__isnull=True)
            .exclude(select_food__exact="")
            .values_list("select_food", flat=True)
            .distinct()
        )

        return areas, menus

    def get_now_location(self, admin_id):
        admin_user = AdminUser.objects.get(id=admin_id)

        current_location = {
            "name": "現在地",
            "latitude": admin_user.now_latitude,
            "longitude": admin_user.now_longitude,
        }

        return current_location

    def get_votes_result(self, admin_id):
        admin_user = AdminUser.objects.get(id=admin_id)
        normal_users = NormalUser.objects.filter(admin_user=admin_user)

        votes_result = {}

        for user in normal_users:
            food = user.select_food
            ratio = user.ratio

            if food not in votes_result:
                votes_result[food] = []

            votes_result[food].append(ratio)

        return votes_result

    def get_weight(self, admin_id):
        admin_user = AdminUser.objects.get(id=admin_id)
        tabelog = admin_user.tabelog

        weight = {
            "distance": tabelog.location_priority,
            "budget": tabelog.price_priority,
            "evaluate": tabelog.store_rating_priority,
            "voice_force": tabelog.decision_power_priority,
        }

        return weight

    def get_time_is(self, admin_id):
        admin_user = AdminUser.objects.get(id=admin_id)
        return admin_user.lunch_or_dinner


if __name__ == "__main__":
    pass
