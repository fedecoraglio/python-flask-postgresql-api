from flask import Blueprint, jsonify, request

# Entitties
from models.entities.Movie import Movie

# Models
from models.MovieModel import MovieModel

main = Blueprint("movie_bluprint", __name__)


@main.route("/")
def get_movies():
    try:
        movies = MovieModel.get_movies()
        return jsonify(movies)
    except Exception as ex:
        return jsonify({"message": ex.args}), 500


@main.route("/<id>")
def get_movie(id):
    try:
        movie = MovieModel.get_movie(id)
        if movie != None:
            return jsonify(movie)
        else:
            return jsonify({}), 404

    except Exception as ex:
        return jsonify({"message": ex.args}), 500


@main.route("/", methods=["POST"])
def add_movie():
    try:
        print(request.json)
        title = request.json["title"]
        duration = int(request.json["duration"])
        released = request.json["released"]
        print(title, duration, released)
        movie = Movie("", title, duration, released)
        movie = MovieModel.add_movie(movie)
        return jsonify(movie)

    except Exception as ex:
        return jsonify({"message": ex.args}), 500

@main.route("/<id>", methods=["DELETE"])
def delete_movie(id):
    try:
        movie = MovieModel.get_movie(id)
        if movie != {}:
          MovieModel.delete_movie(id)
          return jsonify(id)

        return jsonify({"message": "Movie not found"}), 404
    except Exception as ex:
        return jsonify({"message": ex.args}), 500

@main.route("/<id>", methods=["PUT"])
def update_movie(id):
    try:
        validateMovie = MovieModel.get_movie(id)
        if validateMovie != {}:
          title = request.json["title"]
          duration = int(request.json["duration"])
          released = request.json["released"]
          movie = Movie(None,title, duration, released)
          movie = MovieModel.update_movie(id, movie)
          return jsonify(movie)

        return jsonify({"message": "Movie not found"}), 404
    except Exception as ex:
        return jsonify({"message": ex.args}), 500
