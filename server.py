"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/users', methods=['POST'])
def create_acc():
    user_email = request.form.get('email')
    user_password = request.form.get('password')
    num_of_users = len(crud.get_user_by_email(user_email))
    if (num_of_users == 0):
        current_user = crud.create_user(user_email, user_password)
        db.session.add(current_user)
        db.session.commit()
        flash('You have created an account!')
    elif(num_of_users == 1):
        flash('Account already exists')

    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    user_email = request.form.get('email')
    user_password = request.form.get('password')
    our_user = crud.get_user_by_email(user_email)[0]
    if (our_user.password == user_password):
        session['user'] = our_user.user_id
        flash('Logged In!')

    return redirect('/')


    

@app.route('/movies')
def show_movies():
    """Show list of all movies"""
    movies = crud.all_movies()
    return render_template('all_movies.html', movies = movies)

@app.route('/movies/<movie_id>')
def movie_details(movie_id):
    """Show details about movie."""
    movie = crud.get_movie_by_id(movie_id)
    
    return render_template('movie_details.html', movie = movie)

@app.route('/movies')
def user_rating(movie_id):
    movie = crud.get_movie_by_id(movie_id)
    user = crud.get_user_by_id(session['user'])
    user_rating = request.args.get('movie-rating')
    crud.create_rating(user, movie, user_rating)
    flash('rating added')
    return redirect('/movies')


@app.route('/users')
def show_users():
    """Show list of users"""
    users = crud.all_users()
    return render_template('all_users.html', users = users)

@app.route('/users/<user_id>')
def user_details(user_id):
    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user = user)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
