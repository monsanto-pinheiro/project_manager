from braces.views import LoginRequiredMixin, FormValidMessageMixin
from django.views.generic import ListView
from django.db.models import Q
from .models import Pipeline
from .tables import PipelineTable
from operator import attrgetter
from constants.constants import Constants
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib import messages
from django_tables2 import RequestConfig
from django.template.defaultfilters import filesizeformat
import ntpath, os, logging, sys

# Create your views here.

logger_debug = logging.getLogger("project_manager.debug")
logger_production = logging.getLogger("project_manager.production")

class PipelinesView(LoginRequiredMixin, ListView):
	model = Pipeline
	template_name = 'pipelines/pipelines_list.html'
	context_object_name = 'projects'
	ordering = ['id']
	
	def get_context_data(self, **kwargs):
		context = super(PipelinesView, self).get_context_data(**kwargs)
		
		tag_search = 'search_pipelines'
		query_set = Pipeline.objects.filter(is_deleted=False).order_by('-creation_date')
		if (self.request.GET.get(tag_search) != None and self.request.GET.get(tag_search)): 
			query_set = query_set.filter( Q(research__name__icontains=self.request.GET.get(tag_search)) |\
										Q(owner__username__icontains=self.request.GET.get(tag_search)) |\
										Q(reference__icontains=self.request.GET.get(tag_search)) )
		
		query_set_result = sorted(query_set, key=attrgetter('creation_date'), reverse=True)
		table = PipelineTable(query_set_result)
		
		RequestConfig(self.request, paginate={'per_page': Constants.PAGINATE_NUMBER}).configure(table)
		if (self.request.GET.get(tag_search) != None): context[tag_search] = self.request.GET.get(tag_search)
		context['table'] = table
		context['nav_pipelines'] = True
		context['is_super_user'] = self.request.user.is_superuser
		context['is_active'] = self.request.user.is_active
		context['show_paginatior'] = len(query_set_result) > Constants.PAGINATE_NUMBER
		return context