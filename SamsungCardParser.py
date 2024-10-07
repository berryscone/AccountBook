import pandas as pd
from datetime import datetime


class SamsungCardParser:
    cols_to_drop = ["이용구분", "총할부금액", "이용혜택", "혜택금액", "개월", "회차", "이자/수수료", "포인트명", "적립금액", "입금후잔액"]
    col_map = {"이용일": "Date", "가맹점": "Place", "이용금액": "Price", "원금": "Principal"}

    def __init__(self, file_name):
        self.file_name = file_name

    def parse(self):
        data = pd.read_excel(self.file_name, header=2)

        # 불필요한 컬럼 및 데이터가 없는 행 제거
        data = data.drop(columns=self.cols_to_drop)
        data = data.dropna()

        # 모든 카드사 데이터의 열 이름을 통일
        data = data.rename(columns=self.col_map)

        # 금액이 0인 부분 제거 (할인, 합계 등)
        data = data[data["Price"] != 0]

        # Date 열을 date 포맷으로 변경
        data["Date"] = data["Date"].apply(lambda x: datetime.strptime(str(int(x)), "%Y%m%d").date())

        data["Price"] = -data["Price"].str.replace(",", "").astype(int)
        data["Principal"] = -data["Principal"].str.replace(",", "").astype(int)
        data["Pay"] = "삼성"

        return data.reset_index(drop=True)
