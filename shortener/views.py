import datetime

from random import randrange

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages

from django.forms import URLField
from django.core.exceptions import ValidationError

from muskers.models import Culink, CulinkStats
from muskers.forms import CulinkOneForm, CulinkCheckOneForm


class IndexView(FormView):
    template_name = 'shortener/index.html'
    form_class = CulinkOneForm
    success_url = '/'

    def shorten_link(self, longl):
        rand = randrange(1000, 9999)
        shortl = longl[13] + longl[-2] + str(rand)

        while True:
            if not Culink.objects.filter(shortlink_text=shortl).exists():
                break
            else:
                rand = randrange(1000, 9999)
                shortl = longl[13] + longl[-2] + str(rand)

        ndate = timezone.now() + datetime.timedelta(weeks=2)
        new_entry = Culink.objects.create(longlink_text=longl, shortlink_text=shortl, expiration_date=ndate)

        messages.add_message(self.request, messages.INFO, f'Your shortcut: {shortl}')

        return new_entry.shortlink_text

    def form_valid(self, form):
        longl = self.request.POST['longlink_text']

        self.shorten_link(longl)

        return super().form_valid(form)


class AboutView(DetailView):
    template_name = 'shortener/about.html'

    def get(self, request):
        return render(request, 'shortener/about.html')


def add_stats(culink):
    try:
        culinkStats = CulinkStats.objects.get(culink=culink, creation_day=datetime.date.today())
    except CulinkStats.DoesNotExist:
        culinkStats = CulinkStats.objects.create(culink=culink)

    culinkStats.redirections += 1
    culinkStats.save()


def redirect_to(request, shortlink):
    try:
        culink = Culink.objects.get(shortlink_text=shortlink)
    except Culink.DoesNotExist:
        messages.add_message(request, messages.INFO, 'This shortcut does not exists!')
        return HttpResponseRedirect(reverse('shortener:index'))
    else:
        link = culink.longlink_text

        if culink.expiration_date is not None:
            if timezone.now() <= culink.expiration_date:
                add_stats(culink)
                return HttpResponseRedirect(link)
            else:
                messages.add_message(request, messages.INFO, 'This shortcut has expired!')
                return HttpResponseRedirect(reverse('shortener:index'))
        else:
            add_stats(culink)
            return HttpResponseRedirect(link)


def check_link(request, shortlink):
    try:
        culink = Culink.objects.get(shortlink_text=shortlink)
    except Culink.DoesNotExist:
        messages.add_message(request, messages.INFO, 'This shortcut does not exists!')
        return HttpResponseRedirect(reverse('shortener:index'))
    else:
        link = culink.longlink_text

        messages.add_message(request, messages.INFO, f'This shortcut redirects to: {link}')
        return HttpResponseRedirect(reverse('shortener:index'))
