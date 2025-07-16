from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import MyUser, BookDet, NotesDet, ChatW, BookReq

class SignUpForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'full_name', 'gender', 'college', 'city', 'state', 'country', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class BookForm(forms.ModelForm):
    class Meta:
        model = BookDet
        fields = ['title', 'author', 'publication', 'year', 'mrp', 'description', 'image', 'category', 'subcategory1', 'subcategory2']

class NotesForm(forms.ModelForm):
    class Meta:
        model = NotesDet
        fields = ['title', 'description', 'file', 'publication', 'year', 'category', 'subcategory1', 'subcategory2']

class MessageForm(forms.ModelForm):
    class Meta:
        model = ChatW
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your message...'}),
        }

class BookRequestForm(forms.ModelForm):
    class Meta:
        model = BookReq
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
