from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    #Estos titulos no se pueden copiar en la entrega final
    carousel_caption_titel = models.CharField(max_length=30)
    carousel_caption_description = models.CharField(max_length=80)
    heading = models.CharField(max_length=15)
    description = models.CharField(max_length=120)
    publisher = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="publisher")
    #Aca agregamos el identificador unico del dueño de ese post, traes una llave unica de otro modelo y la usas aca
    #on_delete cascade si borras el usuario borra todos los posts del usuario
    #despues de hacer la relacion con ForeignKey tenes que importar de nuevo y te va a pedir que le des una opcion por defecto
    #pones 1 y 1
    imagen = models.ImageField(upload_to="posts", null=True, blank=True)
    creado_el = models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return f'{self.id} - {self.heading} - {self.description}'

class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile') #Se usa OneToOne y no ForeignKey porque queres que haya 1 perfil por cada usuario
    instagram = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to="profiles", null=True, blank=True)

class Mensaje(models.Model):
    mensaje = models.TextField(max_length=1000)
    email = models.EmailField()
    destinatario = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="destinatario")
