import pandas as pd
from datetime import datetime


class HanaCardParser:
    col_map = {"거래일자": "Date", "가맹점명": "Place", "이용금액": "Price"}

    def __init__(self, file_name):
        self.file_name = file_name

    def parse(self):
        data = pd.read_excel(self.file_name)
        first_col = data.iloc[:, 0]
        start_row_idx = first_col[first_col == '거래일자'].index[0]
        data = data.iloc[start_row_idx:, :]

        # 첫 번째 행 trimming 하고 헤더로 설정
        data.iloc[0] = data.iloc[0].str.strip()
        data.columns = data.iloc[0]
        data = data[1:]

        # 첫 번째 열에서 YYYY.MM.DD 포맷이 아닌 행은 drop
        data = data[data.iloc[:, 0].str.match(r'^\d{4}\.\d{2}\.\d{2}$')]

        # 열 에서 '거래일자', '가맹점명', '이용금액' 빼고 모두 drop
        data = data[list(self.col_map.keys())]
        data = data.rename(columns=self.col_map)

        # 다른 데이터와 포맷 일치
        data["Date"] = data["Date"].apply(lambda x: datetime.strptime(x, "%Y.%m.%d").date())
        data["Price"] = -data["Price"].astype(int)
        data["Principal"] = data["Price"]
        data["Pay"] = "하나"

        return data.reset_index(drop=True)
