from django.forms import ModelForm
from .models import *

class Emap2SecForm(ModelForm):
    class Meta:
        model = Emap2SecJob
        fields = [ 'map_file', 'name', 'comment', 'contour', 'sstep', 'vw', 'norm' ]

class Emap2SecPlusForm(ModelForm):
    class Meta:
        model = Emap2SecPlusJob
        fields = []

class MainmastForm(ModelForm):
    class Meta:
        model = MainmastJob
        fields = [ 'map_file', 'name', 'comment', 'gw', 'Dkeep', 't', 'allow',
                   'filter', 'merge', 'Nround', 'Nnb', 'Ntb', 'Rlocal', 'Const' ]

class MainmastSegForm(ModelForm):
    class Meta:
        model = MainmastSegJob
        fields = []

