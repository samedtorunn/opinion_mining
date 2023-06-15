from django import forms

class QueryForm(forms.Form):
    query = forms.CharField(label='Enter a query', max_length=100)
    start_date = forms.DateField()
    end_date = forms.DateField()

    second_query = forms.CharField(label='Enter a second query', max_length=100, required=False)
    second_start_date = forms.DateField(required=False)
    second_end_date = forms.DateField(required=False)
