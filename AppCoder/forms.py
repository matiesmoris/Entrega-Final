from django import forms

class PersonaForm(forms.Form): #Tiene que cumplir las mismas reglas que Persona en models.py
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    fecha_nacimiento = forms.DateField()

class BuscarPersonasForm(forms.Form):
    criterio_nombre=forms.CharField(max_length=100)

