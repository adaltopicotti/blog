from django import forms
from .models import Post, Comment, ForLogic, Cotador

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)
  

class Register_4logic(forms.ModelForm):
    class Meta:
        model = ForLogic
        fields = ('nome', 'email',)

class CotadorForm(forms.ModelForm):
    class Meta:
        model = Cotador
        fields = ('nome', 'safra', 'cultura', 'ativo')
