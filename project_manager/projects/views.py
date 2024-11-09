
from braces.views import LoginRequiredMixin, FormValidMessageMixin
from django.views.generic import ListView, FormView, UpdateView, DetailView
from django_tables2 import RequestConfig
from projects.models import Project, Research, ProjectType, Specie, Institute, Event, EventType, File
from projects.models import PersonInEvent, Equipment, EquipmentInEvent
from django.db.models import Q
from operator import attrgetter
from constants.constants import Constants
from constants.meta_key_values import MetaKeyAndValue
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.contrib import messages
from django.template.defaultfilters import filesizeformat
from django.http import JsonResponse
from projects.tables import ProjectTable, ProjectEventsTable, FilesEventTable, ManPowerEventTable, EquipmentEventTable
from projects.forms import ProjectForm, EventForm, EventUpdateForm, EquipmentForm
from projects.manage_database import ManageDatabase
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView
from .forms import ResearchForm, ProjectTypeForm, SpecieForm, InstituteForm, EventTypeForm, UploadMultipleFilesForm, ManPowerForm, EquipmentEventForm
from utils.lock_atomic_transaction import LockedAtomicTransaction
from django.conf import settings
from django.utils.safestring import mark_safe
from utils.utils import Utils
import ntpath, os, logging, sys


logger_debug = logging.getLogger("project_manager.debug")
logger_production = logging.getLogger("project_manager.production")

class ProjectView(LoginRequiredMixin, ListView):
	model = Project
	template_name = 'projects/projects.html'
	context_object_name = 'projects'
	ordering = ['id']
	
	def get_context_data(self, **kwargs):
		context = super(ProjectView, self).get_context_data(**kwargs)
		
		tag_search = 'search_projects'
		query_set = Project.objects.filter(is_deleted=False)
		if (self.request.GET.get(tag_search) != None and self.request.GET.get(tag_search)): 
			query_set = query_set.filter( Q(research__name__icontains=self.request.GET.get(tag_search)) |\
										Q(owner__username__icontains=self.request.GET.get(tag_search)) |\
										Q(reference__icontains=self.request.GET.get(tag_search)) )
		
		query_set_result = sorted(query_set, key=attrgetter('start_date', 'id'), reverse=True)
		table = ProjectTable(query_set_result)
		
		RequestConfig(self.request, paginate={'per_page': Constants.PAGINATE_NUMBER}).configure(table)
		if (self.request.GET.get(tag_search) != None): context[tag_search] = self.request.GET.get(tag_search)
		context['table'] = table
		context['nav_projets'] = True
		context['is_super_user'] = self.request.user.is_superuser
		context['is_active'] = self.request.user.is_active
		context['show_paginatior'] = len(query_set_result) > Constants.PAGINATE_NUMBER
		return context

	
class ProjectAddView(LoginRequiredMixin, FormValidMessageMixin, FormView):
	"""
	Create a new reference
	"""
	form_class = ProjectForm
	success_url = reverse_lazy('projects')
	template_name = 'projects/project_add.html'

	## Other solution to get the reference
	## https://pypi.python.org/pypi?%3aaction=display&name=django-contrib-requestprovider&version=1.0.1
	def get_form_kwargs(self):
		"""
		Set the request to pass in the form
		"""
		kw = super(ProjectAddView, self).get_form_kwargs()
		kw['request'] = self.request # the trick!
		return kw
	
	
	def get_context_data(self, **kwargs):
		context = super(ProjectAddView, self).get_context_data(**kwargs)
		context['nav_projets'] = True
		context['is_super_user'] = self.request.user.is_superuser
		context['is_active'] = self.request.user.is_active
		context['source_pk'] = ""		## only for code improved..., use din update project, when rever_lazy from model django form
										
		context['edit_remove_projects_type'] = True if ProjectType.objects.exclude(name__isnull=True).count() > 0 else False
		context['edit_remove_research'] = True if Research.objects.exclude(name__isnull=True).count() > 0 else False
		context['edit_remove_specie'] = True if Specie.objects.exclude(name__isnull=True).count() > 0 else False
		context['edit_remove_institute'] = True if Institute.objects.exclude(name__isnull=True).count() > 0 else False
		return context
	
	def form_valid(self, form):
		
		### test anonymous account
		if (not self.request.user.is_superuser or not self.request.user.is_active):
			messages.warning(self.request, "'{}' account can not create projects.".format(self.request.user.username), fail_silently=True)
			return super(ProjectAddView, self).form_invalid(form)

		## save it...
		with LockedAtomicTransaction(Project):
			project = form.save(commit=False)
			project.reference = project.get_project_reference()
			project.owner = self.request.user
			project.save()
			
			### set the possible update from the previous
			manage_database = ManageDatabase()
			manage_database.set_project_metakey(project, self.request.user,\
				MetaKeyAndValue.META_KEY_project_create, MetaKeyAndValue.META_VALUE_Success,
				project.to_json())

		messages.success(self.request, "Project '" + project.reference + "' was created successfully", fail_silently=True)
		return super(ProjectAddView, self).form_valid(form)

	## static method, not need for now.
	form_valid_message = ""		## need to have this

