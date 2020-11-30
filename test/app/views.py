from flask import render_template, url_for, request, redirect, flash
from app import app, db
from .forms import FilmForm, UpdateForm
from .models import Film, Genre
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
def index():
    filmForm = FilmForm()
    available_genre = Genre.query.all()
    genres = [(g.id, g.genre) for g in available_genre]
    filmForm.genres.choices = genres

    if filmForm.validate_on_submit():
        name = filmForm.name.data
        release_date = filmForm.release_date.data
        director = filmForm.director.data
        description = filmForm.description.data
        budget = float(filmForm.budget.data)
        genre_id = filmForm.genres.data
        genre = Genre.query.get(genre_id)
        film = Film(name=name, director=director, release_date=release_date, description=description, budget=budget, genre=genre)
        db.session.add(film)
        db.session.commit()
    
    return render_template('film.html', form=filmForm)


@app.route('/films/', methods=['GET', 'POST'])
def films():
    q = request.args.get('q')

    films = Film.query.order_by(Film.budget.asc())

    if q:
        films = Film.query.filter(Film.description.contains(q) | Film.name.contains(q))
    
    return render_template('films.html', films=films, query=q)


@app.route('/films/<int:film_id>/delete/', methods=['GET', 'POST'])
def delete_film(film_id):
    film = Film.query.get(film_id)
    db.session.delete(film)
    db.session.commit()
    flash(f'{film.name} was deleted!', 'success')
    return redirect(url_for('films'))

@app.route('/films/<int:film_id>/update/', methods=['GET', 'POST'])
def update_film(film_id):
    film = Film.query.get(film_id)
    update_form = UpdateForm()
    available_genre = Genre.query.all()
    genres = [(g.id, g.genre) for g in available_genre]
    update_form.genres.choices = genres
    if update_form.validate_on_submit():
        film.name = update_form.name.data
        film.release_date = update_form.release_date.data
        film.director = update_form.director.data
        film.description = update_form.description.data
        film.budget = float(update_form.budget.data)
        genre = Genre.query.get(update_form.genres.data)
        film.genre = genre
        db.session.commit()
        return redirect(url_for('films'))

    return render_template('update_film.html', form=update_form, film=film)