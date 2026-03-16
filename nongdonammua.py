import pandas as pd
import matplotlib.pyplot as plt

# ======================
# ĐỌC DỮ LIỆU
# ======================

df = pd.read_csv("hanoi-air-quality.csv")

# bỏ khoảng trắng trong tên cột
df.columns = df.columns.str.strip()

# chuyển date sang dạng thời gian
df['date'] = pd.to_datetime(df['date'])

# lọc dữ liệu 2020-2024
df = df[(df['date'].dt.year >= 2020) & (df['date'].dt.year <= 2024)]

# chuyển dữ liệu sang dạng số
cols = ['pm25','pm10','o3','no2','so2','co']
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

# ======================
# TẠO CỘT NĂM
# ======================

df["year"] = df["date"].dt.year

# ======================
# TẠO CỘT MÙA
# ======================

def get_season(month):
    if month in [3,4,5]:
        return "Spring"
    elif month in [6,7,8]:
        return "Summer"
    elif month in [9,10,11]:
        return "Autumn"
    else:
        return "Winter"

df["season"] = df["date"].dt.month.apply(get_season)

# ======================
# PM2.5 THEO NĂM
# ======================

pm25_year = df.groupby("year")["pm25"].mean()

pm25_year.plot(kind="bar")

plt.title("Nồng độ PM2.5 trung bình theo năm (2020–2024)")
plt.xlabel("Năm")
plt.ylabel("PM2.5")

plt.tight_layout()
plt.savefig("pm25_theo_nam.png")

plt.show()

# ======================
# PM2.5 THEO MÙA
# ======================

pm25_season = df.groupby("season")["pm25"].mean()

pm25_season.plot(kind="bar")

plt.title("Nồng độ PM2.5 trung bình theo mùa")
plt.xlabel("Mùa")
plt.ylabel("PM2.5")

plt.tight_layout()
plt.savefig("pm25_theo_mua.png")

plt.show()

# ======================
# PM10 THEO NĂM
# ======================

pm10_year = df.groupby("year")["pm10"].mean()

pm10_year.plot(kind="bar")

plt.title("Nồng độ PM10 trung bình theo năm (2020–2024)")
plt.xlabel("Năm")
plt.ylabel("PM10")

plt.tight_layout()
plt.savefig("pm10_theo_nam.png")

plt.show()

# ======================
# PM10 THEO MÙA
# ======================

pm10_season = df.groupby("season")["pm10"].mean()

pm10_season.plot(kind="bar")

plt.title("Nồng độ PM10 trung bình theo mùa")
plt.xlabel("Mùa")
plt.ylabel("PM10")

plt.tight_layout()
plt.savefig("pm10_theo_mua.png")

plt.show()

print("Đã tạo xong các biểu đồ nồng độ!")