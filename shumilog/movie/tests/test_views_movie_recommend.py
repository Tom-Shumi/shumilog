from django.urls import reverse_lazy
from movie.views import *

from ..models import *
from common.tests.test_common import LoggedInTestCase


class TestMovieRecommendView(LoggedInTestCase):

    def test_recommend_to_watch_later_success(self):
        movie = MovieM.objects.create(movie_id='1', movie_title='テスト', released_date='2000-01-01', movie_summary='あらすじ')
        movie_genre_m = MovieGenreM.objects.get(movie_genre_id='12')
        movie.movie_genres.add(movie_genre_m)

        params = {
            'm_id': '1',
        }

        response = self.client.post(reverse_lazy('movie:recommend_to_watch_later'), params)
        self.assertRedirects(response, reverse_lazy('movie:recommend_list'))
        self.assertEqual(MovieWatchLaterT.objects.filter(movie_id='1').count(), 1)
