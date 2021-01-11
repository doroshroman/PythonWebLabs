from flask import render_template, url_for, request, redirect, flash, make_response, jsonify, abort
from app import app, db
from .models import Film, Genre
from datetime import datetime


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