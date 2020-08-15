from .models import ShumilogUser
from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, label='ユーザ名', max_length=15)
    password = forms.CharField(widget=forms.PasswordInput, label='パスワード', max_length=15)
    password_retype = forms.CharField(widget=forms.PasswordInput, label='パスワード(確認)', max_length=15)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if ShumilogUser.objects.filter(username=username).exists():
            raise forms.ValidationError('The username has been already taken.')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 5:
            raise forms.ValidationError('Password must contain 5 or more characters.')
        return password

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        retyped = self.cleaned_data.get('password_retype')
        if password and retyped and (password != retyped):
            self.add_error('password_retype', 'This does not match with the above.')

    def save(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        new_user = ShumilogUser.objects.create_user(username=username)
        new_user.set_password(password)
        new_user.save()
