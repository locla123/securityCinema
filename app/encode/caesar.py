# k: bước dịch
# plain_text: văn bản cần mã hóa
# encrypted_text: khởi tạo chuỗi trống lưu trữ văn bản sau khi mã hóa


def caesar_encrypt(plain_text, k):
    encrypted_text = ""
    for char in plain_text:
        if char.isalpha():
            if char.islower():
                # mã hóa kí tự thường
                encrypted_text += chr((ord(char) - ord('a') + k) % 26 + ord('a'))
            else:
                # mã hóa kí tự in hoa
                encrypted_text += chr((ord(char) - ord('A') + k) % 26 + ord('A'))
        else:
            # Giữ nguyên ký tự không phải chữ cái
            encrypted_text += char
    return encrypted_text


def caesar_decrypt(encrypted_text, k):
    decrypted_text = ""
    for char in encrypted_text:
        if char.isalpha():
            if char.islower():
                decrypted_text += chr((ord(char) - k - ord('a')) % 26 + ord('a'))
            else:
                decrypted_text += chr((ord(char) - k - ord('A')) % 26 + ord('A'))
        else:
            decrypted_text += char
    return decrypted_text


K = 25

# temp = caesar_encrypt('S01', K)
# dec_temp = caesar_decrypt(temp, K)
# print(temp)
# print(dec_temp)

# Mã hóa văn bản
# plain_text = "HEDIEUHANH"
# print('Văn bản cần mã hóa:', plain_text)
# k = 25
#
# encrypted_text = caesar_encrypt(plain_text, k)
# print(f"Sau khi mã hóa: {encrypted_text}")
#
# # Giải mã văn bản
# encrypted_text = "RGLFMASLEBSLE"
# print('Văn bản cần giải mã: ', encrypted_text)
# k = 24
#
# decrypted_text = caesar_decrypt(encrypted_text, k)
# print(f"Sau khi giải mã: {decrypted_text}")