class ProjectUpdateView(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
	"""
	Create a new reference
	"""
	model = Project
	form_class = ProjectForm
	success_url = reverse_lazy('projects')
	template_name = 'projects/project_update.html'

	## Other solution to get the reference
	## https://pypi.python.org/pypi?%3aaction=display&name=django-contrib-requestprovider&version=1.0.1
	def get_form_kwargs(self):
		"""
		Set the request to pass in the form
		"""
		kw = super(ProjectUpdateView, self).get_form_kwargs()
		kw['request'] = self.request # the trick!
		return kw
	
	def get_context_data(self, **kwargs):
		context = super(ProjectUpdateView, self).get_context_data(**kwargs)
		context['nav_projets'] = True
		context['is_super_user'] = self.request.user.is_superuser
		context['is_active'] = self.request.user.is_active
		context['source_pk'] = self.kwargs['pk']	## with this, is possible to pass the pk_project, to include in rever_lazy in django-update-forms
		
		context['edit_remove_projects_type'] = True if ProjectType.objects.exclude(name__isnull=True).count() > 0 else False
		context['edit_remove_research'] = True if Research.objects.exclude(name__isnull=True).count() > 0 else False
		context['edit_remove_specie'] = True if Specie.objects.exclude(name__isnull=True).count() > 0 else False
		context['edit_remove_institute'] = True if Institute.objects.exclude(name__isnull=True).count() > 0 else False

		### if it's possible to change event type
	##	context['possible_to_change_projects_type'] = Event.objects.filter(project__id=self.kwargs['pk'], is_deleted = False).count() == 0
		context['possible_to_change_projects_type'] = True
		return context
	
	def form_valid(self, form):
		
		### test anonymous account
		if (not self.request.user.is_superuser or not self.request.user.is_active):
			messages.warning(self.request, "'{}' account can not update projects.".format(self.request.user.username), fail_silently=True)
			return super(ProjectUpdateView, self).form_invalid(form)

		## save it...
		if (not self.request.is_ajax()):
			with transaction.atomic():
				project = form.save(commit=False)
				project.reference = project.get_project_reference()		### can change the type of project
				## project.owner = self.request.user					###
				project.save()
	
				### set the possible update from the previous
				manage_database = ManageDatabase()
				manage_database.set_project_metakey(project, self.request.user,\
					MetaKeyAndValue.META_KEY_project_update, MetaKeyAndValue.META_VALUE_Success,
					project.to_json())
			
		messages.success(self.request, "Project '" + project.reference + "' was updated successfully", fail_silently=True)
		return super(ProjectUpdateView, self).form_valid(form)

	## static method, not need for now.
	form_valid_message = ""		## need to have this

###############################################
## Research
class ResearchCreateView(BSModalCreateView):
	template_name = 'modal_forms/create_research.html'
	form_class = ResearchForm
	success_message = 'Success: Research was created.'
#	success_url = reverse_lazy('project-add')

	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		reverse = self.request.POST.get("reverse", "")
		### you can add reverse attribute in the javascript 
		if (len(reverse) > 0):
			if (len(project_pk) == 0): return reverse_lazy(reverse)
			return reverse_lazy(reverse, kwargs={'pk': project_pk})
		
		if (len(project_pk) == 0): return reverse_lazy('project-add')
		return reverse_lazy('project-update', kwargs={'pk': project_pk})

	def form_valid(self, form):
		
		## set create owner
		if (not self.request.is_ajax()):
			form.instance.owner = self.request.user
		return super(ResearchCreateView, self).form_valid(form)

class ResearchUpdateView(BSModalUpdateView):
	model = Research
	template_name = 'modal_forms/update_research.html'
	form_class = ResearchForm
	success_message = 'Success: Research was updated.'
#	success_url = reverse_lazy('project-add')
	
	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		reverse = self.request.POST.get("reverse", "")
		### you can add reverse attribute in the javascript 
		if (len(reverse) > 0):
			if (len(project_pk) == 0): return reverse_lazy(reverse)
			return reverse_lazy(reverse, kwargs={'pk': project_pk})
		
		if (len(project_pk) == 0): return reverse_lazy('project-add')
		return reverse_lazy('project-update', kwargs={'pk': project_pk})


class ResearchDeleteView(BSModalDeleteView):
	model = Research
	form_class = ResearchForm
	template_name = 'modal_forms/delete_research.html'
	success_message = 'Success: Research was deleted.'
#	success_url = reverse_lazy('project-add')

	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		if (len(project_pk) == 0): return reverse_lazy('project-add')
		return reverse_lazy('project-update', kwargs={'pk': project_pk})

###############################################
### Project type
class ProjectTypeCreateView(BSModalCreateView):
	template_name = 'modal_forms/create_project_type.html'
	form_class = ProjectTypeForm
	success_message = 'Success: Project type was created.'
#	success_url = reverse_lazy('project-add')

	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		reverse = self.request.POST.get("reverse", "")
		### you can add reverse attribute in the javascript 
		if (len(reverse) > 0):
			if (len(project_pk) == 0): return reverse_lazy(reverse)
			return reverse_lazy(reverse, kwargs={'pk': project_pk})
		
		if (len(project_pk) == 0): return reverse_lazy('project-add')
		return reverse_lazy('project-update', kwargs={'pk': project_pk})
	
	def form_valid(self, form):
		if (not self.request.is_ajax()):
			form.instance.owner = self.request.user
		return super(ProjectTypeCreateView, self).form_valid(form)
	form_valid_message = ""		## need to have this

class ProjectTypeUpdateView(BSModalUpdateView):
	model = ProjectType
	template_name = 'modal_forms/update_project_type.html'
	form_class = ProjectTypeForm
	success_message = 'Success: Project type was updated.'
#	success_url = reverse_lazy('project-add')

	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		reverse = self.request.POST.get("reverse", "")
		### you can add reverse attribute in the javascript 
		if (len(reverse) > 0):
			if (len(project_pk) == 0): return reverse_lazy(reverse)
			return reverse_lazy(reverse, kwargs={'pk': project_pk})
		
		if (len(project_pk) == 0): return reverse_lazy('project-add')
		return reverse_lazy('project-update', kwargs={'pk': project_pk})
	
class ProjectTypeDeleteView(BSModalDeleteView):
	model = ProjectType
	template_name = 'modal_forms/delete_project_type.html'
	success_message = 'Success: Project type was deleted.'
#	success_url = reverse_lazy('project-add')
	
	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		if (len(project_pk) == 0): return reverse_lazy('project-add')
		return reverse_lazy('project-update', kwargs={'pk': project_pk})
	
###############################################
### Specie
class SpecieCreateView(BSModalCreateView):
	template_name = 'modal_forms/create_specie.html'
	form_class = SpecieForm
	success_message = 'Success: Specie was created.'
#	success_url = reverse_lazy('project-add')

	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		reverse = self.request.POST.get("reverse", "")
		### you can add reverse attribute in the javascript 
		if (len(reverse) > 0):
			if (len(project_pk) == 0): return reverse_lazy(reverse)
			return reverse_lazy(reverse, kwargs={'pk': project_pk})
		
		if (len(project_pk) == 0): return reverse_lazy('project-add')
		return reverse_lazy('project-update', kwargs={'pk': project_pk})
	
	def form_valid(self, form):
		if (not self.request.is_ajax()):
			form.instance.owner = self.request.user
		return super(SpecieCreateView, self).form_valid(form)
	form_valid_message = ""		## need to have this

class SpecieUpdateView(BSModalUpdateView):
	model = Specie
	template_name = 'modal_forms/update_specie.html'
	form_class = SpecieForm
	success_message = 'Success: Specie was updated.'
#	success_url = reverse_lazy('project-add')

	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		reverse = self.request.POST.get("reverse", "")
		### you can add reverse attribute in the javascript 
		if (len(reverse) > 0):
			if (len(project_pk) == 0): return reverse_lazy(reverse)
			return reverse_lazy(reverse, kwargs={'pk': project_pk})
		
		if (len(project_pk) == 0): return reverse_lazy('project-add')
		return reverse_lazy('project-update', kwargs={'pk': project_pk})
	
class SpecieDeleteView(BSModalDeleteView):
	model = Specie
	template_name = 'modal_forms/delete_specie.html'
	success_message = 'Success: Specie was deleted.'
#	success_url = reverse_lazy('project-add')
	
	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		if (len(project_pk) == 0): return reverse_lazy('project-add')
		return reverse_lazy('project-update', kwargs={'pk': project_pk})

###############################################
### Institute
class InstituteCreateView(BSModalCreateView):
	template_name = 'modal_forms/create_institute.html'
	form_class = InstituteForm
	success_message = 'Success: Institute was created.'
#	success_url = reverse_lazy('project-add')

	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		reverse = self.request.POST.get("reverse", "")
		### you can add reverse attribute in the javascript 
		if (len(reverse) > 0):
			if (len(project_pk) == 0): return reverse_lazy(reverse)
			return reverse_lazy(reverse, kwargs={'pk': project_pk})
		
		if (len(project_pk) == 0): return reverse_lazy('project-add')
		return reverse_lazy('project-update', kwargs={'pk': project_pk})
	
	def form_valid(self, form):
		if (not self.request.is_ajax()):
			form.instance.owner = self.request.user
		return super(InstituteCreateView, self).form_valid(form)
	form_valid_message = ""		## need to have this

class InstituteUpdateView(BSModalUpdateView):
	model = Institute
	template_name = 'modal_forms/update_institute.html'
	form_class = InstituteForm
	success_message = 'Success: Institute was updated.'
#	success_url = reverse_lazy('project-add')

	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		reverse = self.request.POST.get("reverse", "")
		### you can add reverse attribute in the javascript 
		if (len(reverse) > 0):
			if (len(project_pk) == 0): return reverse_lazy(reverse)
			return reverse_lazy(reverse, kwargs={'pk': project_pk})
		
		if (len(project_pk) == 0): return reverse_lazy('project-add')
		return reverse_lazy('project-update', kwargs={'pk': project_pk})

class InstituteDeleteView(BSModalDeleteView):
	model = Institute
	template_name = 'modal_forms/delete_institute.html'
	success_message = 'Success: Institute was deleted.'
#	success_url = reverse_lazy('project-add')

	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		if (len(project_pk) == 0): return reverse_lazy('project-add')
		return reverse_lazy('project-update', kwargs={'pk': project_pk})
	
###############################################
### EventType
class EventTypeCreateView(BSModalCreateView):
	template_name = 'modal_forms/create_event_type.html'
	form_class = EventTypeForm
	success_message = 'Success: Event type was created.'
#	success_url = reverse_lazy('event-add')

	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		reverse = self.request.POST.get("reverse", "")
		### you can add reverse attribute in the javascript 
		if (len(reverse) > 0):
			if (len(project_pk) == 0): return reverse_lazy(reverse)
			return reverse_lazy(reverse, kwargs={'pk': project_pk})
		
		if (len(project_pk) == 0): return reverse_lazy('event-add')
		return reverse_lazy('event-add', kwargs={'pk': project_pk})
	
	def form_valid(self, form):
		if (not self.request.is_ajax()):
			form.instance.owner = self.request.user
		return super(EventTypeCreateView, self).form_valid(form)
	form_valid_message = ""		## need to have this

class EventTypeUpdateView(BSModalUpdateView):
	model = EventType
	template_name = 'modal_forms/update_event_type.html'
	form_class = EventTypeForm
	success_message = 'Success: Event type was updated.'
#	success_url = reverse_lazy('event-add')

	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		reverse = self.request.POST.get("reverse", "")
		### you can add reverse attribute in the javascript 
		if (len(reverse) > 0):
			if (len(project_pk) == 0): return reverse_lazy(reverse)
			return reverse_lazy(reverse, kwargs={'pk': project_pk})
		
		if (len(project_pk) == 0): return reverse_lazy('event-add')
		return reverse_lazy('event-add', kwargs={'pk': project_pk})
	
class EventTypeDeleteView(BSModalDeleteView):
	model = EventType
	template_name = 'modal_forms/delete_event_type.html'
	success_message = 'Success: Event type was deleted.'
#	success_url = reverse_lazy('event-add')
	
	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		if (len(project_pk) == 0): return reverse_lazy('event-add')
		return reverse_lazy('event-add', kwargs={'pk': project_pk})

###############################################
### Equipment
class EquipmentCreateView(BSModalCreateView):
	template_name = 'modal_forms/create_equipment.html'
	form_class = EquipmentForm
	success_message = 'Success: Equipment was created.'
#	success_url = reverse_lazy('settings-equipment')

	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		reverse = self.request.POST.get("reverse", "")
		### you can add reverse attribute in the javascript 
		if (len(reverse) > 0):
			if (len(project_pk) == 0): return reverse_lazy(reverse)
			return reverse_lazy(reverse, kwargs={'pk': project_pk})
		
		if (len(project_pk) == 0): return reverse_lazy('settings-equipment')
		return reverse_lazy('settings-equipment', kwargs={'pk': project_pk})
	
	def form_valid(self, form):
		if (not self.request.is_ajax()):
			form.instance.owner = self.request.user
		return super(EquipmentCreateView, self).form_valid(form)
	form_valid_message = ""		## need to have this

class EquipmentUpdateView(BSModalUpdateView):
	model = Equipment
	template_name = 'modal_forms/update_equipment.html'
	form_class = EquipmentForm
	success_message = 'Success: Equipment was updated.'
#	success_url = reverse_lazy('event-add')

	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		reverse = self.request.POST.get("reverse", "")
		### you can add reverse attribute in the javascript 
		if (len(reverse) > 0):
			if (len(project_pk) == 0): return reverse_lazy(reverse)
			return reverse_lazy(reverse, kwargs={'pk': project_pk})
		
		if (len(project_pk) == 0): return reverse_lazy('settings-equipment')
		return reverse_lazy('settings-equipment', kwargs={'pk': project_pk})


###############################################
### PersonInEvent
class PersonInEventCreateView(BSModalCreateView):
	template_name = 'modal_forms/create_man_power.html'
	form_class = ManPowerForm
	success_message = 'Success: Person was added to this event.'

	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		event_pk = self.request.POST.get("source_pk", "")
		if (len(event_pk) == 0): return reverse_lazy('event-view')
		return reverse_lazy('event-view', kwargs={'pk': event_pk, 'tab_item': 'tab_workforce'})
	
	def form_valid(self, form):
		
		## First POST is to test if all fields are correct (form_isvalid()). Only save the data in second POST
		if (not self.request.is_ajax()):
			with LockedAtomicTransaction(PersonInEvent), LockedAtomicTransaction(Project):
				person_in_event = form.save(commit=False)
				person_in_event.owner = self.request.user
				person_in_event.event = Event.objects.get(id=self.request.POST.get("source_pk", "")) 
				person_in_event.save()
				
				### set the possible update from the previous
				manage_database = ManageDatabase()
				manage_database.set_person_in_event_metakey(person_in_event, self.request.user,\
					MetaKeyAndValue.META_KEY_person_in_event_create, MetaKeyAndValue.META_VALUE_Success,
					person_in_event.to_json())
			
				### update time and people in the project
				project = Project.objects.get(id=person_in_event.event.project.id)
				project.update_people_and_time()

		return super(PersonInEventCreateView, self).form_valid(form)
	
	form_valid_message = ""		## need to have this


class PersonInEventUpdateView(BSModalUpdateView):
	model = PersonInEvent
	template_name = 'modal_forms/update_man_power.html'
	form_class = ManPowerForm
	success_message = 'Success: Person for this event was updated.'

	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		if (len(project_pk) == 0): return reverse_lazy('event-view')
		return reverse_lazy('event-view', kwargs={'pk': project_pk, 'tab_item': 'tab_workforce'})
	
	def form_valid(self, form):
		## First POST is to test if all fields are correct. Only save the data in second POST
		if (not self.request.is_ajax()):
			with LockedAtomicTransaction(PersonInEvent), LockedAtomicTransaction(Project):
				person_in_event = form.save(commit=False)
				person_in_event.save()
				
				### set the possible update from the previous
				manage_database = ManageDatabase()
				manage_database.set_person_in_event_metakey(person_in_event, self.request.user,\
					MetaKeyAndValue.META_KEY_person_in_event_update, MetaKeyAndValue.META_VALUE_Success,
					person_in_event.to_json())
			
				### update time and people in the project
				project = Project.objects.get(id=person_in_event.event.project.id)
				project.update_people_and_time()

		return super(PersonInEventUpdateView, self).form_valid(form)

class PersonInEventView(BSModalUpdateView):
	model = PersonInEvent
	template_name = 'modal_forms/view_man_power.html'
	form_class = ManPowerForm
	success_message = 'Success: Person for this event was updated.'

	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		if (len(project_pk) == 0): return reverse_lazy('event-view')
		return reverse_lazy('event-view', kwargs={'pk': project_pk, 'tab_item': 'tab_workforce'})
	

	
class PersonInEventDeleteView(BSModalDeleteView):
	model = PersonInEvent
	template_name = 'modal_forms/delete_man_power.html'
	success_message = 'Success: Person was deleted for this event.'
	
	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		if (len(project_pk) == 0): return reverse_lazy('project-events')
		return reverse_lazy('project-events', kwargs={'pk': project_pk, 'tab_item': 'tab_workforce'})

###############################################
### PersonInEvent
class EquipmentInEventCreateView(BSModalCreateView):
	template_name = 'modal_forms/create_event_equipment.html'
	form_class = EquipmentEventForm
	success_message = 'Success: Equipment was added to this event.'

	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		event_pk = self.request.POST.get("source_pk", "")
		if (len(event_pk) == 0): return reverse_lazy('event-view')
		return reverse_lazy('event-view', kwargs={'pk': event_pk, 'tab_item': 'tab_equipment'})
	
	def form_valid(self, form):
		
		## First POST is to test if all fields are correct (form_isvalid()). Only save the data in second POST
		if (not self.request.is_ajax()):
			with LockedAtomicTransaction(EquipmentInEvent), LockedAtomicTransaction(Project):
				equipment_in_event = form.save(commit=False)
				equipment_in_event.owner = self.request.user
				equipment_in_event.event = Event.objects.get(id=self.request.POST.get("source_pk", "")) 
				equipment_in_event.save()
				
				### set the possible update from the previous
				manage_database = ManageDatabase()
				manage_database.set_equipment_in_event_metakey(equipment_in_event, self.request.user,\
					MetaKeyAndValue.META_KEY_equipment_in_event_create, MetaKeyAndValue.META_VALUE_Success,
					equipment_in_event.to_json())
			
				### update time and people in the project
				project = Project.objects.get(id=equipment_in_event.event.project.id)
				project.update_equipment_hours()

		return super(EquipmentInEventCreateView, self).form_valid(form)
	
	form_valid_message = ""		## need to have this


class EquipmentInEventUpdateView(BSModalUpdateView):
	model = EquipmentInEvent
	template_name = 'modal_forms/update_equipment_in_event.html'
	form_class = EquipmentEventForm
	success_message = 'Success: Equipment for this event was updated.'

	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		if (len(project_pk) == 0): return reverse_lazy('event-view')
		return reverse_lazy('event-view', kwargs={'pk': project_pk, 'tab_item': 'tab_equipment'})
	
	def form_valid(self, form):
		## First POST is to test if all fields are correct. Only save the data in second POST
		if (not self.request.is_ajax()):
			with LockedAtomicTransaction(EquipmentInEvent), LockedAtomicTransaction(Project):
				equipment_in_event = form.save(commit=False)
				equipment_in_event.save()
				
				### set the possible update from the previous
				manage_database = ManageDatabase()
				manage_database.set_equipment_in_event_metakey(equipment_in_event, self.request.user,\
					MetaKeyAndValue.META_KEY_equipment_in_event_update, MetaKeyAndValue.META_VALUE_Success,
					equipment_in_event.to_json())
			
				### update time and people in the project
				project = Project.objects.get(id=equipment_in_event.event.project.id)
				project.update_equipment_hours()

		return super(EquipmentInEventUpdateView, self).form_valid(form)

class EquipmentInEventView(BSModalUpdateView):
	model = EquipmentInEvent
	template_name = 'modal_forms/view_equipment_in_event.html'
	form_class = EquipmentEventForm
	success_message = 'Success: Equipment for this event was updated.'

	def get_success_url(self):
		"""
		get source_pk from update project, need to pass it in context
		"""
		project_pk = self.request.POST.get("source_pk", "")
		if (len(project_pk) == 0): return reverse_lazy('event-view')
		return reverse_lazy('event-view', kwargs={'pk': project_pk, 'tab_item': 'tab_equipment'})
	

###############################################
### ProjectEvent
class ProjectEventView(LoginRequiredMixin, DetailView):
	model = Project
	template_name = 'projects/projects_events.html'
	context_object_name = 'project'
	ordering = ['id']
	
	def get_context_data(self, **kwargs):
		context = super(ProjectEventView, self).get_context_data(**kwargs)
		project = kwargs['object']
		
		tag_search = 'search_events'
		query_set = Event.objects.filter(project=project, is_deleted=False).order_by('-creation_date')
		if (self.request.GET.get(tag_search) != None and self.request.GET.get(tag_search)): 
			query_set = query_set.filter( Q(event__creation_date=self.request.GET.get(tag_search)) )
		
		query_set_result = sorted(query_set, key=attrgetter('creation_date'), reverse=True)
		table = ProjectEventsTable(query_set_result)
		RequestConfig(self.request, paginate={'per_page': Constants.PAGINATE_NUMBER}).configure(table)
		if (self.request.GET.get(tag_search) != None): context[tag_search] = self.request.GET.get(tag_search)
		
		context['table'] = table
		context['nav_projets'] = True
		context['is_super_user'] = self.request.user.is_superuser
		context['is_active'] = self.request.user.is_active
		context['show_paginatior'] = len(query_set_result) > Constants.PAGINATE_NUMBER
		
		### data to show in html
		context['header_legend'] = "List all Events for project: {}".format(project.reference)
			
		## instance
		context['project'] = project
		
		### set sessions values
		self.request.session[Constants.SESSION_PROJECTS_PK_KEY] = str(project.id)
		return context


class EventAddView(LoginRequiredMixin, FormValidMessageMixin, FormView):
	"""
	Create a new reference
	https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
	https://github.com/ouhouhsami/django-progressbarupload
	"""
	form_class = EventForm
	template_name = 'event/event_add.html'
	utils = Utils()
	
	## Other solution to get the reference
	## https://pypi.python.org/pypi?%3aaction=display&name=django-contrib-requestprovider&version=1.0.1
	def get_form_kwargs(self):
		"""
		Set the request to pass in the form
		"""
		kw = super(EventAddView, self).get_form_kwargs()
		kw['request'] = self.request # the trick!
		return kw
	
	def get_success_url(self):
		return reverse_lazy('project-events', args=[self.request.session[Constants.SESSION_PROJECTS_PK_KEY]])

	def get_context_data(self, **kwargs):
		context = super(EventAddView, self).get_context_data(**kwargs)
		context['nav_projets'] = True
		context['is_super_user'] = self.request.user.is_superuser
		context['is_active'] = self.request.user.is_active
		context['source_pk'] = ""		## only for code improved..., use didnt update project, when rever_lazy from model django form
		
		### message to 
		context['message_note'] = "Maximum size per file is {}.".format(filesizeformat(settings.MAX_FILE_UPLOAD))

		context['project_pk'] = self.request.session[Constants.SESSION_PROJECTS_PK_KEY]
		context['edit_remove_events_type'] = True if EventType.objects.exclude(name__isnull=True).count() > 0 else False
		return context
	
	def form_valid(self, form):
		
		### test anonymous account
		if (not self.request.user.is_superuser or not self.request.user.is_active):
			messages.warning(self.request, "'{}' account can not create projects.".format(self.request.user.username), fail_silently=True)
			return super(EventAddView, self).form_invalid(form)
		
		## save it...
		with LockedAtomicTransaction(Event):
			event = form.save(commit=False)
			event.owner = self.request.user
			event.project_id = self.request.session[Constants.SESSION_PROJECTS_PK_KEY]
			event.save()
			
			path_to_file_partial = self.utils.get_path_to_project_event_file(
						self.request.session[Constants.SESSION_PROJECTS_PK_KEY], event.pk, self.request.user.pk)
			path_to_file = os.path.join(settings.MEDIA_ROOT, path_to_file_partial)
			### with multi upload files
			for file_memory in self.request.FILES.getlist('file_field'):
				## test directory
				if (not os.path.exists(path_to_file)): self.utils.make_path(path_to_file)
				
				### save file
				file = File()
				file_name_cleaned = self.utils.clean_name(ntpath.basename(file_memory.name))
				with open(os.path.join(path_to_file, file_name_cleaned), 'wb') as handle_write:
					handle_write.write(file_memory.read())
				file.file_name = file_name_cleaned
				file.path_name.name = os.path.join(path_to_file_partial, file_name_cleaned)
				file.hash_file = self.utils.md5sum(file.get_path_root())
				file.owner = self.request.user
				file.event = event
				file.save()
				
			### set the possible update from the previous
			manage_database = ManageDatabase()
			manage_database.set_event_metakey(event, self.request.user,\
				MetaKeyAndValue.META_KEY_event_create, MetaKeyAndValue.META_VALUE_Success,
				event.to_json())
				
				
		messages.success(self.request, "Event '" + event.event_type.name + "' was created successfully", fail_silently=True)
		return super(EventAddView, self).form_valid(form)

	## static method, not need for now.
	form_valid_message = ""		## need to have this

class EventUpdateView(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
	"""
	Create a new reference
	"""
	model = Event
	form_class = EventUpdateForm
	template_name = 'event/event_update.html'

	## Other solution to get the reference
	## https://pypi.python.org/pypi?%3aaction=display&name=django-contrib-requestprovider&version=1.0.1
	def get_form_kwargs(self):
		"""
		Set the request to pass in the form
		"""
		kw = super(EventUpdateView, self).get_form_kwargs()
		kw['request'] = self.request # the trick!
		return kw
	
	def get_success_url(self):
		return reverse_lazy('project-events', args=[self.request.session[Constants.SESSION_PROJECTS_PK_KEY]])
		
	def get_context_data(self, **kwargs):
		context = super(EventUpdateView, self).get_context_data(**kwargs)
		context['nav_projets'] = True
		context['is_super_user'] = self.request.user.is_superuser
		context['is_active'] = self.request.user.is_active
		context['source_pk'] = self.kwargs['pk']	## with this, is possible to pass the pk_project, to include in rever_lazy in django-update-forms
		
		### message to 
		context['message_note'] = "Maximum size per file is {}.".format(filesizeformat(settings.MAX_FILE_UPLOAD))

		context['project_pk'] = self.request.session[Constants.SESSION_PROJECTS_PK_KEY]
		context['edit_remove_events_type'] = True if EventType.objects.exclude(name__isnull=True).count() > 0 else False
		
		## list of files
		query_set = File.objects.filter(event__pk=self.kwargs['pk'], is_deleted=False).order_by('-creation_date')
		table = FilesEventTable(query_set, request=self.request)
		context['table'] = table
		
		## event source pk
		self.request.session[Constants.SESSION_EVENT_PK_KEY] = str(self.object.pk)
		return context
	
	def form_valid(self, form):
		
		### test anonymous account
		if (not self.request.user.is_superuser or not self.request.user.is_active):
			messages.warning(self.request, "'{}' account can not update projects.".format(self.request.user.username), fail_silently=True)
			return super(EventUpdateView, self).form_invalid(form)

		## save it...
		with transaction.atomic():
			event = form.save(commit=False)
			### need to add an update class
			# event.owner = self.request.user
			event.save()

			### set the possible update from the previous
			manage_database = ManageDatabase()
			manage_database.set_event_metakey(event, self.request.user,\
				MetaKeyAndValue.META_KEY_event_update, MetaKeyAndValue.META_VALUE_Success,
				event.to_json())
			
		messages.success(self.request, "Event '" + event.event_type.name + "' was updated successfully", fail_silently=True)
		return super(EventUpdateView, self).form_valid(form)

	## static method, not need for now.
	form_valid_message = ""		## need to have this

class EventView(LoginRequiredMixin, DetailView):
	"""
	Create a new reference
	"""
	model = Event
	template_name = 'event/event_detail.html'

	def get_success_url(self):
		return reverse_lazy('project-events', args=[self.request.session[Constants.SESSION_PROJECTS_PK_KEY]])
		
	def get_context_data(self, **kwargs):
		context = super(EventView, self).get_context_data(**kwargs)
		event = kwargs['object']
		
		context['nav_item'] = self.kwargs.get('tab_item', 'tab_files')
		context['nav_projets'] = True
		context['is_super_user'] = self.request.user.is_superuser
		context['is_active'] = self.request.user.is_active
		context['header_message'] = "View event: {}".format(event.event_type.name)
		context['event'] = event
		try:
			project = Project.objects.get(pk=self.request.session[Constants.SESSION_PROJECTS_PK_KEY])
			context['project'] = project
		except Project.DoesNotExist:
			message = "Fail to collect this project pk: '{}'".format(self.request.session[Constants.SESSION_PROJECTS_PK_KEY])
			self.logger_production.error(message)
			self.logger_debug.error(message)
		
		##### get the number of hours, unique people and equipment hours
		(context['event_number_people_allocated'], context['event_number_hours'],
			context['event_number_hours_equipment']) = event.get_number_hours()
		
		## list of files
		query_set = File.objects.filter(event__pk=self.kwargs['pk'], is_deleted=False).order_by('-creation_date')
		table = FilesEventTable(query_set, request=self.request)
		context['table'] = table
		
		## list of man power
		query_set_man_power = PersonInEvent.objects.filter(event__pk=self.kwargs['pk'], is_deleted=False).order_by('-creation_date')
		table_man_power = ManPowerEventTable(query_set_man_power, request=self.request)
		context['table_man_power'] = table_man_power
		
		## list of equipment
		query_set_equipment = EquipmentInEvent.objects.filter(event__pk=self.kwargs['pk'], is_deleted=False).order_by('-creation_date')
		table_equipment = EquipmentEventTable(query_set_equipment, request=self.request)
		context['table_equipment'] = table_equipment
		
		
		## event source pk
		self.request.session[Constants.SESSION_EVENT_PK_KEY] = str(event.id)
		return context
	
	## static method, not need for now.
	form_valid_message = ""		## need to have this


class FileAddView(LoginRequiredMixin, FormValidMessageMixin, FormView):
	"""
	Create a new reference
	"""
	template_name = 'files/files_add.html'
	form_class = UploadMultipleFilesForm
	utils = Utils()
	
	def get_form_kwargs(self):
		"""
		Set the request to pass in the form
		"""
		kw = super(FileAddView, self).get_form_kwargs()
		kw['request'] = self.request
		return kw
	
	def get_success_url(self):
		return reverse_lazy('event-view', kwargs={ 'pk': self.request.session[Constants.SESSION_EVENT_PK_KEY],
											'tab_item': 'tab_files'})
		
	def get_context_data(self, **kwargs):
		context = super(FileAddView, self).get_context_data(**kwargs)
		context['nav_projets'] = True
		context['is_super_user'] = self.request.user.is_superuser
		context['is_active'] = self.request.user.is_active
		context['project_pk'] = self.request.session[Constants.SESSION_PROJECTS_PK_KEY]
		context['event_pk'] = self.request.session[Constants.SESSION_EVENT_PK_KEY]
		context['message_note'] = "Maximum size per file is {}.".format(filesizeformat(settings.MAX_FILE_UPLOAD))
		
		try:
			event = Event.objects.get(pk=self.request.session[Constants.SESSION_EVENT_PK_KEY])
			context['event'] = event
			context['header_message'] = "Upload files to event -{}-".format(event.event_type.name)
		except Event.DoesNotExist:
			message = "Fail to collect this event pk: '{}'".format(self.request.session[Constants.SESSION_EVENT_PK_KEY])
			self.logger_production.error(message)
			self.logger_debug.error(message)
		
		try:
			project = Project.objects.get(pk=self.request.session[Constants.SESSION_PROJECTS_PK_KEY])
			context['project'] = project
		except Project.DoesNotExist:
			message = "Fail to collect this project pk: '{}'".format(self.request.session[Constants.SESSION_PROJECTS_PK_KEY])
			self.logger_production.error(message)
			self.logger_debug.error(message)
		return context
	
	
	def post(self, request):
		form = UploadMultipleFilesForm(request.POST, request.FILES, request=request)
		
		data = {}	## return data
		try:
			if form.is_valid():
				
				## doesn't work like that
				#upload_files = form.save()
				
				### get the temporary variable
				path_name = form.cleaned_data['path_name']
				if (path_name is None):
					data = {'is_valid': False, 'name': self.request.FILES['path_name'].name, 'message' : 'Internal server error, path not found.' }
					return JsonResponse(data)

				## because sometimes has 
# 				if (str(type(path_name.file)) == "<class '_io.BytesIO'>"):
# 					temp_file = self.utils.get_temp_file("upload_file", ".dat")
# 					with open(temp_file, 'wb') as out: ## Open temporary file as bytes
# 						path_name.file.seek(0)
# 						out.write(path_name.file.read())                ## Read bytes into file
# 					self.utils.move_file(temp_file, sz_file_to)
# 				else: self.utils.copy_file(path_name.file.name, sz_file_to)

				## get event by id			
				event = Event.objects.get(pk=self.request.session[Constants.SESSION_EVENT_PK_KEY])
	
				## get path random
				path_to_file_partial = self.utils.get_path_to_project_event_file_with_random(
						self.request.session[Constants.SESSION_PROJECTS_PK_KEY], 
						self.request.session[Constants.SESSION_EVENT_PK_KEY],
						self.request.user.pk)
				path_to_file = os.path.join(settings.MEDIA_ROOT, path_to_file_partial)
			
				with LockedAtomicTransaction(File):
					## test directory
					if (not os.path.exists(path_to_file)): self.utils.make_path(path_to_file)
				
					### save file
					file = File()
					file_name_cleaned = self.utils.clean_name(ntpath.basename(path_name.name))
					with open(os.path.join(path_to_file, file_name_cleaned), 'wb') as handle_write:
						handle_write.write(path_name.read())
					file.file_name = file_name_cleaned
					file.path_name.name = os.path.join(path_to_file_partial, file_name_cleaned)
					file.hash_file = self.utils.md5sum(file.get_path_root())
					file.owner = self.request.user
					file.event = event
					file.save()
	
				message = "Import file: {}    File type: {}".format(file_name_cleaned, str(type(path_name.file)))
				logger_debug.info(message)
				logger_production.info(message)
				
				data = {'is_valid': True, 'name': file_name_cleaned, 'url': mark_safe(file.get_only_path_web()) }
			else:
				data = {'is_valid': False, 'name': self.request.FILES['path_name'].name, 'message' : str(form.errors['path_name'][0]) }
		except:
			self.logger_debug.error(sys.exc_info())
			self.logger_production.error(sys.exc_info())
			data = {'is_valid': False, 'name': self.request.FILES['path_name'].name, 'message' : 'Internal server error, unknown error.' }
			return JsonResponse(data)
	
		return JsonResponse(data)
	


