'''
Created on 19/03/2020

@author: mmp
'''
from bootstrap_modal_forms.forms import BSModalForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, ButtonHolder, Submit, Button, Fieldset
from django import forms
from django.contrib.auth.models import User
from projects.models import Project, Research, Specie, ProjectType, Institute, EventType, Event
from projects.models import File, PersonInEvent, Equipment, EquipmentInEvent
from django.urls import reverse
from constants.constants import Constants
from django.conf import settings
from project_manager.formatChecker import ContentTypeRestrictedFileFieldForm
from django.template.defaultfilters import filesizeformat
import os, datetime

## https://kuanyui.github.io/2015/04/13/django-crispy-inline-form-layout-with-bootstrap/
class ProjectForm(forms.ModelForm):
	"""
	Reference form, name, isolate_name and others
	"""
	error_css_class = 'error'
	description = forms.CharField(widget=forms.Textarea(attrs={'rows': '6'}))
	start_date = forms.DateField(widget=forms.DateInput(
					format=settings.DATE_INPUT_FORMATS[0],
					attrs={
						"class": "form-control text-input" , ## 'type':'date',
					}
				),
				input_formats = settings.DATE_INPUT_FORMATS,
				initial = datetime.datetime.today,
			)
	end_date = forms.DateField(widget=forms.DateInput(
					format=settings.DATE_INPUT_FORMATS[0],
					attrs={
						"class": "form-control text-input" , ## 'type':'date',
					}
				),
				input_formats = settings.DATE_INPUT_FORMATS,
				initial = datetime.datetime.today() + datetime.timedelta(days=60),
			)
	
	class Meta:
		model = Project
		# specify what fields should be used in this form.
		fields = ('research', 'specie', 'project_type', 'institute', 'description', 'start_date', 'end_date')
		
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request')
		super(ProjectForm, self).__init__(*args, **kwargs)

		self.fields['research'].queryset = Research.objects.exclude(name__isnull=True).exclude(name__exact='').order_by("name")
		self.fields['research'].empty_label = None		## to remove empty label in combo box
		self.fields['specie'].queryset = Specie.objects.exclude(name__isnull=True).exclude(name__exact='').all()
		self.fields['specie'].empty_label = None		## to remove empty label in combo box
		self.fields['project_type'].queryset = ProjectType.objects.exclude(name__isnull=True).exclude(name__exact='').all()
		self.fields['project_type'].empty_label = None		## to remove empty label in combo box
		self.fields['institute'].queryset = Institute.objects.exclude(name__isnull=True).exclude(name__exact='').all()
		self.fields['institute'].empty_label = None		## to remove empty label in combo box
		
		## can exclude explicitly
		field_text= [
			# (field_name, Field title label, Detailed field description, requiered)
			('description', 'Description', 'Project short summary...', True),
			('research', 'Client', 'Whom order the project', True),
			('specie', 'Specie', 'Specie on analysis', True),
			('project_type', 'Project type', 'Project type', True),
			('institute', 'Institute', 'Institute attached to the project', True),
			('start_date', 'Start date', 'Start date of the project. (YYYY-MM-DD)', True),
			('end_date', 'End date', 'Possible end date of the project. (YYYY-MM-DD)', True),
		]
		for x in field_text:
			self.fields[x[0]].label = x[1]
			self.fields[x[0]].help_text = x[2]
			self.fields[x[0]].required = x[3]

		self.helper = FormHelper()
		self.helper.form_method = 'POST'
		self.helper.layout = Layout(
			Fieldset(
				'Create a project',
				Div(
					Div('description', css_class="col-sm-12"),
					css_class = 'row'
				),
				Div(
					Div( 
						Div('research'),
						## buttons are in javascript js/project-add.js
						css_class = "col-sm-4"),
					Div(
						Div('specie'),
						## buttons are in javascript js/project-add.js
						css_class = "col-sm-4"),
					Div( 
						Div('project_type'),
						## buttons are in javascript js/project-add.js
						css_class = "col-sm-4"),
					css_class = 'row'
				),
				Div(
					Div( 
						Div('institute'),
						css_class = "col-sm-4"),
					Div( 
						Div('start_date'),
						css_class = "col-sm-4"),
					Div( 
						Div('end_date'),
						css_class = "col-sm-4"),
					css_class = 'row'
				),
				css_class = 'article-content'
			),
			ButtonHolder(
				Submit('save', 'Save', css_class='btn-primary'),
				Button('cancel', 'Cancel', css_class='btn-secondary', onclick='window.location.href="{}"'.format(reverse('projects')))
			)
		)

