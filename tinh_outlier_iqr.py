import pandas as pd

# đọc đúng file của bạn
df = pd.read_csv("hanoi-air-quality-clean.csv")

# chuẩn hóa tên cột
df.columns = df.columns.str.strip().str.lower()

# các chỉ số cần tính
cols = ["pm25","pm10","o3","no2","so2","co"]

result = []

for col in cols:

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    IQR = Q3 - Q1

    upper = Q3 + 1.5 * IQR

    # đếm ngoại lai
    outliers = df[df[col] > upper]

    count = outliers.shape[0]

    max_value = df[col].max()

    result.append([col.upper(), upper, count, max_value])

table = pd.DataFrame(result, columns=[
    "Chỉ số",
    "Ngưỡng rào trên (IQR)",
    "Số lượng giá trị ngoại lai",
    "Giá trị cao nhất ghi nhận"
])

print(table)

# xuất ra excel
table.to_excel("bang_ngoai_lai_IQR.xlsx", index=False)

print("Đã xuất file bang_ngoai_lai_IQR.xlsx")