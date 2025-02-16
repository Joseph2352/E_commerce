from django.views.generic import TemplateView
from django.utils.timezone import now

from produits.models import Produits,Categorys

class HomeViews(TemplateView):
    template_name='E_commerce/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Categorys.objects.all()
        context['categories_produits'] = {categorie: Produits.objects.filter(category=categorie) for categorie in categories}

        context['static_version'] = now().timestamp()
        
        return context


        