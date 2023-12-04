from django.forms import ModelForm
from .models import Task, licuefac, molienda
from django import forms
from .models import Incidente
from .models import Datos

class CorreoForm(forms.Form):
    asunto = forms.CharField(max_length=100)
    cuerpo = forms.CharField(widget=forms.Textarea)

class DatosForm(forms.ModelForm):
    class Meta:
        model = Datos
        fields = ['campo1', 'campo2']

        
class IncidenteForm(forms.ModelForm):
    class Meta:
        model = Incidente
        fields = ['titulo', 'descripcion']


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']



class licuefacForm(ModelForm):
    class Meta:
        model = licuefac
        fields = ['campo1', 'campo2']

class moliendaForm(forms.ModelForm):
    class Meta:
        model = molienda
        fields = ['campo1', 'campo2']

