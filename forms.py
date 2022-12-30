from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    image = forms.ImageField()



class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)