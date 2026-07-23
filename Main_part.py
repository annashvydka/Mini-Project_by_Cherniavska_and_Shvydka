# Отримайте історичні ринкові дані для вибраного фінансового інструменту.
# Ці дані повинні включати основні показники, такі як ціна відкриття, ціна закриття, максимум, мінімум і обсяг торгів.

import yfinance as yf
import pandas as pd

#2
data = yf.download("SBUX", start="2025-01-01", end="2026-01-01")

df = data.reset_index()  #бо дата була рядками, а тепер стала окремою колонкою і замість дат 123
df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]  #з усіх даних візьмемо лише ці колонкі

#print(df.columns)
df.columns = df.columns.get_level_values(0)  #прибирає з назв колнок 'SBUX'

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
        df.loc[row, "Signal"] = 1 #купівля
    elif short_mov_aver < long_mov_aver:
        df.loc[row, "Signal"] = -1  #продаж
    else:
        df.loc[row, "Signal"] = 0  #утримання


#4.1
df["Price_Change"] = 0.0

for row in range(1, len(df)):
    df.loc[row, "Price_Change"] = df.loc[row, "Close"] - df.loc[row - 1, "Close"]


df["Profit"] = 0.0
for row in range(1, len(df)):
    if df.loc[row, "Signal"] == 1:
        df.loc[row, "Profit"] = df.loc[row, "Price_Change"]
    elif df.loc[row, "Signal"] == -1:
        df.loc[row, "Profit"] = -df.loc[row, "Price_Change"] #якщо ціна впала ("Price_Change"<0) то ми наче заробили невтрачену суму
    else:
        df.loc[row, "Profit"] = 0

print(df)

total_profit = df["Profit"].sum()
print(total_profit)