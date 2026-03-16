import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# 1. Đọc và sắp xếp dữ liệu
df = pd.read_csv("hanoi-air-quality-clean.csv")
df.columns = df.columns.str.strip().str.lower()
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)

# 2. Tạo biến trễ (Lag-1)
df['pm25_lag1'] = df['pm25'].shift(1)
df = df.dropna(subset=['pm25_lag1', 'pm10', 'no2', 'so2', 'co'])

# 3. Chia 80% đầu để TRAIN, 290 dòng kế tiếp để TEST
train_size = int(len(df) * 0.8)
df_train = df.iloc[:train_size]
df_test = df.iloc[train_size : train_size + 290].copy()

# Reset index của tập test về 0-289 để vẽ biểu đồ theo yêu cầu
df_test = df_test.reset_index(drop=True)

features = ['pm10', 'no2', 'so2', 'co', 'pm25_lag1']
X_train, y_train = df_train[features], df_train['pm25']
X_test, y_test = df_test[features], df_test['pm25']

# 4. Huấn luyện mô hình
X_train_const = sm.add_constant(X_train)
model = sm.OLS(y_train, X_train_const).fit()

# 5. Dự báo
X_test_const = sm.add_constant(X_test)
pred = model.predict(X_test_const)

# 6. VẼ BIỂU ĐỒ (ĐÃ XÓA R-SQUARED KHỎI TIÊU ĐỀ)
plt.figure(figsize=(15, 6))

# Vẽ đường giá trị thật
plt.plot(df_test.index, y_test, label="Giá trị thật (Actual)", color='#1f77b4', linewidth=1.5)

# Vẽ đường giá trị dự báo
plt.plot(df_test.index, pred, label="Giá trị dự báo (Predicted)", color='#d62728', linestyle='--', linewidth=1.5)

# Tính khoảng tin cậy để fill màu (Dựa trên sai số tập Train)
std_error = np.std(y_train - model.predict(X_train_const))
plt.fill_between(df_test.index, pred - std_error, pred + std_error, color='gray', alpha=0.15, label="Khoảng tin cậy")

# --- DÒNG LỆNH ĐÃ SỬA ---
# Chỉ giữ lại tiêu đề chữ, xóa phần hiển thị R2
plt.title("So sánh PM2.5 Thực tế và Dự báo (290 mẫu thử nghiệm)", fontsize=14)
# ------------------------

plt.xlabel("Số thứ tự mẫu (0 - 289)", fontsize=12)
plt.ylabel("Nồng độ PM2.5 (µg/m³)", fontsize=12)
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()

# Lưu hình ra file mới
plt.savefig("bieu_do_pm25_khong_r2.png", dpi=300)
plt.show()

# 7. Vẫn in các chỉ số ra màn hình để bạn biết độ chính xác
print(f"Hệ số xác định R2: {r2_score(y_test, pred):.4f}")
print(f"MAE: {mean_absolute_error(y_test, pred):.4f}")