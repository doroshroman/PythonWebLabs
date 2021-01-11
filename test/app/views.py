from flask import render_template, url_for, request, redirect, flash, make_response, jsonify, abort
from app import app, db
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


"""
--------------------------------------------------------------
---------------------------API--------------------------------
"""

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.route('/api/v1/films/', methods=['GET'])
def api_get_films():
    films = Film.query.all()
    films_list = [film.serialize for film in films]
    return jsonify({'films': films_list})

@app.route('/api/v1/films/<int:film_id>/', methods=['GET'])
def api_get_film(film_id):
    film = Film.query.get(film_id)
    if not film:
        return abort(404)
    return jsonify({'film': film.serialize}), 200

@app.route('/api/v1/films/<int:film_id>', methods=['DELETE'])
def api_delete_film(film_id):
    film = Film.query.get(film_id)
    if not film:
        abort(404)
    
    db.session.delete(film)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/v1/films/', methods=['POST'])
def api_post_film():
    req = request.json
    if not req or not 'name' in req or not 'director' in req or not 'budget' in req:
        abort(400)
    
    release_date = req.get('release_date')
    name = req.get('name')
    director = req.get('director')
    description = req.get('description')
    budget = req.get('budget')
    genre_id = req.get('genre_id')
    
    genre = Genre.query.get(int(genre_id))
    
    if not genre:
        abort(404)

    film = Film(release_date=release_date, name=name, director=director, description=description, budget=budget, genre=genre)
    db.session.add(film)
    db.session.commit()
    return jsonify({'film': film.serialize}), 201

@app.route('/api/v1/films/<int:film_id>', methods=['PUT'])
def api_update_film(film_id):
    film = Film.query.get(film_id)
    req = request.json
    if not film:
        abort(404)
    if not req:
        abort(400)
    
    release_date = req.get('release_date')
    name = req.get('name')
    director = req.get('director')
    description = req.get('description')
    budget = req.get('budget')
    genre_id = req.get('genre_id')
    genre = Genre.query.get(int(genre_id))
    
    if not genre:
        abort(404)

    film.release_date = release_date if release_date else datetime.utcnow()
    film.name = name
    film.director = director
    film.description = description
    film.budget = budget
    film.genre = genre
    db.session.commit()
    return jsonify({'film': film.serialize})