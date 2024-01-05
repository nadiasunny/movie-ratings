"""Script to seed database"""


import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb ratings')
# More code will go here

os.system('createdb ratings')
model.connect_to_db(server.app)
model.db.create_all()

# Loop over each dictionary in movie_data and use it to supply arguments to 
# crud.create_movie. You’ll also going to want to add each new movie to a list 
# because we’re going to need them later to create random ratings. 
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

    movies_in_db = []

    for movie in movie_data:
        title = movie['title']
        overview = movie['overview']
        poster = movie['poster_path']
        format = '%Y-%m-%d'
        release = datetime.strptime(movie['release_date'], format)

        movie_obj = crud.create_movie(title, overview, release, poster)
        movies_in_db.append(movie_obj)

model.db.session.add_all(movies_in_db)
model.db.session.commit()

for n in range(10):
    email = f'MR.user{n}@mystery.com'
    password = 'mysterious'

    current_user = crud.create_user(email, password)
    ratings = []
    for m in range(10):
        ratings.append(crud.create_rating(current_user, choice(movies_in_db), randint(0,5)))
    model.db.session.add_all(ratings)
    model.db.session.commit()
