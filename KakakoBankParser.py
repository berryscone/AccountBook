import pandas as pd
import xlrd
from datetime import datetime


class KakaoBankParser:
    cols_to_drop = ['구분', '거래 후 잔액', '거래구분', '메모']
    col_map = {"거래일시": "Date", "내용": "Place", "거래금액": "Price"}

    def __init__(self, file_name):
        self.file_name = file_name

    def parse(self):
        data = pd.read_excel(self.file_name)

        # 위와 오른쪽에 불필요한 부분 제거
        data = data.iloc[9:, 1:]

        # 열 이름 변경
        data.columns = data.iloc[0]
        data = data.iloc[1:]
        data = data.reset_index(drop=True)

        # 불필요한 컬럼 및 데이터가 없는 행 제거
        data = data.drop(columns=self.cols_to_drop)
        data = data.dropna()

        # 모든 카드사 데이터의 열 이름을 통일
        data = data.rename(columns=self.col_map)

        # Date 열을 date 포맷으로 변경
        data["Date"] = data["Date"].apply(lambda x: datetime.strptime(x[:10], "%Y.%m.%d").date())

        # Price 열의 부호를 변경
        data["Price"] = pd.to_numeric(data["Price"].str.replace(',', ''))

        # 존재하지 않는 결제원금 열 추가
        data["Principal"] = data["Price"]

        data["Pay"] = "카카오뱅크"

        return data.reset_index(drop=True)
