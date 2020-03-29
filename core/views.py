from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
# Create your views here.

class StaffRequiredMixin(object):
    """
        Required user is member of staff.
    """
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        #if not request.user.is_staff:
        #    return redirect( reverse_lazy('admin:login') )
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

class HomePageView(TemplateView):

    template_name = "core/home.html"

    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Inicio"
        return context
    """
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': "Inicio"})

class SamplePageView(TemplateView):

    template_name = "core/sample.html"