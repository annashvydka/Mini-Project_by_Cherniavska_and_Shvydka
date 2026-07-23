# Отримайте історичні ринкові дані для вибраного фінансового інструменту.
# Ці дані повинні включати основні показники, такі як ціна відкриття, ціна закриття, максимум, мінімум і обсяг торгів.

import yfinance as yf
import pandas as pd
#2
data = yf.download("SBUX", start="2025-01-01", end="2026-01-01")

df = data.reset_index()  #бо дата була рядками, а тепер стала окремою колонкою і замість дат 123
df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]  #з усіх даних візьмемо лише ці колонкі

#3
short_period= 7
long_period = 30

df["Short_Moving_Average"] = df["Close"].rolling(short_period).mean()
df["Long_Moving_Average"] = df["Close"].rolling(long_period).mean()

df["Signal"] = 0 #нова колонка сигналів

for row in range( long_period, len(df)):
    short_mov_aver= df.loc[row, "Short_Moving_Average"]
    long_mov_aver= df.loc[row, "Long_Moving_Average"]

    if short_mov_aver > long_mov_aver:
        df.loc[row, "Signal"] = 1
    elif short_mov_aver < long_mov_aver:
        df.loc[row, "Signal"] = -1
    else:
        df.loc[row, "Signal"] = 0
print(df)

