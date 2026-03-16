import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# đọc dữ liệu
df = pd.read_csv("hanoi-air-quality-clean.csv")

# xử lý dữ liệu
df.columns = df.columns.str.strip()
df['date'] = pd.to_datetime(df['date'])

# lọc dữ liệu 2020-2024
df = df[(df['date'].dt.year >= 2020) & (df['date'].dt.year <= 2024)]

cols = ['pm25','pm10','o3','no2','so2','co']
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

# bỏ các dòng thiếu dữ liệu
df = df.dropna()

# ======================
# XÁC ĐỊNH BIẾN
# ======================

X = df[['pm10','o3','no2','so2','co']]
y = df['pm25']

# chia dữ liệu train / test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ======================
# XÂY DỰNG MÔ HÌNH
# ======================

model = LinearRegression()

model.fit(X_train, y_train)

# dự đoán
y_pred = model.predict(X_test)

# ======================
# ĐÁNH GIÁ MÔ HÌNH
# ======================

mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nKẾT QUẢ MÔ HÌNH HỒI QUY TUYẾN TÍNH\n")

print("MSE:", mse)
print("RMSE:", rmse)
print("MAE:", mae)
print("R2:", r2)

# hệ số hồi quy
coef_table = pd.DataFrame({
    "Variable": X.columns,
    "Coefficient": model.coef_
})

print("\nHỆ SỐ HỒI QUY:")
print(coef_table)

print("\nIntercept:", model.intercept_)
import matplotlib.pyplot as plt

# ======================
# BIỂU ĐỒ HỆ SỐ HỒI QUY
# ======================

plt.figure(figsize=(8,5))

plt.bar(coef_table["Variable"], coef_table["Coefficient"])

plt.title("Ảnh hưởng của các chất ô nhiễm đến PM2.5")
plt.xlabel("Biến")
plt.ylabel("Hệ số hồi quy")

plt.axhline(0)   # đường mức 0

plt.tight_layout()

plt.savefig("he_so_hoi_quy.png")

plt.show()