
from braces.views import LoginRequiredMixin
from django.views.generic import ListView
from django_tables2 import RequestConfig
from django.db.models import Q
from projects.models import Research, ProjectType, Specie, Institute, EventType, Equipment
from constants.constants import Constants
from operator import attrgetter
from projects.tables import ResearchTable, InstituteTable, EventTypeTable, SpecieTable, ProjectTypeTable, EquipmentTable
import logging

logger_debug = logging.getLogger("project_manager.debug")
logger_production = logging.getLogger("project_manager.production")

class SettingsResearchView(LoginRequiredMixin, ListView):
	"""
	Several definitions: 
		1) Event type
		2) Project type
		3) Species
		4) Clients
		5) Institute
	"""
	model = Research
	template_name = 'settings/settings_research.html'
	context_object_name = 'research'
	ordering = ['name']
	
	def get_context_data(self, **kwargs):
		context = super(SettingsResearchView, self).get_context_data(**kwargs)
		
		tag_search = 'search_research'
		query_set = Research.objects.all()
		if (not self.request.GET.get(tag_search) is None and self.request.GET.get(tag_search)): 
			query_set = query_set.filter( Q(name__icontains=self.request.GET.get(tag_search)) |\
										Q(email__icontains=self.request.GET.get(tag_search)) |\
										Q(phone__icontains=self.request.GET.get(tag_search)) )
		
		### only order here because the field is encrypted
		query_set_result = sorted(query_set, key=attrgetter('name'))
		table = ResearchTable(query_set_result)
		RequestConfig(self.request, paginate={'per_page': Constants.PAGINATE_NUMBER_SETTINGS}).configure(table)
		if (not self.request.GET.get(tag_search) is None): context[tag_search] = self.request.GET.get(tag_search)
		context['table'] = table
		context['nav_settings_research'] = True
		context['nav_settings'] = True
		context['is_super_user'] = self.request.user.is_superuser
		context['is_active'] = self.request.user.is_active
		context['show_paginatior'] = len(query_set_result) > Constants.PAGINATE_NUMBER_SETTINGS
		return context


class SettingsInstituteView(LoginRequiredMixin, ListView):
	"""
	Several definitions: 
		1) Event type
		2) Project type
		3) Species
		4) Clients
		5) Institute
	"""
	model = Institute
	template_name = 'settings/settings_institute.html'
	context_object_name = 'institute'
	ordering = ['name']
	
	def get_context_data(self, **kwargs):
		context = super(SettingsInstituteView, self).get_context_data(**kwargs)
		
		tag_search = 'search_institute'
		query_set = Institute.objects.all()
		if (not self.request.GET.get(tag_search) is None and self.request.GET.get(tag_search)): 
			query_set = query_set.filter( Q(name__icontains=self.request.GET.get(tag_search)) |\
										Q(abbreviation__icontains=self.request.GET.get(tag_search)) |\
										Q(city__icontains=self.request.GET.get(tag_search)) )
		
		query_set_result = sorted(query_set, key=attrgetter('name'))
		table = InstituteTable(query_set_result)
		RequestConfig(self.request, paginate={'per_page': Constants.PAGINATE_NUMBER_SETTINGS}).configure(table)
		if (not self.request.GET.get(tag_search) is None): context[tag_search] = self.request.GET.get(tag_search)
		context['table'] = table
		context['nav_settings_institute'] = True
		context['nav_settings'] = True
		context['is_super_user'] = self.request.user.is_superuser
		context['is_active'] = self.request.user.is_active
		context['show_paginatior'] = len(query_set_result) > Constants.PAGINATE_NUMBER_SETTINGS
		return context

class SettingsSpecieView(LoginRequiredMixin, ListView):
	"""
	Several definitions: 
		1) Event type
		2) Project type
		3) Species
		4) Clients
		5) Institute
	"""
	model = Specie
	template_name = 'settings/settings_specie.html'
	context_object_name = 'specie'
	ordering = ['name']
	
	def get_context_data(self, **kwargs):
		context = super(SettingsSpecieView, self).get_context_data(**kwargs)
		
		tag_search = 'search_specie'
		query_set = Specie.objects.all()
		if (self.request.GET.get(tag_search) != None and self.request.GET.get(tag_search)): 
			query_set = query_set.filter( Q(name__icontains=self.request.GET.get(tag_search)) )
		
		### only order here because the field is encrypted
		query_set_result = sorted(query_set, key=attrgetter('name'))
		table = SpecieTable(query_set_result)
		RequestConfig(self.request, paginate={'per_page': Constants.PAGINATE_NUMBER_SETTINGS}).configure(table)
		if (not self.request.GET.get(tag_search) is None): context[tag_search] = self.request.GET.get(tag_search)
		context['table'] = table
		context['nav_settings_specie'] = True
		context['nav_settings'] = True
		context['is_super_user'] = self.request.user.is_superuser
		context['is_active'] = self.request.user.is_active
		context['show_paginatior'] = len(query_set_result) > Constants.PAGINATE_NUMBER_SETTINGS
		return context


