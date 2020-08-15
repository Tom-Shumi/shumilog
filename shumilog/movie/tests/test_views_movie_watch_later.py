from django.urls import reverse_lazy
from movie.views import *

from ..models import *
from common.tests.test_common import LoggedInTestCase


class TestMovieWatchLaterView(LoggedInTestCase):

    def test_create_movie_watch_later_success(self):
        params = {
            'movie_id_hidden': '1',
            'movie_title_hidden': 'テスト',
            'released_date_hidden': '2000-01-01',
            'movie_summary_hidden': 'あらすじ',
            'genre_ids_hidden': '99',
        }

        response = self.client.post(reverse_lazy('movie:watch_later_create'), params)
        self.assertRedirects(response, reverse_lazy('movie:watch_later_list'))
        self.assertEqual(MovieWatchLaterT.objects.filter(movie_id='1').count(), 1)

    def test_movie_movie_watch_later_success(self):
        movie = MovieM.objects.create(movie_id='1', movie_title='テスト', released_date='2000-01-01', movie_summary='あらすじ')
        movie_genre_m = MovieGenreM.objects.get(movie_genre_id='12')
        movie.movie_genres.add(movie_genre_m)
        movie_watch_later = MovieWatchLaterT.objects.create(id=1, user=self.test_user, movie=movie)
        params = {
            'wl_id': '1',
        }

        self.assertEqual(MovieWatchLaterT.objects.filter(movie_id='1').count(), 1)

        response = self.client.post(reverse_lazy('movie:watch_later_delete'), params)
        self.assertRedirects(response, reverse_lazy('movie:watch_later_list'))
        self.assertEqual(MovieWatchLaterT.objects.filter(movie_id='1').count(), 0)
