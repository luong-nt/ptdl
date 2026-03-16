import pandas as pd

# đọc dữ liệu
df = pd.read_csv("hanoi-air-quality-clean.csv")

# bỏ khoảng trắng trong tên cột
df.columns = df.columns.str.strip()

# chuyển cột date sang dạng thời gian
df['date'] = pd.to_datetime(df['date'])

# lọc dữ liệu từ 2020-2024
df = df[(df['date'].dt.year >= 2020) & (df['date'].dt.year <= 2024)]

# các biến cần phân tích
cols = ['pm25','pm10','o3','no2','so2','co']

# chuyển sang dạng số
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

# ======================
# THỐNG KÊ MÔ TẢ
# ======================

stats = df[cols].describe()

# số giá trị thiếu
missing = df[cols].isnull().sum()
stats.loc['missing_values'] = missing

print("\nBẢNG THỐNG KÊ MÔ TẢ:")
print(stats)

# ======================
# PHÁT HIỆN NGOẠI LAI
# ======================

outlier_count = {}

for col in cols:

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lower) | (df[col] > upper)]

    outlier_count[col] = len(outliers)

outlier_df = pd.DataFrame(outlier_count, index=['outliers'])

print("\nSỐ LƯỢNG NGOẠI LAI:")
print(outlier_df)

# ======================
# XUẤT FILE EXCEL
# ======================

with pd.ExcelWriter("bang_thong_ke_mo_ta.xlsx") as writer:
    stats.to_excel(writer, sheet_name="Thong_ke_mo_ta")
    outlier_df.to_excel(writer, sheet_name="Outliers")

print("\nĐã tạo file: bang_thong_ke_mo_ta.xlsx")
import matplotlib.pyplot as plt
import seaborn as sns

# ======================
# VẼ BIỂU ĐỒ NGOẠI LAI
# ======================

plt.figure(figsize=(10,6))

sns.boxplot(data=df[cols])

plt.title("Phát hiện giá trị ngoại lai của các biến ô nhiễm không khí")
plt.xlabel("Các biến")
plt.ylabel("Giá trị")

plt.tight_layout()

# lưu hình
plt.savefig("boxplot_outliers.png")

plt.show()
import matplotlib.pyplot as plt
import seaborn as sns

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
# HISTOGRAM THEO MÙA
# ======================

plt.figure(figsize=(10,6))

sns.histplot(
    data=df,
    x="pm25",
    hue="season",
    bins=30,
    kde=True,
    element="step"
)

plt.title("Histogram PM2.5 theo mùa (2020–2024)")
plt.xlabel("PM2.5")
plt.ylabel("Tần suất")

plt.tight_layout()

plt.savefig("histogram_pm25_season.png")

plt.show()
print(df.groupby("season")["pm25"].mean())
import matplotlib.pyplot as plt
import seaborn as sns

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
# HISTOGRAM PM2.5 THEO NĂM
# ======================

plt.figure(figsize=(10,6))

sns.histplot(
    data=df,
    x="pm25",
    hue="year",
    bins=30,
    kde=True,
    element="step",
    palette="tab10"
)

plt.title("Histogram PM2.5 theo năm (2020–2024)")
plt.xlabel("PM2.5")
plt.ylabel("Tần suất")

plt.tight_layout()

plt.savefig("histogram_pm25_year.png")

plt.show()


# ======================
# HISTOGRAM PM2.5 THEO MÙA
# ======================

plt.figure(figsize=(10,6))

sns.histplot(
    data=df,
    x="pm25",
    hue="season",
    bins=30,
    kde=True,
    element="step",
    palette={
        "Winter": "#1f77b4",   # xanh
        "Summer": "#d62728",   # đỏ
        "Spring": "#2ca02c",   # xanh lá
        "Autumn": "#ff7f0e"    # cam
    }
)

plt.title("Histogram PM2.5 theo mùa (2020–2024)")
plt.xlabel("PM2.5")
plt.ylabel("Tần suất")

plt.tight_layout()

plt.savefig("histogram_pm25_season.png")

plt.show()


# ======================
# HISTOGRAM PM10 THEO NĂM
# ======================

plt.figure(figsize=(10,6))

sns.histplot(
    data=df,
    x="pm10",
    hue="year",
    bins=30,
    kde=True,
    element="step",
    palette="tab10"
)

plt.title("Histogram PM10 theo năm (2020–2024)")
plt.xlabel("PM10")
plt.ylabel("Tần suất")

plt.tight_layout()

plt.savefig("histogram_pm10_year.png")

plt.show()


# ======================
# HISTOGRAM PM10 THEO MÙA
# ======================

plt.figure(figsize=(10,6))

sns.histplot(
    data=df,
    x="pm10",
    hue="season",
    bins=30,
    kde=True,
    element="step",
    palette={
        "Winter": "#1f77b4",
        "Summer": "#d62728",
        "Spring": "#2ca02c",
        "Autumn": "#ff7f0e"
    }
)

plt.title("Histogram PM10 theo mùa (2020–2024)")
plt.xlabel("PM10")
plt.ylabel("Tần suất")

plt.tight_layout()

plt.savefig("histogram_pm10_season.png")

plt.show()