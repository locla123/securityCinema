**CÁCH RUN PROJECT SAU KHI CLONE VỀ:**
#B1: tạo môi trường ảo (venv)
B2: Mở terminal lên (lúc này phải trỏ vể venv), và install các thư viện trong file requirements.txt (pip install -r requirements.txt)
B3: install flask_recaptcha (pip install flask_recaptcha)
B4: Kết nối với database qua MySQL Workbench bằng cách cấu hình lại tên database và password ở file __init__.py
    - Ở dòng 9-10: 
    app.config["SQLALCHEMY_DATABASE_URI"] = str.format("mysql+pymysql://root:{}@localhost/tenCSDL?charset=utf8mb4",
                                                   "passwordCSDL")
    - Thay tenCSDL là tên của CSDL đã tạo trước ở MySQL Workbench và mật khẩu của MySQL.
B5: Chạy file models.py để tạo các tables ở database (lệnh db.create_all())
    Chạy từng khối lệnh để thêm dữ liệu vào các tables
B6: fix bug markup: Vào venv -> lib -> flask_recaptcha.py, ở dòng 14 thay jinja2 bằng markupsafe
B7: Lưu lại và run file index.py -> truy cập localhost xem đã chạy được chưa
