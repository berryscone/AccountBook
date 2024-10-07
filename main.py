from HyundaiCardParser import HyundaiCardParser
from SinhanCardParser import SinhanCardParser
from KBCardParser import KBCardParser
from KakakoBankParser import KakaoBankParser
from HanaCardParser import HanaCardParser
from LotteCardParser import LotteCardParser
from SamsungCardParser import SamsungCardParser
import pandas as pd

data_list = []

sscard_parser = SamsungCardParser("삼성.xlsx")
sscard_data = sscard_parser.parse()
data_list.append(sscard_data)

hncard_parser = HanaCardParser("하나.xls")
hncard_data = hncard_parser.parse()
data_list.append(hncard_data)

# ltcard_parser = LotteCardParser("롯데.xls")
# ltcard_data = ltcard_parser.parse()
# data_list.append(ltcard_data)

hdcard_parser = HyundaiCardParser('현대.xls')
hdcard_data = hdcard_parser.parse()
data_list.append(hdcard_data)

kbank_parser = KakaoBankParser("카뱅.xlsx")
kbank_data = kbank_parser.parse()
data_list.append(kbank_data)

scard_parser = SinhanCardParser('신한.xls')
scard_data = scard_parser.parse()
data_list.append(scard_data)

kcard_parser = KBCardParser("국민.xlsx")
kcard_data = kcard_parser.parse()
data_list.append(kcard_data)

data = pd.concat(data_list, ignore_index=True)
data = data.sort_values(by="Date", ascending=True, ignore_index=True)
data["Place"] = data["Place"].str.normalize("NFC")

data.to_excel("6월.xlsx", header=True, index=False)

print()
