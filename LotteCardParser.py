import pandas as pd
from datetime import datetime


class LotteCardParser:
    col_map = {"이용일": "Date", "이용가맹점": "Place", "이용총액": "Price"}

    def __init__(self, file_name):
        self.file_name = file_name

    def parse(self):
        # data = pd.read_excel(self.file_name, engine='xlrd')
        data = pd.read_html(self.file_name)[1]
        data.columns = data.columns.droplevel([0])

        # 첫 번째 열에서 YYYY.MM.DD 포맷이 아닌 행은 drop
        data = data[data.iloc[:, 0].str.match(r'^\d{4}\.\d{2}\.\d{2}$')]
        data["이용총액"] = data["원금"].fillna(0) + data["수수료"].fillna(0)

        # 열 에서 '이용일', '이용가맹점', '이용총액' 빼고 모두 drop
        data = data[list(self.col_map.keys())]
        data = data.rename(columns=self.col_map)

        # 다른 데이터와 포맷 일치
        data["Date"] = data["Date"].apply(lambda x: datetime.strptime(x, "%Y.%m.%d").date())
        data["Price"] = -data["Price"].astype(int)
        data["Principal"] = data["Price"]
        data["Pay"] = "롯데"

        return data.reset_index(drop=True)
