from .models import MovieReviewT
from django import forms
from .models import *



class MovieReviewCreateForm(forms.ModelForm):
    class Meta:
        model = MovieReviewT
        fields = []

    movie_title = forms.CharField(label='映画タイトル', max_length=40, required=False)
    watched_year = forms.IntegerField(label='視聴年', max_value=9999, min_value=2000, required=True)
    watched_month = forms.IntegerField(label='視聴月', max_value=12, min_value=1, required=True)
    watched_day = forms.IntegerField(label='視聴日', max_value=31, min_value=1, required=True)
    movie_review_score = forms.IntegerField(label='点数', max_value=5, min_value=1, required=True)
    movie_review = forms.CharField(label='レビュー', widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False)
    movie_image = forms.ImageField(label='画像', required=False)

    # hidden
    movie_id_hidden = forms.CharField(widget=forms.HiddenInput, required=False)
    movie_title_hidden = forms.CharField(widget=forms.HiddenInput, required=False)
    released_date_hidden = forms.CharField(widget=forms.HiddenInput, required=False)
    genre_ids_hidden = forms.CharField(widget=forms.HiddenInput, required=False)
    movie_summary_hidden = forms.CharField(widget=forms.HiddenInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MovieReviewSearchForm(forms.Form):
    watched_date_from = forms.CharField(label='視聴日From', max_length=10, required=False,
                                        widget=forms.TextInput(attrs={'placeholder': 'YYYY/MM/DD'}))
    watched_date_to = forms.CharField(label='視聴日To', max_length=10, required=False,
                                        widget=forms.TextInput(attrs={'placeholder': 'YYYY/MM/DD'}))
    movie_title = forms.CharField(label='映画タイトル', max_length=40, required=False)
    movie_score_from = forms.IntegerField(label='点数From', max_value=5, min_value=1, required=False)
    movie_score_to = forms.IntegerField(label='点数To', max_value=5, min_value=1, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MovieWatchLaterForm(forms.Form):
    movie_title = forms.CharField(label='映画タイトル', max_length=40, required=False)

    # hidden
    movie_id_hidden = forms.CharField(widget=forms.HiddenInput, required=False)
    movie_title_hidden = forms.CharField(widget=forms.HiddenInput, required=False)
    released_date_hidden = forms.CharField(widget=forms.HiddenInput, required=False)
    genre_ids_hidden = forms.CharField(widget=forms.HiddenInput, required=False)
    movie_summary_hidden = forms.CharField(widget=forms.HiddenInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MovieRecommendSearchForm(forms.Form):
    movie_title = forms.CharField(label='映画タイトル', max_length=40, required=False)
    released_date_from = forms.CharField(label='公開日From', max_length=10, required=False,
                                        widget=forms.TextInput(attrs={'placeholder': 'YYYY/MM/DD'}))
    released_date_to = forms.CharField(label='公開日To', max_length=10, required=False,
                                        widget=forms.TextInput(attrs={'placeholder': 'YYYY/MM/DD'}))
    movie_genre = forms.ModelChoiceField(label='映画ジャンル', queryset=MovieGenreM.objects.all().order_by('movie_genre_id'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
