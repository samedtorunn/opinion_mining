from django import forms

class QueryForm(forms.Form):
    query = forms.CharField(label='Enter a query', max_length=100)
    compare_to = forms.CharField(label='Compare to', max_length=100, required=False)
    start_date = forms.DateField()
    end_date = forms.DateField()

    second_query = forms.CharField(label='Enter a second query', max_length=100, required=False)
    second_start_date = forms.DateField(required=False)
    second_end_date = forms.DateField(required=False)