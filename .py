# Bài 2:
import math

# Hằng số pi theo đề bài
pi = 3.14

# Nhập chiều rộng a và chiều dài b
a = float(input("Nhập chiều rộng a: "))
b = float(input("Nhập chiều dài b: "))

# Diện tích hình chữ nhật
dt_hcn = a * b

# Bán kính hình tròn bằng một nửa chiều rộng a
r = a / 2

# Diện tích hình tròn
dt_tron = pi * (r ** 2)

# Diện tích trồng cây
dt_cay = dt_hcn - dt_tron

# In kết quả với 2 chữ số thập phân
print(f"Diện tích phần trồng cây còn lại là: {dt_cay:.2f}")