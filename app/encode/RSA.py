import math
import random


def is_NguyenTo(number):  # Hàm kiếm tra số nguyên tố
    if number < 2:
        return False
    for i in range(2, number // 2 + 1):
        if number % i == 0:
            return False
    return True


def random_NguyenTo(so_min, so_max):  # Hàm tạo ra số nguyên tố ngẫu nhiên
    nguyen_to = random.randint(so_min, so_max)
    while not is_NguyenTo(nguyen_to):
        nguyen_to = random.randint(so_min, so_max)
    return nguyen_to


p = random_NguyenTo(1000, 5000)  # Gán p 1 số nguyên tố ngẫu nhiên
q = random_NguyenTo(1000, 5000)  # Gán q 1 số nguyên tố ngẫu nhiên

while p == q:  # Vòng lặp cập nhật lại giá trị q kh i trường hợp 2 số nguyên tố q và p giống nhau
    q = random_NguyenTo(1000, 5000)

N = p * q  # Tính N
n = (p - 1) * (q - 1)  # Tính n


def mod_nghichdao(e, phi):  # Hàm trả về d, với công thức e * d đồng dư 1 mod n
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d


e = random.randint(3, n - 1)  # Tìm e sao cho e là số nguyên tố cùng với n
while math.gcd(e, n) != 1:  # Vòng lặp kiểm tra ucln của e vs n là 1
    e = random.randint(3, n - 1)

d = mod_nghichdao(e, n)  # Tính d bằng công thức được xây dựng ở hàm trên


# print("Public Key: ", e)
# print("Private Key: ", d)
# print("n: ", n)
# print("p: ", p)
# print("q: ", q)


def Ma_hoa(message, public_key, n):
    text_mahoa = ""
    for char in message:
        m = ord(char)
        c = pow(m, public_key, n)
        text_mahoa += str(c) + " "
    return text_mahoa.strip()


def Giai_ma(text_mahoa, private_key, n):
    text_giaima = ""
    parts = text_mahoa.split()
    for part in parts:
        if part:
            c = int(part)
            m = pow(c, private_key, n)
            text_giaima += chr(m)
    return text_giaima

#
# message = input("Nhập message: ")
# test_message_mahoa = Ma_hoa(message, e, N)
# print("Mã hóa của đoạn message:", test_message_mahoa)
#
# test_message_giaima = Giai_ma(test_message_mahoa, d, N)
# print("Giải mã của đoạn message:", test_message_giaima)
#
# massage_giaima = input("Nhập văn bản đã mã hóa : ")
# test_message_giaima = Giai_ma(massage_giaima, d, N)
# print("Giải mã của đoạn message: ", test_message_giaima)
