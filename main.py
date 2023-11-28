from HCardParser import HCardParser
from SCardParser import SCardParser
from KBankParser import KBankParser
import pandas as pd

data_list = []

hcard_parser = HCardParser('hyundaicard_20231128.xls')
hcard_data = hcard_parser.parse()
data_list.append(hcard_data)

scard_parser = SCardParser('이용대금명세서(신용카드).xls')
scard_data = scard_parser.parse()
data_list.append(scard_data)

kbank_parser = KBankParser("카카오뱅크_거래내역_N5838885598_2023100716381561.xlsx")
kbank_data = kbank_parser.parse()
data_list.append(kbank_data)

data = pd.concat(data_list, ignore_index=True)
data = data.sort_values(by="Date", ascending=True, ignore_index=True)

print()