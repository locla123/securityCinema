from app.models import Genre, Tag, Movie, MovieTag, MovieGenre, User, ShowSchedule, ShowRoom, Showtime, Show, Seat, \
    Ticket
from app import app, db
from app.encode import blowfish
from flask_login import current_user


def load_tags():
    return Tag.query.all()


def load_genres():
    return Genre.query.all()


def load_movies(tag_id=None, genre_id=None, page=None):
    movies = Movie.query

    if tag_id:
        movies = Movie.query.join(MovieTag).filter(MovieTag.tag_id.__eq__(tag_id))
    if genre_id:
        movies = Movie.query.join(MovieGenre).filter(MovieGenre.genre_id.__eq__(genre_id))
    if page:
        page_size = app.config['PAGE_SIZE']
        start = page * page_size - page_size
        end = start + page_size

    return movies.slice(start, end).all()


def count_movie():
    return Movie.query.count()


def get_movie_by_id(movie_id=None):
    if movie_id:
        return Movie.query.get(movie_id)


def check_user_existence(email=None, username=None):
    if email:
        user = User.query.filter(User.email.__eq__(email.strip())).first()
        if user:
            return False
    if username:
        user = User.query.filter(User.username.__eq__(username.strip())).first()
        if user:
            return False

    return True


def add_user(full_name=None, email=None, username=None, password=None, avatar_path=None, key=None):
    if full_name and email and username and password and key:
        password = blowfish.encrypt(password.strip(), key)
        with app.app_context():
            user = User(full_name=full_name,
                        email=email,
                        username=username,
                        password=password,
                        avatar=avatar_path,
                        key=key)

            db.session.add(user)
            db.session.commit()


def get_user_by_id(user_id):
    with app.app_context():
        return User.query.get(user_id)


def check_user_valid(username=None, password=None):
    if username and password:
        with app.app_context():
            user = User.query.filter(User.username.__eq__(username.strip())).first()
            # print(blowfish.encrypt(password.strip(), user.key))
            if blowfish.decrypt(user.password, user.key).__eq__(password):
                return user


# SELECT m.name, sc.time, st.start_time, st.end_time, sr.name
# FROM cinemaapp.movie m
# LEFT JOIN cinemaapp.show_schedule sc
# ON m.id = sc.movie_id
# LEFT JOIN cinemaapp.show sh
# ON sc.id = sh.show_schedule_id
# LEFT JOIN cinemaapp.showtime st
# ON st.id = sh.showtime_id
# LEFT JOIN cinemaapp.show_room sr
# ON sh.show_room_id = sr.id
# WHERE m.id = 1
# GROUP BY m.name, sc.time, st.start_time, st.end_time, sr.name

# def get_shows(movie_id=None, time=None):
#     with app.app_context():
#         shows = db.session.query(Movie.name, ShowSchedule.time, Showtime.start_time, Showtime.end_time, ShowRoom.name) \
#             .join(Movie, ShowSchedule.movie_id.__eq__(Movie.id)).group_by(Movie.name, ShowSchedule.time) \
#             .join(Show, Show.show_schedule_id.__eq__(ShowSchedule.id)) \
#             .join(Showtime, Showtime.id.__eq__(Show.showtime_id)).group_by(Showtime.start_time, Showtime.end_time) \
#             .join(ShowRoom, ShowRoom.id.__eq__(Show.show_room_id)).group_by(ShowRoom.name)
#         if movie_id:
#             shows = shows.filter(Movie.id.__eq__(movie_id))
#         if time:
#             shows = shows.filter(ShowSchedule.time.__eq__(time))
#
#         return shows.all()

def get_shows(movie_id=None):
    with app.app_context():
        shows = db.session.query(ShowSchedule.id, Movie.name, ShowSchedule.time) \
            .join(Movie, Movie.id.__eq__(ShowSchedule.movie_id)) \
            .group_by(ShowSchedule.id, Movie.id, Movie.name, ShowSchedule.time)
        if movie_id:
            shows = shows.filter(Movie.id.__eq__(movie_id))
        return shows.all()


