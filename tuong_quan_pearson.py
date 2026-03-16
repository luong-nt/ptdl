import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ======================
# ĐỌC DỮ LIỆU
# ======================

df = pd.read_csv("hanoi-air-quality-clean.csv")

# bỏ khoảng trắng trong tên cột
df.columns = df.columns.str.strip()

# chuyển date sang dạng thời gian
df['date'] = pd.to_datetime(df['date'])

# lọc dữ liệu 2020-2024
df = df[(df['date'].dt.year >= 2020) & (df['date'].dt.year <= 2024)]

# các biến phân tích
cols = ['pm25','pm10','o3','no2','so2','co']

# chuyển sang dạng số
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

# bỏ dòng thiếu dữ liệu
df = df.dropna()

# ======================
# TÍNH MA TRẬN TƯƠNG QUAN
# ======================

corr_matrix = df[cols].corr(method='pearson')

print("\nMA TRẬN HỆ SỐ TƯƠNG QUAN PEARSON:\n")
print(corr_matrix)

# ======================
# TƯƠNG QUAN VỚI PM2.5
# ======================

pm25_corr = corr_matrix['pm25'].sort_values(ascending=False)

print("\nTƯƠNG QUAN VỚI PM2.5:\n")
print(pm25_corr)

# ======================
# PHÂN LOẠI MỨC ĐỘ TƯƠNG QUAN
# ======================

def corr_level(r):

    r = abs(r)

    if r >= 0.7:
        return "Mạnh"
    elif r >= 0.4:
        return "Trung bình"
    elif r >= 0.2:
        return "Yếu"
    else:
        return "Rất yếu"

corr_detail = []

for var in cols:

    if var != "pm25":

        r = corr_matrix.loc["pm25", var]

        corr_detail.append({
            "Variable": var,
            "Pearson_r": r,
            "Muc_do_tuong_quan": corr_level(r)
        })

corr_detail_df = pd.DataFrame(corr_detail)

print("\nPHÂN TÍCH TƯƠNG QUAN VỚI PM2.5:\n")
print(corr_detail_df)

# ======================
# VẼ HEATMAP
# ======================

plt.figure(figsize=(8,6))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Ma trận hệ số tương quan Pearson giữa các biến")

plt.tight_layout()

plt.savefig("heatmap_tuong_quan.png")

plt.show()

# ======================
# LƯU KẾT QUẢ EXCEL
# ======================

with pd.ExcelWriter("phan_tich_tuong_quan.xlsx") as writer:

    corr_matrix.to_excel(writer, sheet_name="Ma_tran_tuong_quan")

    corr_detail_df.to_excel(writer, sheet_name="Tuong_quan_PM25")

print("\nĐã tạo file: phan_tich_tuong_quan.xlsx")