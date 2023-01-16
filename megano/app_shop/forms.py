from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User

from app_shop.models import Profile, Review, Order


class SignUpForm(UserCreationForm):
    phone = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '9998887766', 'data-validate': 'require'})
    )
    full_name = forms.CharField(
        label='ФИО',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Иванов Иван Иванович',
            'data-validate': 'require'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-input', 'data-validate': 'require'})
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Введите пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Введите пароль повторно'})


class UserProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'full_name', 'user_photo']
        widgets = {
            'user_photo': forms.FileInput(
                attrs={
                    'data-validate': 'onlyImgAvatar',
                    'class': 'Profile-file form-input',
                    'type': 'file',

                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'required': True
                }
            ),
            'full_name': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'required': True
                }
            )
        }

class UserDataUpdate(UserChangeForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-input', 'required': True})
        }


class ChangePasswordForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Тут можно изменить пароль'}),
    )
    new_password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Введите пароль повторно'}),
    )

class RestorePasswordForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Укажите адрес электронной почты'}),
        error_messages={'required': 'Неверный адрес'}
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Адрес электронной почты'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Введите пароль'})
    )

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['full_name', 'email', 'text']
        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'class': 'form-input'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-input'
                }
            ),
            'text': forms.Textarea(
                attrs={
                    'class': 'form-textarea',
                    'placeholder': 'Review'
                }
            )
        }
