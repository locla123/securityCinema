from sqlalchemy.orm import relationship

from app import db, app
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, LargeBinary, DateTime, Date, Boolean, Time
from enum import Enum as UserEnum
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date, time

Base = declarative_base()


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    note = Column(String(100))
    movie_tags = relationship('MovieTag', backref='tag', lazy=True)

    def __str__(self):
        return self.name


class Genre(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(1000))
    movie_genres = relationship('MovieGenre', backref='genre', lazy=True)

    def __str__(self):
        return self.name


class Movie(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    price = Column(Float, default=0)
    image = Column(String(500))
    movie_tags = relationship('MovieTag', backref='movie', lazy=True)
    movie_genres = relationship('MovieGenre', backref='movie', lazy=True)
    movie_show_schedules = relationship('ShowSchedule', backref='movie', lazy=True)
    tickets = relationship('Ticket', backref='movie', lazy=True)

    def __str__(self):
        return self.name


class MovieTag(BaseModel):
    movie_id = Column(Integer, ForeignKey(Movie.id), nullable=False)
    tag_id = Column(Integer, ForeignKey(Tag.id), nullable=False)


class MovieGenre(BaseModel):
    movie_id = Column(Integer, ForeignKey(Movie.id), nullable=False)
    genre_id = Column(Integer, ForeignKey(Genre.id), nullable=False)


class User(BaseModel, Base, UserMixin):
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    avatar = Column(String(500),
                    default='https://icons.veryicon.com/png/o/miscellaneous/two-color-icon-library/user-286.png')
    username = Column(String(100), nullable=False, unique=True)
    # password = Column(String(100), nullable=False)
    password = Column(LargeBinary, nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    key = Column(LargeBinary)
    joined_date = Column(DateTime, default=datetime.now())
    tickets = relationship('Ticket', backref='user', lazy=True)


class ShowSchedule(BaseModel):
    time = Column(Date, nullable=False)
    movie_id = Column(Integer, ForeignKey(Movie.id), nullable=False)
    shows = relationship('Show', backref='show_schedule', lazy=True)
    tickets = relationship('Ticket', backref='show_schedule', lazy=True)


class ShowRoom(BaseModel):
    name = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False)
    description = Column(String(500))
    shows = relationship('Show', backref='show_room', lazy=True)
    seats = relationship('Seat', backref='showroom', lazy=True)
    tickets = relationship('Ticket', backref='showroom', lazy=True)

    def __str__(self):
        return self.name


class Showtime(BaseModel):
    name = Column(String(50), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    rate = Column(Float, nullable=False)
    shows = relationship('Show', backref='showtime', lazy=True)
    tickets = relationship('Ticket', backref='showtime', lazy=True)

    def __str__(self):
        return self.name


class Show(BaseModel):
    show_schedule_id = Column(Integer, ForeignKey(ShowSchedule.id), nullable=False)
    showtime_id = Column(Integer, ForeignKey(Showtime.id), nullable=False)
    show_room_id = Column(Integer, ForeignKey(ShowRoom.id), nullable=False)


class Seat(BaseModel):
    name = Column(String(25), nullable=False)
    is_available = Column(Boolean, default=True)
    show_room_id = Column(Integer, ForeignKey(ShowRoom.id), nullable=False)
    tickets = relationship('Ticket', backref='seat', lazy=True)


class Ticket(BaseModel):
    movie_id = Column(Integer, ForeignKey(Movie.id), nullable=False)
    show_schedule_id = Column(Integer, ForeignKey(ShowSchedule.id), nullable=False)
    showtime_id = Column(Integer, ForeignKey(Showtime.id), nullable=False)
    showroom_id = Column(Integer, ForeignKey(ShowRoom.id), nullable=False)
    seat_id = Column(Integer, ForeignKey(Seat.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    total_price = Column(Float, nullable=False)
    booked_date = Column(DateTime, default=datetime.now())


if __name__ == "__main__":
    with app.app_context():
        # db.create_all()

        # t3 = Tag(name='Coming')
        # t2 = Tag(name='Promotion')
        # t1 = Tag(name='Showing')
        # db.session.add_all([t1, t2, t3])
        # db.session.commit()

        # g1 = Genre(name='Action')
        # g2 = Genre(name='Adventure')
        # g3 = Genre(name='Cartoon')
        # g4 = Genre(name='Comedy')
        # g5 = Genre(name='Drama')
        # g6 = Genre(name='Music')
        # g7 = Genre(name='Romantic')
        # db.session.add_all([g1, g2, g3, g4, g5, g6, g7])
        # db.session.commit()

        # m1 = Movie(name='IT’S OKAY TO NOT BE OKAY', price=120000, image='images/p1.png')
        # m2 = Movie(name='SWEET HOME', price=99000, image='images/p2.png')
        # m3 = Movie(name='VAGABOND', price=135000, image='images/p3.png')
        # m4 = Movie(name='CRASH LANDING ON YOU', price=129000, image='images/p4.png')
        # m5 = Movie(name='ROOKIE HISTORIAN GOO HAE RYUNG', price=150000, image='images/p5.png')
        # m6 = Movie(name='WHEN THE CAMELLIA BLOOMS', price=250000, image='images/p6.png')
        # m7 = Movie(name='CHIEF OF STAFF', price=199000, image='images/p7.png')
        # m8 = Movie(name='KINGDOM', price=175000, image='images/p8.png')
        # m9 = Movie(name='ROMANCE IS A BONUS BOOK', price=215000, image='images/p9.png')
        # m10 = Movie(name='MR. SUNSHINE', price=210000, image='images/p10.png')
        # db.session.add_all([m1, m2, m3, m4, m5, m6, m7, m8, m9, m10])
        # db.session.commit()

        # mt1 = MovieTag(movie_id=1, tag_id=1)
        # mt2 = MovieTag(movie_id=2, tag_id=1)
        # mt3 = MovieTag(movie_id=3, tag_id=1)
        # mt4 = MovieTag(movie_id=4, tag_id=1)
        # mt5 = MovieTag(movie_id=5, tag_id=3)
        # mt6 = MovieTag(movie_id=6, tag_id=1)
        # mt7 = MovieTag(movie_id=7, tag_id=1)
        # mt8 = MovieTag(movie_id=8, tag_id=2)
        # mt9 = MovieTag(movie_id=9, tag_id=2)
        # mt10 = MovieTag(movie_id=10, tag_id=1)
        # db.session.add_all([mt1, mt2, mt3, mt4, mt5, mt6, mt7, mt8, mt9, mt10])
        # db.session.commit()

        # mg1 = MovieGenre(movie_id=1, genre_id=7)
        # mg2 = MovieGenre(movie_id=2, genre_id=2)
        # mg3 = MovieGenre(movie_id=3, genre_id=1)
        # mg4 = MovieGenre(movie_id=4, genre_id=5)
        # mg5 = MovieGenre(movie_id=5, genre_id=7)
        # mg6 = MovieGenre(movie_id=6, genre_id=7)
        # mg7 = MovieGenre(movie_id=7, genre_id=1)
        # mg8 = MovieGenre(movie_id=8, genre_id=5)
        # mg9 = MovieGenre(movie_id=9, genre_id=4)
        # mg10 = MovieGenre(movie_id=10, genre_id=5)
        # db.session.add_all([mg1, mg2, mg3, mg4, mg5, mg6, mg7, mg8, mg9, mg10])
        # db.session.commit()
        #
        # d1 = date(2023, 5, 24)
        # d2 = date(2023, 5, 25)
        #
        # sc1 = ShowSchedule(time=d1, movie_id=1)
        # sc2 = ShowSchedule(time=d2, movie_id=1)
        # db.session.add_all([sc1, sc2])
        # db.session.commit()

        # t_start1 = time(7, 0, 0)
        # t_end1 = time(9, 0, 0)
        # t_start2 = time(10, 0, 0)
        # t_end2 = time(12, 0, 0)
        # t_start3 = time(19, 0, 0)
        # t_end3 = time(21, 0, 0)
        #
        # st1 = Showtime(name='morning', start_time=t_start1, end_time=t_end1, rate=0.5)
        # st2 = Showtime(name='noon', start_time=t_start2, end_time=t_end2, rate=0.7)
        # st3 = Showtime(name='night', start_time=t_start3, end_time=t_end3, rate=0.75)
        # db.session.add_all([st1, st2, st3])
        # db.session.commit()
        #
        # sr1 = ShowRoom(name='P001', capacity=5)
        # sr2 = ShowRoom(name='P002', capacity=12)
        # db.session.add_all([sr1, sr2])
        # db.session.commit()
        #
        # sh1 = Show(show_schedule_id=1, showtime_id=1, show_room_id=1)
        # sh2 = Show(show_schedule_id=1, showtime_id=2, show_room_id=2)
        # sh3 = Show(show_schedule_id=2, showtime_id=3, show_room_id=1)
        # sh4 = Show(show_schedule_id=2, showtime_id=3, show_room_id=2)
        # db.session.add_all([sh1, sh2, sh3, sh4])
        # db.session.commit()

        s1 = Seat(name='S01', show_room_id=1)
        s2 = Seat(name='S02', show_room_id=1)
        s3 = Seat(name='S03', show_room_id=1)
        s4 = Seat(name='S01', show_room_id=2)
        s5 = Seat(name='S02', show_room_id=2)
        s6 = Seat(name='S03', show_room_id=2)
        db.session.add_all([s1, s2, s3, s4, s5, s6])
        db.session.commit()
