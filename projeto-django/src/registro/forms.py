
from django import forms            
from .models import User  

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
   
    class Meta:
        model = User
        fields = ('nome', 'email', 'login', 'password') 
        
	


