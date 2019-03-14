from django import forms

class IndexForm(forms.Form):
	scholar_url = forms.CharField(max_length= 500)
	max_approx_publications = forms.CharField(max_length=100)