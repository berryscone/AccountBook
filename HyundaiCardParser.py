import pandas as pd
from datetime import datetime


class HyundaiCardParser:
    cols_to_drop = ["이용카드", "할부/회차", "적립/할인율(%)", "예상적립/할인", "결제후잔액", "수수료(이자)"]
    col_map = {"이용일": "Date", "이용가맹점": "Place", "이용금액": "Price", "결제원금": "Principal"}

    def __init__(self, file_name):
        self.file_name = file_name

    def parse(self):
        data = pd.read_html(self.file_name)[0]

        # 컬럼이 멀티인덱스로 나오기 때문에 불필요한 1,2번째 인덱스를 제거
        data.columns = data.columns.droplevel([0, 1])

        # 불필요한 컬럼 및 데이터가 없는 행 제거
        data = data.drop(columns=self.cols_to_drop)
        data = data.dropna()

        # 모든 카드사 데이터의 열 이름을 통일
        data = data.rename(columns=self.col_map)

        # 금액이 0인 부분 제거 (할인, 합계 등)
        data = data[data["Price"] != 0]

        # Date 열을 date 포맷으로 변경
        data["Date"] = data["Date"].apply(lambda x: datetime.strptime(x, "%Y년 %m월 %d일").date())

        data["Price"] = -data["Price"].astype(int)
        data["Principal"] = -data["Principal"].astype(int)
        data["Pay"] = "현대"

        return data.reset_index(drop=True)
