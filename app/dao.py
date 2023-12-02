from app.models import Genre, Tag, Movie, MovieTag, MovieGenre, User, ShowSchedule, ShowRoom, Showtime, Show, Seat, \
    Ticket
from app import app, db
from app.encode import blowfish, RSA, caesar
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
        user = None
        for u in User.query.all():
            if blowfish.decrypt(u.email, u.key).__eq__(email.strip()):
                user = u
                break
        # user = User.query.filter(User.email.__eq__(email.strip())).first()
        if user:
            return False
    if username:
        user = None
        for u in User.query.all():
            if blowfish.decrypt(u.username, u.key).__eq__(username.strip()):
                user = u
        # user = User.query.filter(User.username.__eq__(username.strip())).first()
        if user:
            return False

    return True


def add_user(full_name=None, email=None, username=None, password=None, avatar_path=None, key=None):
    if full_name and email and username and password and key:
        full_name = blowfish.encrypt(full_name.strip(), key)
        email = blowfish.encrypt(email.strip(), key)
        username = blowfish.encrypt(username.strip(), key)
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
        user = User.query.get(user_id)
        # user.full_name = blowfish.decrypt(user.full_name, user.key)
        # user.email = blowfish.decrypt(user.email, user.key)
        # user.username = blowfish.decrypt(user.username, user.key)
        return user


def check_user_valid(username=None, password=None):
    if username and password:
        with app.app_context():
            # user = User.query.filter(User.username.__eq__(blowfish.encrypt(username.strip(), User.key))).first()
            # user = User.query.filter(blowfish.decrypt(User.username, User.key).__eq__(username)).first()
            # if blowfish.decrypt(user.password, user.key).__eq__(password):
            #     return user
            user = None
            for u in User.query.all():
                if blowfish.decrypt(u.username, u.key).__eq__(username.strip()):
                    user = u
                    break
            if blowfish.decrypt(user.password, user.key).__eq__(password):
                user.full_name = blowfish.decrypt(user.full_name, user.key)
                user.email = blowfish.decrypt(user.email, user.key)
                user.username = blowfish.decrypt(user.username, user.key)
                return user


# check_user_valid(username='admin', password='123')

def get_shows(movie_id=None):
    with app.app_context():
        shows = db.session.query(ShowSchedule.id, Movie.name, ShowSchedule.time) \
            .join(Movie, Movie.id.__eq__(ShowSchedule.movie_id)) \
            .group_by(ShowSchedule.id, Movie.id, Movie.name, ShowSchedule.time)
        if movie_id:
            shows = shows.filter(Movie.id.__eq__(movie_id))
        return shows.all()


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
        user = None
        if username:
            for u in User.query.all():
                if blowfish.decrypt(u.username, u.key).__eq__(username.strip()):
                    user = u
            return user


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
        ticket = db.session.query(Ticket.id, Showtime.start_time, Showtime.end_time, ShowSchedule.time,
                                  Movie.name.label('movie_name'),
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

# print(get_ticket_info())
# print(current_user)

# print(RSA.Ma_hoa('abc', RSA.e, RSA.N))

# def test():
#     user = None
#     with app.app_context():
#         for u in User.query.all():
#             if blowfish.decrypt(u.username, u.key).__eq__('locla123'):
#                 user = u
#     print(blowfish.decrypt(user.password, user.key))
# print(user)
# if user:
#     temp = RSA.Ma_hoa(blowfish.decrypt(user.email, user.key), RSA.e, RSA.N)
#     temp_dec = RSA.Giai_ma(temp, RSA.d, RSA.N)
#     print(temp)
#     print(temp_dec)


# test()
