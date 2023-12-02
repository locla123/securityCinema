import math
import random

from flask import render_template, request, redirect, url_for, jsonify, session
from pyotp import TOTP

from app import app, dao, login, recaptcha
from app.encode import blowfish
from flask_login import login_user, logout_user, login_required, current_user
import cloudinary.uploader

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import requests



def generate_otp():
    length = 6
    otp = ''
    for _ in range(length):
        otp += str(random.randint(0, 9))

    return otp


def verify_otp(otp, user_otp):
    print(otp)
    print(user_otp)
    if str(otp).__eq__(str(user_otp)):
        return True
    return False


def send_otp_email(email, otp):
    myemail = '2151050187khanh@ou.edu.vn'
    mypassword = '079203035064'

    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.starttls()
    connection.login(user=myemail, password=mypassword)

    message = MIMEMultipart()
    message['From'] = myemail
    message['To'] = email
    message['Subject'] = "Your OTP"  # Chủ đề của email
    body = f"Your OTP is: {otp}"
    message.attach(MIMEText(body, 'plain'))

    connection.send_message(message)
    connection.quit()


from jinja2 import Environment, FileSystemLoader
from app.encode.blowfish import decrypt
from app.encode.caesar import caesar_decrypt, K


@app.template_filter('decrypt_blowfish')
def blowfish_decrypt_user_full_name(user):
    env = Environment(loader=FileSystemLoader('templates'))
    env.filters['decrypt_blowfish'] = decrypt
    return decrypt(user.full_name, user.key)


@app.template_filter('caesar_decrypt')
def caesar_decrypt_seat_name(seat_name):
    env = Environment(loader=FileSystemLoader('templates'))
    env.filters['caesar_decrypt'] = caesar_decrypt
    return caesar_decrypt(seat_name, K)



totp = TOTP('base32secret3232')


def generate_otp():
    return totp.now()


def verify_otp(otp, user_otp):
    print(otp)
    print(user_otp)
    if str(otp).__eq__(str(user_otp)):
        return True
    return False


def send_otp_email(email, otp):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox802e7eca77604dde9c15297ab748e4fb.mailgun.org/messages",
        auth=("api", "db292522a7e22450feaff96e55e28d85-5d2b1caa-53959040"),
        data={
            "from": "Mailgun Sandbox <postmaster@sandbox802e7eca77604dde9c15297ab748e4fb.mailgun.org>",
            "to": email,
            "subject": "Your One-Time Password (OTP)",
            "text": f"Your OTP is: {otp}"
        }
    )


@app.route('/forget_pass', methods=['POST', 'GET'])
def forget_pass():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            user = dao.get_user_by_username(username)

            if user:
                user_mail = user.email
                ma_otp = totp.generate_otp(40)
                send_otp_email(user_mail, ma_otp)
                session['username'] = username
                session['ma_otp'] = ma_otp

                # Truyền thông tin người dùng (username) qua URL parameters đến route confirm_otp
                return redirect(url_for('confirm_otp'))

    return render_template('forget_pass.html')


@app.route('/confirm-otp', methods=['GET', 'POST'])
def confirm_otp():
    ma_otp = session['ma_otp']
    if request.method == 'POST':
        user_otp = request.form.get('otp')  # Lấy mã OTP nhập từ form
        print(user_otp)
        # Gọi hàm verify_otp để kiểm tra xem mã OTP nhập vào có trùng khớp với mã OTP đã tạo không
        is_valid = verify_otp(ma_otp, user_otp)

        if is_valid:
            # Nếu mã OTP xác nhận đúng, bạn có thể thực hiện hành động tiếp theo, ví dụ: đổi mật khẩu
            return redirect(url_for('change_password'))  # Chuyển hướng đến route đổi mật khẩu

        # Nếu mã OTP không trùng khớp, bạn có thể xử lý thông báo lỗi hoặc làm gì đó khác tùy ý
        error_message = 'Invalid OTP. Please try again.'
        return render_template('confirm_otp.html', error_message=error_message)

    # Nếu là method GET, hiển thị form xác nhận OTP
    return render_template('confirm_otp.html')


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    username = session.get('username')  # Lấy thông tin username từ session
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        if new_password.strip() == confirm_password.strip():
            # Thay đổi mật khẩu cho người dùng có username tương ứng
            dao.change_user_password(username, new_password)

            return redirect(url_for('user_login'))  # Chuyển hướng đến trang đăng nhập sau khi thay đổi mật khẩu

    return render_template('change_password.html', username=username)


