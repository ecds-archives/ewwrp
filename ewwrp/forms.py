from django import forms
from settings import COLLECTIONS
from eulxml.xmlmap.teimap import Tei, TeiDiv, TEI_NAMESPACE

class SearchForm(forms.Form):
    keyword = forms.CharField(required=False)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        terms = ['keyword']
        
        # Make sure at least one term is in cleaned_data
        for term in terms:
            if term in cleaned_data and cleaned_data[term]:
                return cleaned_data
        raise forms.ValidationError("Please enter search terms.")
    
class AdvancedSearchForm(forms.Form):
    keyword = forms.CharField(required=False)
    title = forms.CharField(required=False)
    collection = forms.MultipleChoiceField(choices=[(x,y['name']) for x,y in COLLECTIONS.items()], required=False)
    # Still need to implement these
    # author = forms.CharField(required=False)
    # date = forms.DateField(label="Date", widget=forms.DateInput, required=False)
    # subject = forms.CharField(label="Subject", max_length=100, required=False)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        terms = ['keyword', 'title', 'collection']
        
        # Make sure at least one term is in cleaned_data
        for term in terms:
            if term in cleaned_data and cleaned_data[term]:
                return cleaned_data
        raise forms.ValidationError("Please enter search terms.")