class ResearchForm(BSModalForm):
	class Meta:
		model = Research
		fields = ['_name_data', '_email_data', '_phone_data']
	
class ProjectTypeForm(BSModalForm):
	class Meta:
		model = ProjectType
		fields = ['name', 'abbreviation', 'description']

class SpecieForm(BSModalForm):
	class Meta:
		model = Specie
		fields = ['name']

class InstituteForm(BSModalForm):
	class Meta:
		model = Institute
		fields = ['_name_data', '_abbreviation_data', '_city_data']

class EventTypeForm(BSModalForm):
	class Meta:
		model = EventType
		fields = ['name', 'description']

class EquipmentForm(BSModalForm):
	class Meta:
		model = Equipment
		fields = ['name', 'room', 'ip', 'description']

class ManPowerForm(BSModalForm):
	
	class Meta:
		model = PersonInEvent
		fields = ['person', 'number_of_hours', 'description']
		
	def __init__(self, *args, **kwargs):
		self.request = kwargs.get('request')
		super(ManPowerForm, self).__init__(*args, **kwargs)
		self.fields['person'].queryset = User.objects.exclude(username__in=settings.PASS_IN_PERSON_USERNAMES)
		if (not self.instance.id is None):
			self.fields['person'].initial = self.instance.person.id

class EquipmentEventForm(BSModalForm):
	
	class Meta:
		model = EquipmentInEvent
		fields = ['equipment', 'number_of_hours', 'description']
		
	def __init__(self, *args, **kwargs):
		self.request = kwargs.get('request')
		super(EquipmentEventForm, self).__init__(*args, **kwargs)
		self.fields['equipment'].queryset = Equipment.objects.all()
		if (not self.instance.id is None):
			self.fields['equipment'].initial = self.instance.equipment.id
			
## https://kuanyui.github.io/2015/04/13/django-crispy-inline-form-layout-with-bootstrap/
class EventForm(forms.ModelForm):
	"""
	Reference form, name, isolate_name and others
	"""
	error_css_class = 'error'
	description = forms.CharField(widget=forms.Textarea(attrs={'rows': '6'}))
	file_field = ContentTypeRestrictedFileFieldForm(widget=forms.ClearableFileInput(attrs={'multiple': True}),
							max_upload_size=settings.MAX_FILE_UPLOAD)
	
	class Meta:
		model = Event
		# specify what fields should be used in this form.
		fields = ('event_type', 'description')
		
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request')
		super(EventForm, self).__init__(*args, **kwargs)

		self.fields['event_type'].queryset = EventType.objects.exclude(name__isnull=True).exclude(name__exact='').all()
		self.fields['event_type'].empty_label = None		## to remove empty label in combo box
		
		## can exclude explicitly
		## exclude = ('md5',)
		field_text= [
			('description', 'Description', 'Event short summary...', False),
			('event_type', 'Event type', 'Event type', True),
			('file_field', 'Import Files', 'You can also add files on edit view of the Event. ' +\
				"Maximum size per file is {}.".format(filesizeformat(settings.MAX_FILE_UPLOAD)), False),
		]
		for x in field_text:
			self.fields[x[0]].label = x[1]
			self.fields[x[0]].help_text = x[2]
			self.fields[x[0]].required = x[3]

		self.helper = FormHelper()
		self.helper.form_method = 'POST'
		self.helper.layout = Layout(
			Fieldset(
				'Create an Event',
				Div(
					Div('description', css_class="col-sm-12"),
					css_class = 'row'
				),
				Div(
					Div( 
						Div('event_type'),
						## buttons are in javascript js/project-add.js
						css_class = "col-sm-4"),
					css_class = 'row'
				),
				css_class = 'article-content'
			),
			Fieldset(
				'Upload files, you can also upload/remove files after create an event. Max. per file: {}'.format(\
						filesizeformat(settings.MAX_FILE_UPLOAD)),
				Div(
					Div('file_field', css_class="col-sm-12"),
					css_class = 'row'
				),
				css_class = 'article-content'
			),
			ButtonHolder(
				Submit('save', 'Save', css_class='btn-primary'),
				Button('cancel', 'Cancel', css_class='btn-secondary', onclick='window.location.href="{}"'.format(reverse('project-events',
								args=[self.request.session[Constants.SESSION_PROJECTS_PK_KEY]])))
			)
		)

