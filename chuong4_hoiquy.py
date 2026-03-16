import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


# ==============================
# 1. Đọc dữ liệu
# ==============================

data = pd.read_csv("hanoi-air-quality-clean.csv")

print("Các cột trong dữ liệu:")
print(data.columns)


# ==============================
# 2. Chọn biến
# ==============================

X = data[['pm10','co','no2','so2','o3']]
y = data['pm25']


# ==============================
# 3. Chia dữ liệu
# 80% đầu train
# 20% cuối test
# ==============================

split_index = int(len(data) * 0.8)

X_train = X[:split_index]
X_test = X[split_index:]

y_train = y[:split_index]
y_test = y[split_index:]

print("Train size:", len(X_train))
print("Test size:", len(X_test))


# ==============================
# 4. Thêm hệ số chặn B0
# ==============================

X_train = sm.add_constant(X_train)
X_test = sm.add_constant(X_test)


# ==============================
# 5. Huấn luyện mô hình hồi quy
# ==============================

model = sm.OLS(y_train, X_train).fit()

print("\nKẾT QUẢ HỒI QUY")
print(model.summary())


# ==============================
# 6. Dự đoán trên tập test
# ==============================

y_pred = model.predict(X_test)


# ==============================
# 7. Tính các chỉ số đánh giá
# ==============================

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\nĐÁNH GIÁ MÔ HÌNH")

print("R2 =", r2)
print("MAE =", mae)
print("RMSE =", rmse)


# ==============================
# 8. Phương trình hồi quy
# ==============================

coef = model.params

print("\nPHƯƠNG TRÌNH HỒI QUY:")

print(f"""
PM2.5 =
{coef['const']} +
{coef['pm10']} * PM10 +
{coef['co']} * CO +
{coef['no2']} * NO2 +
{coef['so2']} * SO2 +
{coef['o3']} * O3
""")


# ==============================
# 9. Tạo bảng kết quả
# ==============================

metrics = pd.DataFrame({
    "Metric": ["R2", "MAE", "RMSE"],
    "Value": [r2, mae, rmse]
})

coefficients = pd.DataFrame({
    "Variable": model.params.index,
    "Coefficient": model.params.values
})

comparison = pd.DataFrame({
    "Actual_PM25": y_test.values,
    "Predicted_PM25": y_pred.values
})


# ==============================
# 10. Xuất Excel
# ==============================

with pd.ExcelWriter("ket_qua_hoi_quy.xlsx") as writer:

    metrics.to_excel(writer, sheet_name="Model_Metrics", index=False)

    coefficients.to_excel(writer, sheet_name="Regression_Coefficients", index=False)

    comparison.to_excel(writer, sheet_name="Prediction_Comparison", index=False)

print("\nĐã xuất file: ket_qua_hoi_quy.xlsx")


# ==============================
# 11. Vẽ biểu đồ dự đoán
# ==============================

plt.figure(figsize=(12,6))

plt.plot(y_test.values, label="PM2.5 Thực tế", linewidth=2)

plt.plot(y_pred.values, label="PM2.5 Dự đoán", linestyle="--")

plt.title("So sánh PM2.5 thực tế và dự đoán (20% dữ liệu cuối)")

plt.xlabel("20% dữ liệu test (theo thời gian)")
plt.ylabel("Nồng độ PM2.5")

plt.legend()

plt.grid(True)

# lưu biểu đồ
plt.savefig("bieu_do_du_doan_pm25.png", dpi=300)

plt.show()

print("Đã lưu biểu đồ: bieu_do_du_doan_pm25.png")
print(len(data))