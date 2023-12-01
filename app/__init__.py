from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_recaptcha import ReCaptcha
import cloudinary

app = Flask(__name__)
app.secret_key = 'ASGEY&%^BDFVARQ^SFS'
app.config["SQLALCHEMY_DATABASE_URI"] = str.format("mysql+pymysql://root:{}@localhost/cinemaapp?charset=utf8mb4",
                                                   "Omc6789#")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app=app)
login = LoginManager(app=app)

app.config['PAGE_SIZE'] = 8

# recaptcha configuration
recaptcha = ReCaptcha(app=app)
app.config.update(dict(
    RECAPTCHA_ENABLED=True,
    RECAPTCHA_SITE_KEY=f"6LesNiIpAAAAAGmyTRjW7rLqLL6LRXScwfz6KJhW",
    RECAPTCHA_SECRET_KEY=f"6LesNiIpAAAAAL7fmwsnDAituhvD6DEI--Y3mAWx"
))
# app.config.update(dict(
#     RECAPTCHA_ENABLED=True,
#     RECAPTCHA_SITE_KEY=f"6LcPdRwpAAAAABSQJZhIuu3AdlF0ZiOdYO9DfVT6",
#     RECAPTCHA_SECRET_KEY=f"6LcPdRwpAAAAAF87p-9zvsUSr9VYUphwRwrYjYc9"
# ))

# recaptcha = ReCaptcha()
recaptcha.init_app(app)

app.config['SECRET_KEY'] = 'cairocoders-ednalan'
cloud_dict = {
    "cloud_name": "dad8ejn0r",
    "api_key": "916986197549325",
    "api_secret": "8ZDd8GQafg9rc9_h5UrIBt0SZ4Q"
}

cloudinary.config(
    cloud_name=cloud_dict["cloud_name"],
    api_key=cloud_dict["api_key"],
    api_secret=cloud_dict["api_secret"]
)