class EventUpdateForm(forms.ModelForm):
	"""
	Reference form, name, isolate_name and others
	"""
	error_css_class = 'error'
	description = forms.CharField(widget=forms.Textarea(attrs={'rows': '6'}))
	file_field = ContentTypeRestrictedFileFieldForm(widget=forms.ClearableFileInput(attrs={'multiple': True}),
							max_upload_size=settings.MAX_FILE_UPLOAD)
	
	class Meta:
		model = Event
		# specify what fields should be used in this form.
		fields = ('event_type', 'description')
		
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request')
		super(EventUpdateForm, self).__init__(*args, **kwargs)

		self.fields['event_type'].queryset = EventType.objects.exclude(name__isnull=True).exclude(name__exact='').all()
		self.fields['event_type'].empty_label = None		## to remove empty label in combo box
		
		## can exclude explicitly
		## exclude = ('md5',)
		field_text= [
			('description', 'Description', 'Event short summary...', False),
			('event_type', 'Event type', 'Event type', True),
			('file_field', 'Import Files', 'You can also add files on edit view of the Event. ' +\
				"Maximum size per file is {}.".format(filesizeformat(settings.MAX_FILE_UPLOAD)), False),
		]
		for x in field_text:
			self.fields[x[0]].label = x[1]
			self.fields[x[0]].help_text = x[2]
			self.fields[x[0]].required = x[3]

		self.helper = FormHelper()
		self.helper.form_method = 'POST'
		self.helper.layout = Layout(
			Fieldset(
				'',  ## it is in HTML
				Div(
					Div('description', css_class="col-sm-12"),
					css_class = 'row'
				),
				Div(
					Div( 
						Div('event_type'),
						## buttons are in javascript js/project-add.js
						css_class = "col-sm-4"),
					css_class = 'row'
				),
				css_class = 'article-content'
			),
			ButtonHolder(
				Submit('save', 'Save', css_class='btn-primary'),
				Button('cancel', 'Cancel', css_class='btn-secondary', onclick='window.location.href="{}"'.format(reverse('project-events',
								args=[self.request.session[Constants.SESSION_PROJECTS_PK_KEY]])))
			)
		)

class UploadMultipleFilesForm(forms.ModelForm):
	"""
	Add multiple files to and event
	Try to put some limits
	"""
	
	class Meta:
		model = File
		fields = ('path_name', )

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request')
		super(UploadMultipleFilesForm, self).__init__(*args, **kwargs)
		
	def clean(self):
		"""
		Test data 
		"""
		cleaned_data = super(UploadMultipleFilesForm, self).clean()
		
		if (not self.request.user.is_superuser or not self.request.user.is_active):
			self.add_error('path_name', "You are not allowed to perform this operation.")
			return cleaned_data
		
		### get path name
		if ('path_name' not in self.cleaned_data):
			self.add_error('path_name', "There's no file to upload")
			return cleaned_data
		path_name = self.cleaned_data['path_name']
		
		### test the file name if exist
		number_files = File.objects.filter(file_name__iexact=os.path.basename(path_name.name),\
 				is_deleted=False, event__pk=self.request.session[Constants.SESSION_EVENT_PK_KEY]).count()

		if (number_files > 0):
			self.add_error('path_name', "There is one file with this name in the event.")
			return cleaned_data
		
		if (path_name.size > settings.MAX_FILE_UPLOAD):
			self.add_error('path_name', "Max file size is: {}".format(filesizeformat(settings.MAX_FILE_UPLOAD)))
			return cleaned_data
		return cleaned_data	
	
	