"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db


# FUNCTIONS BELOW 


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def all_users():
    """return all users"""

    return User.query.all()

def get_user_by_id(user_id):
    """Return user by id"""

    return User.query.get(user_id)

def get_user_by_email(user_email):
    """Return user by use"""
    return User.query.filter(User.email == user_email).all()

def create_movie(title, overview, release_date, poster_path):
    """""Create and return """
    movie = Movie(
        title=title, 
        overview=overview, 
        release_date=release_date,
        poster_path=poster_path,
    )

    return movie

def all_movies():

    return Movie.query.all()

def get_movie_by_id(movie_id):
    return Movie.query.get(movie_id)



def create_rating(user, movie, score):
    """Create and return a new rating."""
    
    rating = Rating(user=user, movie=movie, score=score)

    return rating



if __name__ == '__main__':
    from server import app
    connect_to_db(app)


