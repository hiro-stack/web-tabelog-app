from .tabelog_app_manipulate.tabelog_data_collect import Tabelog_Data_Collect
from .tabelog_app_manipulate.data_maked import DataMaker
from .tabelog_app_manipulate.analysts import Analysts
from .tabelog_app_manipulate.mapping import Mapping


class Application:
    def __init__(
        self,
        current_location,
        areas,
        menus,
        max_minutes,
        price_max,
        time_is,
        weight,
        votes_result,
        alpha,
    ):
        self.tabelog_data_collecter = Tabelog_Data_Collect(areas, menus)
        self.data_maked = DataMaker(current_location, votes_result, alpha)
        self.analysts = Analysts(time_is, price_max, max_minutes, weight)
        self.mapping = Mapping(current_location)

    def app(self):
        self.tabelog_data_collecter.main()
        self.data_maked.main()
        self.analysts.main()
        self.mapping.main()

    def main(self):
        self.app()


if __name__ == "__main__":
    pass
