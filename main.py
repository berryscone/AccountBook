from HyundaiCardParser import HyundaiCardParser
from SinhanCardParser import SinhanCardParser
from KBCardParser import KBCardParser
from KakakoBankParser import KakaoBankParser
from HanaCardParser import HanaCardParser
import pandas as pd

data_list = []

hncard_parser = HanaCardParser("하나.xls")
hncard_data = hncard_parser.parse()
data_list.append(hncard_data)

hdcard_parser = HyundaiCardParser('현대.xls')
hdcard_data = hdcard_parser.parse()
data_list.append(hdcard_data)

kbank_parser = KakaoBankParser("카카오.xlsx")
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

data.to_excel("4월.xlsx", header=True, index=False)

print()