# def get_showtime(show_schedule_id=None):
#     with app.app_context():
#         showtime = db.session.query(Show.id, Showtime.start_time, Showtime.end_time) \
#             .join(ShowSchedule, ShowSchedule.id.__eq__(Show.show_schedule_id)).group_by(Show.id, ShowSchedule.id) \
#             .join(Showtime, Showtime.id.__eq__(Show.showtime_id)).group_by(Showtime.id, Showtime.start_time,
#                                                                            Showtime.end_time)
#         if show_schedule_id:
#             showtime = showtime.filter(Show.show_schedule_id.__eq__(show_schedule_id))
#
#         return showtime.all()


def get_showroom(show_schedule_id=None):
    if show_schedule_id:
        with app.app_context():
            showroom = db.session.query(Showtime.id, Showtime.start_time, Showtime.end_time,
                                        ShowRoom.name, ShowRoom.id.label('showroom_id')) \
                .join(Show, Show.showtime_id == Showtime.id) \
                .join(ShowSchedule, Show.show_schedule_id == ShowSchedule.id) \
                .join(ShowRoom, Show.show_room_id == ShowRoom.id) \
                .group_by(Showtime.id, Showtime.start_time, Showtime.end_time, ShowRoom.name, ShowRoom.id)

            showroom = showroom.filter(ShowSchedule.id.__eq__(show_schedule_id))

            return showroom.all()


def get_showtime_rate(showtime_id=None):
    if showtime_id:
        with app.app_context():
            return Showtime.query.get(showtime_id).rate


def get_seats(showroom_id=None):
    with app.app_context():
        seats = db.session.query(Seat.name, Seat.id).join(ShowRoom, ShowRoom.id.__eq__(Seat.show_room_id)).group_by(
            Seat.name, Seat.id)

        seats = seats.filter(Seat.show_room_id.__eq__(showroom_id))

        return seats.all()


def pay_ticket(movie_id=None, show_schedule_id=None, showtime_id=None, showroom_id=None, seat_id=None,
               total_price=None):
    if movie_id and show_schedule_id and showtime_id and showroom_id and seat_id and total_price:
        with app.app_context():
            t = Ticket(movie_id=movie_id,
                       show_schedule_id=show_schedule_id,
                       showtime_id=showtime_id,
                       showroom_id=showroom_id,
                       seat_id=seat_id,
                       user=current_user,
                       total_price=total_price)
            db.session.add(t)
            db.session.commit()


def get_user_by_username(username=None):
    with app.app_context():
        if username:
            return User.query.filter(User.username.__eq__(username.strip())).first()


def change_user_password(username, new_pass):
    with app.app_context():
        user = User.query.filter(User.username.__eq__(username.strip())).first()
        if user:
            user.password = blowfish.encrypt(new_pass.strip(), blowfish.generate_key())
            db.session.commit()
            return user
        return None


def get_ticket_info():
    with app.app_context():
        ticket = db.session.query(Ticket.id, Showtime.start_time, Showtime.end_time, ShowSchedule.time, Movie.name.label('movie_name'),
                                  ShowRoom.name.label('showroom_name'), Seat.name.label('seat_name')) \
            .join(Ticket, Ticket.showtime_id.__eq__(Showtime.id)) \
            .join(ShowSchedule, ShowSchedule.id.__eq__(Ticket.show_schedule_id)) \
            .join(Movie, Movie.id.__eq__(Ticket.movie_id)) \
            .join(ShowRoom, ShowRoom.id.__eq__(Ticket.showroom_id)) \
            .join(Seat, Seat.id.__eq__(Ticket.seat_id)) \
            .group_by(Ticket.id, Showtime.start_time, Showtime.end_time, ShowSchedule.time, Movie.name,
                      ShowRoom.name, Seat.name)
        if current_user:
            ticket = ticket.filter(Ticket.user_id.__eq__(current_user.id))
        return ticket.all()


print(get_ticket_info())
