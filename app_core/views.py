from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy, reverse

from django.views.generic import TemplateView, CreateView
from django.views.generic.edit import FormView

from django.http import HttpResponseRedirect
from .forms import UserRegisterForm, LoginForm
from app_article.models import ArticleModel
from django.views.generic import ListView


class HomeView(ListView):
    model = ArticleModel
    template_name = "core/home.html"
    context_object_name = "articles"
    
    def get_queryset(self):
        queryset = ArticleModel.objects.all()

        # Filtro por autor
        author = self.request.GET.get('author')
        if author:
            queryset = queryset.filter(author__username__icontains=author)

        # Filtro por categoría
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__icontains=category)
            
        return queryset
    
    
class LegalView(TemplateView):
    template_name = "core/legal.html"
    
    
class ContactView(TemplateView):
    template_name = "core/contact.html"
    
        
class RegisterView(CreateView):
    model = User
    template_name = "core/register.html"
    success_url = reverse_lazy('core:login')
    form_class = UserRegisterForm
    
    def form_valid(self, form):
        messages.success(self.request, ("Usuario creado correctamente"))
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class LoginView(FormView):
    template_name = "core/login.html"
    form_class = LoginForm
    
    def form_valid(self, form):
        usuario = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=usuario, password=password)
        
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f'Bienvenido {user.username}')
            return HttpResponseRedirect(reverse('core:home'))
        else:
            messages.error(self.request, "Usuario o contraseña no válido")
            return super(LoginView, self).form_invalid(form)


@login_required   
def logout_view(request):
    logout(request)
    messages.info(request, ("Sesión cerrada correctamente"))
    return HttpResponseRedirect(reverse('core:home'))


