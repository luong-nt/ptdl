import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import statsmodels.api as sm

# 1. Đọc dữ liệu từ file sạch
df = pd.read_csv('hanoi-air-quality-clean.csv')

# 2. Chọn các biến độc lập và biến phụ thuộc (theo bài của bạn)
X = df[['pm10', 'no2', 'so2', 'co']]
y = df['pm25']

# 3. Chia dữ liệu thành tập Huấn luyện (80%) và Kiểm tra (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Xây dựng mô hình hồi quy OLS (để lấy được p-value và các hệ số)
X_train_const = sm.add_constant(X_train) # Thêm hệ số chặn (B0)
X_test_const = sm.add_constant(X_test)
model = sm.OLS(y_train, X_train_const).fit()

# 5. Trích xuất bảng Hệ số hồi quy (Bảng 5.1 trong bài)
summary_table = model.summary2().tables[1]
summary_table.reset_index(inplace=True)
summary_table.columns = ['Biến', 'Hệ số B', 'Sai số chuẩn', 't-value', 'p-value', 'Dưới (95%)', 'Trên (95%)']

# 6. Dự báo trên tập Test và tính toán chỉ số đánh giá (R2, MAE, RMSE)
y_pred = model.predict(X_test_const)
metrics_data = {
    'Chỉ số': ['R-squared (R2)', 'MAE', 'RMSE'],
    'Giá trị': [
        r2_score(y_test, y_pred),
        mean_absolute_error(y_test, y_pred),
        np.sqrt(mean_squared_error(y_test, y_pred))
    ]
}
metrics_df = pd.DataFrame(metrics_data)

# 7. Xuất kết quả ra file Excel
file_name = 'Bao_cao_Hoi_quy_PM25.xlsx'
with pd.ExcelWriter(file_name) as writer:
    summary_table.to_excel(writer, sheet_name='He_so_hoi_quy', index=False)
    metrics_df.to_excel(writer, sheet_name='Danh_gia_mo_hinh', index=False)

print(f"Chúc mừng! Bạn đã xuất file thành công: {file_name}")