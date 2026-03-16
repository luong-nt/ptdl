import pandas as pd

# đọc dữ liệu
df = pd.read_csv("hanoi-air-quality.csv")

# xóa khoảng trắng trong tên cột
df.columns = df.columns.str.strip()

# chuyển date
df['date'] = pd.to_datetime(df['date'])

# lọc năm 2020-2024
df = df[(df['date'].dt.year >= 2020) & (df['date'].dt.year <= 2024)]

# các cột cần xử lý
cols = ['pm25','pm10','o3','no2','so2','co']

# chuyển sang số
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

# nội suy trung bình 2 giá trị gần nhất
df[cols] = df[cols].interpolate(method='linear')

# xử lý thiếu đầu cuối
df[cols] = df[cols].bfill().ffill()

# lưu file mới
df.to_csv("hanoi-air-quality-clean.csv", index=False)

print("Đã xử lý xong dữ liệu!")