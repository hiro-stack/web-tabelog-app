import pandas as pd
import numpy as np
import os
import sys

class Analysts:
    def __init__(self, time_is, max_price, max_minutes, weight): 

        """
        初期化メソッド。
        Args:
            time_is (str): 'lunch' または 'dinner' の指定。
            max_price (int): 最大許容価格。
            max_minutes (int): 最大許容移動時間（分）。
            weight (dict): 各項目の重みを格納した辞書。
        """

        self.time_is = time_is
        self.max_price = max_price
        self.max_minutes = max_minutes
        self.weight = weight

        #スケーリング対象のカラム
        self.columns_to_scale = ["星5段階評価", "価格", "現在地点からの徒歩(分)", "声の大きさ"]

        #標準化するときの最小値
        self.min_val_override = 0.1

        #出力用カラム
        self.output_columns = ['点数', '店名', '星5段階評価', '価格', '項目', '現在地点からの徒歩(分)', '声の大きさ', '緯度', '経度']


        self.input_folder = 'data/maked_data'
        self.input_file = 'combined_data.csv'
        self.output_folder = 'data/result_data'
        self.output_file = 'result_data.csv'

        self.result_df = pd.DataFrame()

    def main(self):
        self.app()

    def app(self):
        self.input_data()

        #データのフィルタリング
        self.data_filterling()

        #対象カラムに対し値の逆数を取る
        self.data_reciprocal()

        #対象カラムに対し値を標準化させる
        self.data_normalization(self.min_val_override)

        #対象カラムに対し、重みづけを行うをかける
        self.apply_weight()

        #点数を出す
        self.evalutate_shop()

        self.output_data()

    #入力処理
    def input_data(self):
        input_file_path = os.path.join(self.input_folder, self.input_file)
        self.result_df = pd.read_csv(input_file_path)
        print(f"データが読み込まれました:{input_file_path}")

    
    #フィルタリングメソッド
    def data_filterling(self):
        self.data_filterring_price()
        self.data_filterring_time()
        
    def data_filterring_time(self):
        self.result_df = self.result_df[self.result_df["現在地点からの徒歩(分)"] <= self.max_minutes]

    def data_filterring_price(self):
        if self.time_is == 'lunch':
            self.result_df = self.result_df[self.result_df["Lunch"] <= self.max_price]

            self.result_df = self.result_df.drop(columns=["Dinner"])
            self.result_df = self.result_df.rename(columns={"Lunch": "価格"})

        elif self.time_is == 'dinner':
            self.result_df = self.result_df[self.result_df["Dinner"] <= self.max_price]

            self.result_df = self.result_df.drop(columns=["Lunch"])
            self.result_df = self.result_df.rename(columns={"Dinner": "価格"})


    #逆数処理メソッド
    def data_reciprocal(self):
        self.data_reciprocal_price()
        self.data_reciprocal_distance()

    def data_reciprocal_price(self):
        self.result_df["価格"] = self.result_df["価格"].apply(lambda x: 1/x if x != 0 else 0)

    def data_reciprocal_distance(self):
        self.result_df["現在地点からの徒歩(分)"] = self.result_df["現在地点からの徒歩(分)"].apply(lambda x: 1/x if x != 0 else 0)


    #標準化メソッド
    def data_normalization(self, min_val_override=1):
        for col in self.columns_to_scale:
            col_min = self.result_df[col].min()
            col_max = self.result_df[col].max()

            print(col_min, col_max)

            # 全ての値が同じ場合
            if col_min == col_max:
                self.result_df[col] = min_val_override
            else:
                # 標準化計算（指定された最小値を考慮）
                self.result_df[col] = (
                    (self.result_df[col] - col_min) / (col_max - col_min)
                ) * (1 - min_val_override) + min_val_override

    #対象項目に対し重みづけを行う
    def apply_weight(self):
        self.result_df['声の大きさ'] *= self.weight['voice_force']
        self.result_df["星5段階評価"] *= self.weight['evaluate']
        self.result_df["価格"] *= self.weight['budget']
        self.result_df["現在地点からの徒歩(分)"] *= self.weight['distance']

    #点数を出す
    def evalutate_shop(self):
        self.result_df['点数'] = self.result_df[self.columns_to_scale].sum(axis=1)
        self.result_df = self.result_df.sort_values(by='点数', ascending=False)


    def output_data(self):
        current_path = os.getcwd()
        output_dir = os.path.join(current_path, self.output_folder)
        os.makedirs(output_dir, exist_ok=True)
        output_df = self.result_df[self.output_columns]
        output_path = os.path.join(self.output_folder, self.output_file)
        output_df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"ファイルが保存されました: {output_path}")

if __name__ == "__main__":
    waight = {'distance': 1.1, 'budget': 1.2, 'evaluate': 1.3, 'voice_force': 1.5}

    print(sys.executable)

    #analysis = Analysts('lunch', 5000, 1000, waight)
    #analysis.main()

