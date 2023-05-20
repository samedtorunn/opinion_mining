from django import forms

class QueryForm(forms.Form):
    query = forms.CharField(max_length=100)
    start_date = forms.DateField()
    end_date = forms.DateField()
