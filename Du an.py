#step 1: Nhập tuổi của bạn
a = input("Bạn bao nhiêu tuổi? ")
a = int(a)
#step 2: Nhập tên của bạn
b = input("Tên của bạn là gì? ")

#step 3: In ra câu chào hỏi
if a < 18:
     print("Xin chào " + b + ", xét theo tuổi của bạn hiện tại là " + str(a) + ", thì có vẻ như bạn vẫn chưa đủ tuổi vị thành niên.")
elif a == 18:
     print("Xin chào " + b + ", xét theo tuổi của bạn hiện tại là " + str(a) + ", thì có vẻ như bạn vừa mới đủ tuổi vị thành niên.")
else:
     print("Xin chào " + b + ", xét theo tuổi của bạn hiện tại là " + str(a) + ", thì có vẻ như bạn đã đủ tuổi vị thành niên.")