@app.route('/')
def index():
    tag_id = request.args.get('tag_id')
    genre_id = request.args.get('genre_id')
    page = int(request.args.get('page', 1))

    movies = dao.load_movies(tag_id=tag_id, genre_id=genre_id, page=page)
    page_size = math.ceil(dao.count_movie() / app.config['PAGE_SIZE'])

    return render_template('index.html',
                           movies=movies,
                           page_size=page_size)


@app.route('/user-register', methods=['POST', 'GET'])
def user_register():
    err_msg = ''
    captcha_err_msg = ''
    if not recaptcha.verify():
        captcha_err_msg = 'Please make sure you are not a robot!'
        return render_template('register.html', captcha_err_msg=captcha_err_msg)
    else:
        try:
            if request.method.__eq__('POST'):
                username = request.form.get('username')
                email = request.form.get('email')
                if username and email:
                    if dao.check_user_existence(email=email, username=username):
                        password = request.form.get('password')
                        confirm = request.form.get('confirm')
                        if password.strip().__eq__(confirm.strip()):  # user valid
                            full_name = request.form.get('fullName')
                            avatar = request.files.get('avatar')

                            avatar_path = None
                            if avatar:
                                res = cloudinary.uploader.upload(avatar)
                                avatar_path = res['secure_url']

                            dao.add_user(full_name=full_name,
                                         email=email,
                                         username=username,
                                         password=password,
                                         avatar_path=avatar_path,
                                         key=blowfish.generate_key())
                            return redirect(url_for('index'))
                        else:
                            err_msg = 'Confirmed password does not match!'
                            render_template('register.html', err_msg=err_msg)
                    else:
                        err_msg = 'Username or email has already been used!'
                        render_template('register.html', err_msg=err_msg)
        except Exception as ex:
            err_msg = str(ex)
            render_template('register.html', err_msg=err_msg)

    return render_template('register.html', err_msg=err_msg)


@app.route('/user-login', methods=['POST', 'GET'])
def user_login():
    err_msg = ''
    captcha_err_msg = ''
    ref = request.args.get('next', 'index')

    if not recaptcha.verify():
        captcha_err_msg = 'Please make sure you are not a robot!'

        return render_template('login.html', captcha_err_msg=captcha_err_msg)
    else:
        try:
            if request.method.__eq__('POST'):
                username = request.form.get('username')
                password = request.form.get('password')
                user = dao.check_user_valid(username=username, password=password)
                if user:
                    login_user(user=user)
                    return redirect(url_for(ref))
                else:
                    err_msg = 'Username or password is incorrect!'
                    return render_template('login.html', err_msg=err_msg)
        except Exception as ex:
            err_msg = str(ex)
            return render_template('login.html', err_msg=err_msg)

    return render_template('login.html')


@app.route('/user-logout')
def user_logout():
    logout_user()
    return redirect(url_for('index'))


@app.context_processor
def common_response():
    return {
        "genres": dao.load_genres(),
        "tags": dao.load_tags()
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id=user_id)


@app.route('/ticket-booking')
def book_ticket():
    movie_id = request.args.get('movie_id')
    show_schedule_id = request.args.get('show_schedule_id')
    showroom_id = request.args.get('showroom_id')
    showtime_id = request.args.get('showtime_id')

    shows = dao.get_shows(movie_id=movie_id)
    movie = dao.get_movie_by_id(movie_id=movie_id)
    showtime = dao.get_showroom(show_schedule_id=show_schedule_id)
    seats = dao.get_seats(showroom_id=showroom_id)
    rate = dao.get_showtime_rate(showtime_id=showtime_id)

    return render_template('booking.html',
                           shows=shows,
                           movie=movie,
                           showtime=showtime,
                           seats=seats,
                           rate=rate)


@login_required
@app.route('/api/ticket-info', methods=['POST'])
def ticket_info():
    data = request.json
    try:
        movie_id = data.get('movieId')
        show_schedule_id = data.get('showScheduleId')
        showtime_id = data.get('showtimeId')
        showroom_id = data.get('showroomId')
        seat_id = data.get('seatId')
        total_price = data.get('price')

        dao.pay_ticket(movie_id=movie_id,
                       show_schedule_id=show_schedule_id,
                       showtime_id=showtime_id,
                       showroom_id=showroom_id,
                       seat_id=seat_id,
                       total_price=total_price)
    except Exception as ex:
        return jsonify({
            'code': 400,
            'exception': str(ex)
        })
    return jsonify({
        'code': 200
    })


@app.route('/movies/')
def detail():
    movie_id = request.args.get('movie_id')
    movie = dao.get_movie_by_id(movie_id=movie_id)

    return render_template('detail.html', movie=movie)

@login_required
@app.route('/details')
def details():
    tickets = dao.get_ticket_info()

    return render_template('ticket.html',
                           tickets=tickets)


if __name__ == '__main__':
    app.run(debug=True)
