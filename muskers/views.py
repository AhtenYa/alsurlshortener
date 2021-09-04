from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import User

from .models import Culink, CulinkStats
from .forms import CulinkForm, LoginForm, RegisterForm, PasswordForm


class IndexView(LoginView):
    template_name = 'muskers/index.html'
    authentication_form = LoginForm
    redirect_field_name = 'muskers:user'
    redirect_authenticated_user = True


@method_decorator(login_required, name='dispatch')
class CreateCulinkView(FormView):
    template_name = 'muskers/user.html'
    form_class = CulinkForm
    success_url = 'shorts/'

    def shorten_by_user(self, tuser, longl, shortl):
        new_entry = Culink.objects.create(owner=tuser,
        longlink_text=longl, shortlink_text=shortl)

    def form_valid(self, form):
        longl = self.request.POST['longlink_text']
        shortl = self.request.POST['shortlink_text']
        tuser = self.request.user

        self.shorten_by_user(tuser, longl, shortl)

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class CulinkUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'muskers.change_culink'
    template_name = 'muskers/edit.html'
    model = Culink
    form_class = CulinkForm
    slug_field = "shortlink_text"

    def has_permission(self):
        culink_obj = self.get_object()

        if self.request.user == culink_obj.owner:
            perms = self.get_permission_required()
            return self.request.user.has_perms(perms)
        else:
            return False


@method_decorator(login_required, name='dispatch')
class CulinkDeleteView(DeleteView):
    template_name = 'muskers/delete.html'
    model = Culink
    success_url = reverse_lazy('muskers:shorts')
    slug_field = "shortlink_text"


@method_decorator(login_required, name='dispatch')
class ResultsView(ListView):
    template_name = 'muskers/shorts.html'
    model = Culink

    def get_context_data(self):
        culinks = Culink.objects.filter(owner=self.request.user)
        culinksDesc = culinks.order_by('-creation_date')

        paginator = Paginator(culinksDesc, 15)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'page_obj': page_obj}

        return context


@method_decorator(login_required, name='dispatch')
class CulinkDetailsView(DetailView):
    template_name = 'muskers/charts.html'

    def get(self, request, slug):
        culink = get_object_or_404(Culink, shortlink_text=slug, owner=request.user)
        culinkStats = CulinkStats.objects.filter(culink=culink)
        context = {'culink': culink, 'qs': culinkStats}

        return render(request, 'muskers/charts.html', context)


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('shortener:index'))


class UserCreateView(CreateView):
    template_name = 'muskers/register.html'
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('muskers:user')

    def get_success_url(self):
        user = self.object

        user_content_type = ContentType.objects.get_for_model(User)
        user_perms = Permission.objects.filter(content_type=user_content_type)
        culink_content_type = ContentType.objects.get_for_model(Culink)
        culink_perms = Permission.objects.filter(content_type=culink_content_type)
        view_culinkstats_perm = Permission.objects.get(codename='view_culinkstats')
        add_user_perm = Permission.objects.get(codename='add_user')

        for perm in user_perms:
            user.user_permissions.add(perm)
        for perm in culink_perms:
            user.user_permissions.add(perm)

        user.user_permissions.add(view_culinkstats_perm)
        user.user_permissions.remove(add_user_perm)

        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return str(self.success_url)


@method_decorator(login_required, name='dispatch')
class UserUpdateView(DetailView):
    template_name = 'muskers/settings.html'

    def get(self, request):
        return render(request, 'muskers/settings.html')


@method_decorator(login_required, name='dispatch')
class UserPasswordView(PasswordChangeView):
    template_name = 'muskers/password.html'
    form_class = PasswordForm
    success_url = reverse_lazy('muskers:settings')


@method_decorator(login_required, name='dispatch')
class UserDeleteView(DeleteView):
    template_name = 'muskers/delete_user.html'
    model = User
    success_url = reverse_lazy('muskers:index')
    slug_field = "username"
