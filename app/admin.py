from app import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import Movie, Seat, Show, ShowSchedule, Showtime, ShowRoom

admin = Admin(app=app, name='Administration',
              template_mode='bootstrap4')
admin.add_view(ModelView(Movie, db.session))
# admin.add_view(ModelView(Seatx, db.session))
# admin.add_view(ModelView(Show, db.session))
# admin.add_view(ModelView(ShowSchedule, db.session))
# admin.add_view(ModelView(Showtime, db.session))
# admin.add_view(ModelView(ShowRoom, db.session))
