from database.db import get_connection
from .entities.Movie import Movie


class MovieModel:
    @classmethod
    def get_movies(self):
        try:
            connection = get_connection()
            movies = []

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, title, duration, released FROM movies ORDER BY title ASC"
                )
                resultset = cursor.fetchall()

                for row in resultset:
                    movie = Movie(row[0], row[1], row[2], row[3])
                    movies.append(movie.to_JSON())

            connection.close()
            return movies
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_movie(self,id):
        try:
            connection = get_connection()
            movie={}
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, title, duration, released FROM movies WHERE id = %s", (id,))
                row = cursor.fetchone()

                if row != None:
                  movie = Movie(row[0], row[1], row[2], row[3])
                  movie = movie.to_JSON()

            connection.close()
            return movie
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_movie(self,movie):
        try:
            connection = get_connection()
            newMovie={}
            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO movies(title, duration, released)
                               VALUES (%s, %s, %s) RETURNING id""", (movie.title, movie.duration, movie.released))
                row = cursor.fetchone()
                connection.commit()
                newMovie = MovieModel.get_movie(row[0])

            connection.close()
            return newMovie
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_movie(self,id):
        try:
            connection = get_connection()
            updatedMovie={}
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM movies WHERE id = %s", (id,))
                connection.commit()

            connection.close()

            return id
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def update_movie(self,id, movie):
        try:
            connection = get_connection()
            updatedMovie={}
            with connection.cursor() as cursor:
                cursor.execute("""UPDATE movies SET title=%s, duration=%s, released=%s
                              WHERE id=%s""",
                               (movie.title, movie.duration, movie.released, id))
                connection.commit()
                updatedMovie = MovieModel.get_movie(id)

            connection.close()
            return updatedMovie
        except Exception as ex:
            raise Exception(ex)
