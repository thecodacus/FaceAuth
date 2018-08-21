from django.contrib.auth.models import User
from django import forms
from .models import FaceSignature

class UserRegForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput)
	password.widget.attrs.update({'class': 'form-control'})
	class Meta:
		model = User
		fields = ('username','email','password')
		widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'})
        }

class UserLoginForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput)
	password.widget.attrs.update({'class': 'form-control'})
	class Meta:
		model = User
		fields = ('username','password')
		widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UserFaceRegForm(forms.ModelForm):
	class Meta:
		model = FaceSignature
		fields={}