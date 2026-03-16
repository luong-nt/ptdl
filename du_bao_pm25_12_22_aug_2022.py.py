import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# ======================
# ĐỌC DỮ LIỆU
# ======================

df = pd.read_csv("hanoi-air-quality-clean.csv")

df.columns = df.columns.str.strip().str.lower()

df["date"] = pd.to_datetime(df["date"])

cols = ["pm25","pm10","no2","so2","co"]

df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")

df = df.dropna(subset=cols)

df = df.sort_values("date")

# ======================
# TẠO MÔ HÌNH HỒI QUY
# ======================

X = df[["pm10","no2","so2","co"]]
y = df["pm25"]

model = LinearRegression()

model.fit(X,y)

# ======================
# CHỌN KHOẢNG DỰ BÁO
# ======================

start_date = "2022-08-12"
end_date = "2022-08-22"

df_test = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

X_test = df_test[["pm10","no2","so2","co"]]

# dự báo
pred = model.predict(X_test)

# ======================
# TÍNH SAI SỐ CHUNG
# ======================

error = y - model.predict(X)

std_error = np.std(error)

upper = pred + std_error
lower = pred - std_error

# ======================
# VẼ BIỂU ĐỒ
# ======================

plt.figure(figsize=(10,5))

plt.plot(df_test["date"],
         df_test["pm25"],
         label="Actual PM2.5",
         linewidth=2)

plt.plot(df_test["date"],
         pred,
         label="Predicted PM2.5",
         linewidth=2)

plt.fill_between(df_test["date"],
                 lower,
                 upper,
                 alpha=0.2,
                 label="Confidence band")

plt.title("So sánh PM2.5 thực tế và dự báo (12/08/2022 – 22/08/2022)")

plt.xlabel("Date")

plt.ylabel("PM2.5")

plt.xticks(rotation=45)

plt.legend()

plt.tight_layout()

plt.savefig("du_bao_pm25_12_22_aug_2022.png")

plt.show()

# ======================
# IN BẢNG SO SÁNH
# ======================

compare = pd.DataFrame({
    "Date": df_test["date"],
    "Actual_PM25": df_test["pm25"],
    "Predicted_PM25": pred
})

print(compare)

compare.to_excel("so_sanh_du_bao_pm25.xlsx", index=False)

print("Đã xuất file so_sanh_du_bao_pm25.xlsx")