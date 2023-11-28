import pandas as pd
from datetime import datetime


class SCardParser:
    cols_to_drop = ['이용 카드', '할 부 기 간', '회 차', '수수료 (이자)', '적용 구분', '결제 후 잔액', '포인트 적립율 (마이 신한 포인트)']
    col_map = {"이용 일자": "Date", "이용 가맹점": "Place", "이용 금액": "Price", "원금": "Principal"}

    def __init__(self, file_name):
        self.file_name = file_name

    def parse(self):
        data = pd.read_html(self.file_name)[10]

        # 컬럼이 멀티인덱스로 나오기 때문에 불필요한 1,2번째 인덱스를 제거
        data.columns = data.columns.droplevel(0)

        # 마지막 3행은 소계, 합계라 제거
        data = data.iloc[:-3]

        # 불필요한 컬럼 및 데이터가 없는 행 제거
        data = data.drop(columns=self.cols_to_drop)
        data = data.dropna()

        # 모든 카드사 데이터의 열 이름을 통일
        data = data.rename(columns=self.col_map)

        # Date 열을 date 포맷으로 변경
        data["Date"] = data["Date"].apply(lambda x: datetime.strptime(x, "%Y.%m.%d").date())

        data["Price"] = -pd.to_numeric(data["Price"].str.replace(',', ''))
        data["Principal"] = -data["Principal"].astype(int)
        data["Pay"] = "신한"

        return data.reset_index(drop=True)
