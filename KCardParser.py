import pandas as pd
import numpy as np
import unicodedata
from datetime import datetime


class KCardParser:
    cols_to_drop = ["이용카드", "구분", np.nan, "할부개월", "회차"]
    col_map = {"이용일자": "Date", "이용하신 가맹점": "Place", "이용금액": "Price", "원금": "Principal"}

    def __init__(self, file_name):
        self.file_name = file_name

    def parse(self):
        data = pd.read_excel(self.file_name)

        # 불필요한 부분 제거
        data = data.iloc[1:, 1:10]

        # 열 이름 변경
        data.columns = data.iloc[0]
        data = data.iloc[1:]
        data = data.reset_index(drop=True)

        # 불필요한 컬럼 및 데이터가 없는 행 제거
        data = data.drop(columns=self.cols_to_drop)
        data = data.dropna()

        # 모든 카드사 데이터의 열 이름을 통일
        data = data.rename(columns=self.col_map)

        # unicode 를 normalize 하고 할인정보가 들어간 행을 제거
        data = data.map(lambda x: unicodedata.normalize("NFKD", x))
        data = data.replace(r'^\s+$', np.nan, regex=True)
        data = data.dropna()

        # Date 열을 date 포맷으로 변경
        data["Date"] = data["Date"].apply(lambda x: datetime.strptime(x, "%y.%m.%d").date())

        # Price 와 Principal 열의 부호를 변경
        data["Price"] = -pd.to_numeric(data["Price"].str.replace(',', ''))
        data["Principal"] = -pd.to_numeric(data["Principal"].str.replace(',', ''))

        data["Pay"] = "국민"

        return data.reset_index(drop=True)