class SettingsProjectTypeView(LoginRequiredMixin, ListView):
	"""
	Several definitions: 
		1) Event type
		2) Project type
		3) Species
		4) Clients
		5) Institute
	"""
	model = ProjectType
	template_name = 'settings/settings_project_type.html'
	context_object_name = 'projecttype'
	ordering = ['name']
	
	def get_context_data(self, **kwargs):
		context = super(SettingsProjectTypeView, self).get_context_data(**kwargs)
		
		tag_search = 'search_project_type'
		query_set = ProjectType.objects.all()
		if (not self.request.GET.get(tag_search) is None and self.request.GET.get(tag_search)): 
			query_set = query_set.filter( Q(name__icontains=self.request.GET.get(tag_search)) )
		
		### only order here because the field is encrypted
		query_set_result = sorted(query_set, key=attrgetter('name'))
		table = ProjectTypeTable(query_set_result)
		RequestConfig(self.request, paginate={'per_page': Constants.PAGINATE_NUMBER_SETTINGS}).configure(table)
		if (not self.request.GET.get(tag_search) is None): context[tag_search] = self.request.GET.get(tag_search)
		context['table'] = table
		context['nav_settings_project_type'] = True
		context['nav_settings'] = True
		context['is_super_user'] = self.request.user.is_superuser
		context['is_active'] = self.request.user.is_active
		context['show_paginatior'] = len(query_set_result) > Constants.PAGINATE_NUMBER_SETTINGS
		return context


class SettingsEventTypeView(LoginRequiredMixin, ListView):
	"""
	Several definitions: 
		1) Event type
		2) Project type
		3) Species
		4) Clients
		5) Institute
	"""
	model = EventType
	template_name = 'settings/settings_event_type.html'
	context_object_name = 'eventtype'
	ordering = ['name']
	
	def get_context_data(self, **kwargs):
		context = super(SettingsEventTypeView, self).get_context_data(**kwargs)
		
		tag_search = 'search_event_type'
		query_set = EventType.objects.all()
		if (not self.request.GET.get(tag_search) is None and self.request.GET.get(tag_search)): 
			query_set = query_set.filter( Q(name__icontains=self.request.GET.get(tag_search)) )
		
		query_set_result = sorted(query_set, key=attrgetter('name'))
		table = EventTypeTable(query_set_result)
		RequestConfig(self.request, paginate={'per_page': Constants.PAGINATE_NUMBER_SETTINGS}).configure(table)
		if (not self.request.GET.get(tag_search) is None): context[tag_search] = self.request.GET.get(tag_search)
		context['table'] = table
		context['nav_settings_event_type'] = True
		context['nav_settings'] = True
		context['is_super_user'] = self.request.user.is_superuser
		context['is_active'] = self.request.user.is_active
		context['show_paginatior'] = len(query_set_result) > Constants.PAGINATE_NUMBER_SETTINGS
		return context


class SettingsEquipmentView(LoginRequiredMixin, ListView):
	"""
	Several definitions: 
		1) Event type
		2) Project type
		3) Species
		4) Clients
		5) Institute
		5) Equipments
	"""
	model = Equipment
	template_name = 'settings/settings_equipment.html'
	context_object_name = 'equipment'
	ordering = ['name']
	
	def get_context_data(self, **kwargs):
		context = super(SettingsEquipmentView, self).get_context_data(**kwargs)
		
		tag_search = 'search_equipment'
		query_set = Equipment.objects.all()
		if (not self.request.GET.get(tag_search) is None and self.request.GET.get(tag_search)): 
			query_set = query_set.filter( Q(name__icontains=self.request.GET.get(tag_search)) )
		
		query_set_result = sorted(query_set, key=attrgetter('name'))
		table = EquipmentTable(query_set_result)
		RequestConfig(self.request, paginate={'per_page': Constants.PAGINATE_NUMBER_SETTINGS}).configure(table)
		if (not self.request.GET.get(tag_search) is None): context[tag_search] = self.request.GET.get(tag_search)
		context['table'] = table
		context['nav_settings_equipments'] = True
		context['nav_settings'] = True
		context['is_super_user'] = self.request.user.is_superuser
		context['is_active'] = self.request.user.is_active
		context['show_paginatior'] = len(query_set_result) > Constants.PAGINATE_NUMBER_SETTINGS
		return context

