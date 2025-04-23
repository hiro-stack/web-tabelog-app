from django.shortcuts import render, get_object_or_404, redirect

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


class TabelogIndexView(View):

    def get(self, request):
        return render(request, "tabelob/index.html")


tabelog_index = TabelogIndexView.as_view()
