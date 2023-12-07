from HCardParser import HCardParser
from SCardParser import SCardParser
from KCardParser import KCardParser
from KBankParser import KBankParser
import pandas as pd

data_list = []

hcard_parser = HCardParser('hyundaicard_20231203.xls')
hcard_data = hcard_parser.parse()
data_list.append(hcard_data)

kbank_parser = KBankParser("카카오뱅크_거래내역_N8426013673_2023120300165808.xlsx")
kbank_data = kbank_parser.parse()
data_list.append(kbank_data)

scard_parser = SCardParser('이용대금명세서(신용카드).xls')
scard_data = scard_parser.parse()
data_list.append(scard_data)

kcard_parser = KCardParser("202312_usage.xlsx")
kcard_data = kcard_parser.parse()
data_list.append(kcard_data)

data = pd.concat(data_list, ignore_index=True)
data = data.sort_values(by="Date", ascending=True, ignore_index=True)
data["Place"] = data["Place"].str.normalize("NFC")

data.to_excel("11월.xlsx", header=True, index=False)

print()
