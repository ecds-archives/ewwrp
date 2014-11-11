from django import forms
from settings import COLLECTIONS
from eulxml.xmlmap.teimap import Tei, TeiDiv, TEI_NAMESPACE

def generic_clean(self, terms):
    cleaned_data = self.cleaned_data

    # Make sure at least one term is in cleaned_data
    for term in terms:
        if term in cleaned_data and cleaned_data[term]:
            return cleaned_data
    raise forms.ValidationError("Please enter search terms.")

class SearchForm(forms.Form):
    keyword = forms.CharField(required=False)
    author = forms.CharField(required=False)
    title = forms.CharField(required=False)
    collection = forms.MultipleChoiceField(choices=[(x,y['name']) for x,y in COLLECTIONS.items()], required=False)
    
    def clean(self):
        terms = ['keyword','author','title','collection',]
        return generic_clean(self, terms)
    
class AdvancedSearchForm(forms.Form):
    keyword = forms.CharField(required=False)
    
    def clean(self):
        terms = ['keyword']
        return generic_clean(self, terms)

class FulltextSearch(forms.Form):
    keyword = forms.CharField(required=False)
    
    def clean(self):
        terms = ['keyword']
        return generic_clean(self, terms)