
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy

class AboutView(View):
    success_url = reverse_lazy('index')
    permission_required = []

    def get(self, request, *args, **kwargs):
        if request.path == '/about/features':
            return render(request, 'others/features.html')
        if request.path == '/about/resources':
            return render(request, 'others/resources.html')
        if request.path == '/about/terms':
            return render(request, 'others/terms.html')
        if request.path == '/about/privacy':
            return render(request, 'others/privacy.html')
        return render(request, 'others/about.html')