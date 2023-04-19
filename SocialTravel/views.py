from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from SocialTravel.models import Post, Profile, Mensaje
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def about(request):
    return render (request, "SocialTravel/about.html")

def index(request):
    context = {
        "posts": Post.objects.all()
    }
    return render(request, "SocialTravel/index.html", context)#El tercer argumento es el contexto

class PostList(ListView):
    model = Post
    #Post.objects.all() llama a esto

class PostDetail(DetailView):
    model = Post
    #Post.objects.get(id=pk) primary key

class PostCreate(LoginRequiredMixin, CreateView): #LoginRequiredMixin no le permite hacer estas acciones al usuario si no esta logeueado, va siempre primero en la herencia
    model = Post
    success_url = reverse_lazy("post-list") #cuando le das guardar te lleva a post-list
    fields = ['carousel_caption_titel','carousel_caption_description','heading','description','imagen']
    #fields = ['carousel_caption_titel', 'description']
    #Si queres seleccionar solo algunos campos, se sacan de models.py

    def form_valid(self, form):
        form.instance.publisher = self.request.user
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    success_url = reverse_lazy("post-list") #cuando le das guardar te lleva a post-list
    fields = ['carousel_caption_titel','carousel_caption_description','heading','description','imagen']

    def test_func(self): #Si el user id no coincide con el post id te tira error 403 FORBIDDEN
        user_id = self.request.user.id
        post_id = self.kwargs.get('pk')
        return Post.objects.filter(publisher=user_id, id=post_id).exists()
    
    def handle_no_permission(self): #Esto se hace para no revelar el 403 FORBIDDEN, ante ataques les mostras que el registro existe
        return render(self.request, "SocialTravel/not_found.html")
    
    def form_valid(self, form):
        form.instance.publisher = self.request.user
        return super().form_valid(form)

class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post-list") #cuando le das guardar te lleva a post-list

    def test_func(self): #Si el user id no coincide con el post id te tira error 403 FORBIDDEN
        user_id = self.request.user.id
        post_id = self.kwargs.get('pk')
        return Post.objects.filter(publisher=user_id, id=post_id).exists()
    
    def handle_no_permission(self): #Esto se hace para no revelar el 403 FORBIDDEN, ante ataques les mostras que el registro existe
        return render(self.request, "SocialTravel/not_found.html")
    
class SignUp(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy("post-list")

class Login(LoginView):
    next_page = reverse_lazy("post-list")

class Logout(LogoutView):
    template_name = 'registration/logout.html'

class ProfileUpdate(UpdateView):
    model = Profile
    fields = '__all__'

class MensajeCreate(CreateView):
    model = Mensaje
    fields = '__all__'
    success_url = reverse_lazy("post-list")

class MensajeList(LoginRequiredMixin, ListView):
    model = Mensaje
    context_object_name = "mensajes"

    def get_queryset(self):
        return Mensaje.objects.filter(destinatario=self.request.user.id).all()

class MensajeDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mensaje
    success_url = reverse_lazy("mensaje-list")

    def test_func(self): #Si el user id no coincide con el post id te tira error 403 FORBIDDEN
        user_id = self.request.user.id
        mensaje_id = self.kwargs.get('pk')
        return Mensaje.objects.filter(destinatario=user_id).exists()














    





