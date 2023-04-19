from django.shortcuts import render
from AppCoder.models import Tarea, Persona
from AppCoder.forms import PersonaForm, BuscarPersonasForm
from django.views.generic import ListView

def mostrar_mi_template(request,nombre,apellido):
    context={
        "nombre":nombre, #se puede usar title(),etc
        "apellido":apellido,
        "notas":[5,6,7,8,9,10],
    }
    return render(request, "AppCoder/index.html", context)

def mostrar_mis_tareas(request,criterio):
    if criterio == "todo":
        tareas = Tarea.objects.all()
    elif criterio:
        tareas = Tarea.objects.filter(nombre=criterio).all() #aca le hicimos un filtro
    
    return render(request,"AppCoder/tareas.html",{"tareas":tareas})

def mostrar_personas(request):

    personas = Persona.objects.all()
    total_personas = len(personas)
    context = {
        "personas": personas,
        "total_personas":total_personas,
        "form": PersonaForm(),
    }
    return render(request, "AppCoder/personas.html", context)

def crear_persona(request):

    f = PersonaForm(request.POST)
    context = {
        "form": f
    } 
    if f.is_valid():
        Persona(nombre=f.data["nombre"], apellido=f.data["apellido"], fecha_nacimiento=f.data["fecha_nacimiento"]).save()
        context['form'] = PersonaForm()

    context["personas"] = Persona.objects.all()
    context["total_personas"] = len(Persona.objects.all())
    return render(request,"AppCoder/personas.html", context)

class BuscarPersonas(ListView):
    model = Persona
    context_object_name = "personas"

    def get_queryset(self):
        f= BuscarPersonasForm(self.request.GET)
        if f.is_valid():
            return Persona.objects.filter(nombre__icontains=f.data["criterio_nombre"]).all()
        return Persona.objects.none()



    

