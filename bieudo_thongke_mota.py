import pandas as pd
import matplotlib.pyplot as plt

# đọc dữ liệu
df = pd.read_csv("hanoi-air-quality-clean.csv")

df.columns = df.columns.str.strip().str.lower()

cols = ["pm25","pm10","o3","no2","so2","co"]

# tính trung bình
mean_values = df[cols].mean()

# vẽ biểu đồ
plt.figure(figsize=(8,5))

plt.bar(mean_values.index, mean_values.values)

plt.title("Giá trị trung bình các chất ô nhiễm không khí")

plt.xlabel("Chất ô nhiễm")

plt.ylabel("Nồng độ trung bình")

plt.tight_layout()

plt.savefig("bieudo_trungbinh_o_nhiem.png")

plt.show()
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("hanoi-air-quality-clean.csv")

df.columns = df.columns.str.strip().str.lower()

cols = ["pm25","pm10","o3","no2","so2","co"]

plt.figure(figsize=(10,6))

plt.boxplot([df[col].dropna() for col in cols],
            labels=[c.upper() for c in cols])

plt.title("Phân bố nồng độ các chất ô nhiễm")

plt.xlabel("Chỉ số")

plt.ylabel("Nồng độ")

plt.tight_layout()

plt.savefig("boxplot_o_nhiem.png")

plt.show()