import time
import random
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from selenium import webdriver


class Tabelog_Data_Collect:
    """
    tabelogサイトからデータを収集するクラス

    Attribute
     BASE_URL: TabelogのTOPページ
     areas: 探索するwリアのリスト
     menus: 探索するメニューのリスト
     items_urls: 収集した店舗URLのリスト。
     detail_infos: 収集した店舗詳細情報のリスト。
     output_folder_base: ベースとなる出力フォルダ名。
     driver: Selenium WebDriverのインスタンス。
    """

    BASE_URL = "https://tabelog.com/"

    def __init__(self, areas: list[str], menus: list[str]):
        self.areas = areas
        self.menus = menus

        # 収集したURLを格納する変数
        self.items_urls: list[str] = []

        # 収集した店舗情報を格納する変数
        self.detail_infos: list[dict] = []

        # データを書き込むためのベースディレクトリ
        self.output_folder_base_name = "data/source_data"
        self.output_folder_area = ""

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # ヘッドレスモード（必要に応じて有効化）
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(
            service=webdriver.chrome.service.Service(ChromeDriverManager().install())
        )
        print(f"Initialized with areas: {self.areas}, menus: {self.menus}")

        # User-Agentリスト
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
            # 他のUser-Agentを追加可能
        ]

    def main(self):
        self.app()

    def app(self):
        for area in self.areas:
            print(f"Collecting data for area: {area}")
            self.make_folder(area)
            for menu in self.menus:
                print(f"  Collecting for menu: {menu}")
                self.data_collect(area, menu)

    # フォルダの作成
    def make_folder(self, area: str):
        self.output_folder_area = os.path.join(self.output_folder_base_name, area)
        os.makedirs(self.output_folder_area, exist_ok=True)

    # areaとmenuからデータ収集を行う
    def data_collect(self, area: str, menu: str):
        print("探索エリア→", area, "探索するメニューの名前→", menu)
        self.items_urls = []
        self.detail_infos = []
        self.go_to_top_page()
        self.collect_urls(menu, area)
        self.get_detail_info()
        self.make_file(menu)

    # 1つのエリアの中で1つのメニューのurlを収集する
    def collect_urls(self, menu: str, area: str):
        self.go_to_input_keyword_page(menu, area)
        self.one_menu_collect_urls()
        self.go_to_top_page()

    # TOPページに移動する
    def go_to_top_page(self):
        self.driver.get(self.BASE_URL)
        print("TOPページに遷移する")

    # tabelogサイトの検索欄にkeywordを入力する
    def go_to_input_keyword_page(self, menu: str, area: str):

        area_element = self.driver.find_element(By.CSS_SELECTOR, "#sa")
        key_word_element = self.driver.find_element(By.CSS_SELECTOR, "#sk")

        area_element.send_keys(area)
        key_word_element.send_keys(menu)

        botton_element = self.driver.find_element(
            By.CSS_SELECTOR, "#js-global-search-btn"
        )
        self.random_wait()

        self.driver.execute_script("arguments[0].click();", botton_element)
        print("メニューの入力が完了した")

    # 1つのメニューのURLを収集する
    def one_menu_collect_urls(self):
        page_num = 1

        while True:
            self.get_items_urls()
            if not self.new_goto_next_page(page_num):
                break
            page_num += 1

        print(f"収集した全url:{self.items_urls}")

    def new_goto_next_page(self, page: int) -> bool:
        try:
            next_button = self.driver.find_element(
                By.CLASS_NAME, "c-pagination__arrow--next"
            )
            self.random_wait()
            next_button.click()
            print(f"Moved to page {page + 1}")
            return True
        except:
            print("Reached the last page.")
            return False

    # ファイルの作成
    def make_file(self, menu: str):
        df = pd.DataFrame(self.detail_infos)
        output_file = os.path.join(self.output_folder_area, f"{menu}.csv")
        df.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"Saved data to {output_file}")

    # 要素が見つからなかったときの時間制限を設ける
    def get_element_with_timeout(self, by, value, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"要素が見つかりませんでした: {value}")
            return None

    # ランダムな時間待機させることでbot認定させないようにする
    def random_wait(self, min_sec=2, max_sec=5):
        wait_time = random.uniform(min_sec, max_sec)
        print(f"Waiting for {wait_time:.2f} seconds")
        time.sleep(wait_time)

    # 収集したurlから店内情報を取得する
    def get_detail_info(self):
        for url in self.items_urls:

            # 1つの店の詳細情報
            detail_one_info = {}

            # URLを取り出してお店のページに行く
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#js-detail-score-open > p > b > span")
                )
            )

            # 1店舗の詳細情報を取り出す
            self.get_one_store_info(detail_one_info)
            self.detail_infos.append(detail_one_info)
        print("全ての店舗の情報を格納した")
        print(self.detail_infos)

    # 1つの店舗の詳細情報を取り出す
    def get_one_store_info(self, detail_one_info):
        self.star_evaluation_info_get(detail_one_info)
        self.store_infos_get(detail_one_info)

    # そのお店の評価(星)を取り出す
    def star_evaluation_info_get(self, detail_one_info):
        star_evaluation_element = self.get_element_with_timeout(
            By.CSS_SELECTOR, "#js-detail-score-open > p > b > span", timeout=5
        )
        if star_evaluation_element:
            star_evaluation = star_evaluation_element.text
            star_evaluation = "None-info" if star_evaluation == "-" else star_evaluation
            detail_one_info["星5段階評価"] = star_evaluation
            print("星5段階情報取得成功")
        else:
            detail_one_info["星5段階評価"] = "None-info"
            print("星5段階情報が見つかりませんでした")

    # 詳細ページから店舗基本情報を取り出す
    def store_infos_get(self, detail_one_info: dict):
        detail_infos_element = self.get_element_with_timeout(
            By.CSS_SELECTOR, "#rst-data-head > table:nth-child(2)", timeout=5
        )
        if detail_infos_element:
            detail_info_trs = detail_infos_element.find_elements(By.TAG_NAME, "tr")
            self.store_detail_infos_get(detail_info_trs, detail_one_info)
            print("店舗基本情報を見つけることに成功")
        else:
            print("店舗基本情報が見つかりませんでした")
        time.sleep(1)

    # 店舗基本情報から各情報を取り出す
    def store_detail_infos_get(self, detail_info_trs, detail_one_info):

        # 項目とその情報をひとつづつ取り出して辞書にして格納する
        for tr in detail_info_trs:

            # 項目名を取り出し
            th_text = tr.find_element(By.TAG_NAME, "th").text
            print("項目名取得成功")

            # 項目キーの文字整形
            self.text_th_maked(th_text)

            # 「予算」の項目は飛ばす
            if th_text == "予算":
                continue

            elif th_text == "予算（口コミ集計）":
                arial_elements = tr.find_elements(By.TAG_NAME, "span")

                dinner_price = ""
                lunch_price = ""

                for i in arial_elements:
                    try:
                        arial_element = i.find_element(By.TAG_NAME, "i")
                        label = arial_element.get_attribute("aria-label")

                        if label == "Dinner":
                            dinner_price = i.text
                        if label == "Lunch":
                            lunch_price = i.text
                    except:
                        continue

                td_text = self.text_td_maked(dinner_price)
                td_text = self.text_td_maked(lunch_price)

                detail_one_info["Dinner"] = dinner_price
                detail_one_info["Lunch"] = lunch_price

            else:
                # 項目バリューの値の取り出し
                td_text = tr.find_element(By.TAG_NAME, "td").text

                td_text = self.text_td_maked(td_text)
                detail_one_info[th_text] = td_text

    # 格納する項目バリューの文字整形
    def text_td_maked(self, td_text):
        td_text = td_text.replace("\n", " ")
        td_text = td_text.replace("大きな地図を見る", "")
        td_text = td_text.replace("周辺のお店を探す", "")
        td_text = td_text.replace("利用金額分布を見る", "")
        if not td_text.strip():
            td_text = "Non-Info"
        return td_text

    # 格納する項目キーの文字整形
    def text_th_maked(self, th_text):
        th_text = th_text.replace("\n", " ")
        th_text = th_text.replace("予約・ お問い合わせ", "お問い合わせ")

    # 画面にあるURLを取得する
    def get_items_urls(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "js-rstlist-info"))
        )
        one_page_rst_body = self.driver.find_element(By.CLASS_NAME, "js-rstlist-info")
        one_page_rst_body_componets = one_page_rst_body.find_elements(
            By.CLASS_NAME, "list-rst__rst-data"
        )
        one_page_components_a_tag = [
            i.find_element(By.CLASS_NAME, "list-rst__rst-name-target")
            for i in one_page_rst_body_componets
        ]
        one_page_detail_urls = [
            i.get_attribute("href") for i in one_page_components_a_tag
        ]
        self.items_urls.extend(one_page_detail_urls)
        print("1ページ分のurlsを収集した")


if __name__ == "__main__":
    main = Tabelog_Data_Collect(
        areas=["北千住", "南流山"], menus=["スペイン料理", "刀削麺"]
    )
    main.main()
