from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize

from project_manager.formatChecker import ContentTypeRestrictedFileField
from utils.utils import Utils
from constants.constants import Constants

from encrypted_fields import fields
import os

from django.core.exceptions import (
	NON_FIELD_ERRORS,
)

from django.db import (connection,
)


def user_directory_path(instance, filename):
	"""
	file will be uploaded to MEDIA_ROOT/<filename>
	"""
	return 'uploads/generic_data/user_{0}/{1}'.format(instance.owner.id, filename)


# Create your models here.
class Institute(models.Model):
	"""
	institute that belongs the research that belongs the research
	"""
	class Meta:
		permissions = [('can_view_institutes', 'Can view institutes'), ('can_add_institutes', 'Can add institutes'),\
					('can_delete_institutes', 'Can delete institutes'), ('can_update_institutes', 'Can update institutes')]
		ordering = ['name', ]
		
	_name_data = fields.EncryptedCharField(max_length=250, verbose_name='Name', unique=True)
	name = fields.SearchField(hash_key=settings.HASH_KEY_INSTITUTE_NAME, encrypted_field_name="_name_data", )
	_abbreviation_data = fields.EncryptedCharField(max_length=30, verbose_name='Abbreviation', unique=True)
	abbreviation = fields.SearchField(hash_key=settings.HASH_KEY_INSTITUTE_ABBREVIATION, encrypted_field_name="_abbreviation_data", )
	_city_data = fields.EncryptedCharField(max_length=30, verbose_name='City')
	city = fields.SearchField(hash_key=settings.HASH_KEY_INSTITUTE_CITY, encrypted_field_name="_city_data", )
	owner = models.ForeignKey(User, related_name='institute', on_delete=models.CASCADE)
	is_obsolete = models.BooleanField(default=False, verbose_name='Obsolete')
	creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')
	
	#######################################
	## translate unique fields
	dt_data_uniq_translate = { '_name_data': 'name', '_abbreviation_data' : 'abbreviation' }
	## comment unique limitation in 
	##  django3.0/lib/python3.6/site-packages/encrypted_fields/fields.py
	##  line 47
	#######################################
	
	def __str__(self):
		return self.abbreviation

	def __eq__(self, other):
		if not isinstance(other, Institute):
			# don't attempt to compare against unrelated types
			return NotImplemented
	
		return self.abbreviation.strip().lower() == other.abbreviation.strip().lower()

	def __key(self):
		return (self.name, self.abbreviation)
	def __hash__(self):
		return hash(self.__key())
	
	#######################################
	## ADD this method
	## translate unique fields
	def _perform_unique_checks(self, unique_checks):
		"""
		this method overrides a method in base Model
			django3.0/lib/python3.6/site-packages/django/db/models/base.py
		line 1070
		"""
		errors = {}

		for model_class, unique_check in unique_checks:
			# Try to look up an existing object with the same values as this
			# object's values for all the unique field.

			lookup_kwargs = {}
			for field_name in unique_check:
				
				## Add by MMP
				if field_name in self.dt_data_uniq_translate: field_name = self.dt_data_uniq_translate[field_name]
				
				f = self._meta.get_field(field_name)
				lookup_value = getattr(self, f.attname)
				if (lookup_value is None or
						(lookup_value == '' and connection.features.interprets_empty_strings_as_nulls)):
					# no value, skip the lookup
					continue
				if f.primary_key and not self._state.adding:
					# no need to check for unique primary key when editing
					continue
				lookup_kwargs[str(field_name)] = lookup_value

			# some fields were skipped, no reason to do the check
			if len(unique_check) != len(lookup_kwargs):
				continue

			qs = model_class._default_manager.filter(**lookup_kwargs)

			# Exclude the current object from the query if we are editing an
			# instance (as opposed to creating a new one)
			# Note that we need to use the pk as defined by model_class, not
			# self.pk. These can be different fields because model inheritance
			# allows single model to have effectively multiple primary keys.
			# Refs #17615.
			model_class_pk = self._get_pk_val(model_class._meta)
			if not self._state.adding and model_class_pk is not None:
				qs = qs.exclude(pk=model_class_pk)
			if qs.exists():
				if len(unique_check) == 1:
					key = unique_check[0]
				else:
					key = NON_FIELD_ERRORS
				errors.setdefault(key, []).append(self.unique_error_message(model_class, unique_check))
		return errors
	
class Research(models.Model):
	"""
	Research that ask something or make a sequence/project (Client)
	"""
	class Meta:
		permissions = [('can_view_researches', 'Can view researches'), ('can_add_researches', 'Can add researches'),\
					('can_delete_researches', 'Can delete researches'), ('can_update_researches', 'Can update researches')]
		ordering = ['name', ]
		
	_name_data = fields.EncryptedCharField(max_length=250, verbose_name='Name', unique=True)
	name = fields.SearchField(hash_key=settings.HASH_KEY_RESEARCH_NAME, encrypted_field_name="_name_data", )
	_email_data = fields.EncryptedCharField(max_length=100, verbose_name='Email', unique=True)
	email = fields.SearchField(hash_key=settings.HASH_KEY_RESEARCH_EMAIL, encrypted_field_name="_email_data", )
	_phone_data = fields.EncryptedCharField(max_length=30, verbose_name='Phone', blank=True, null=True)
	phone = fields.SearchField(hash_key=settings.HASH_KEY_RESEARCH_PHONE, encrypted_field_name="_phone_data", )
	owner = models.ForeignKey(User, related_name='research', on_delete=models.CASCADE)
	is_obsolete = models.BooleanField(default=False, verbose_name='Obsolete')
	creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')

	#######################################
	## translate unique fields
	dt_data_uniq_translate = { '_name_data': 'name', '_email_data': 'email'}
	## comment unique limitation in 
	##  django3.0/lib/python3.6/site-packages/encrypted_fields/fields.py
	##  line 47
	#######################################
	
	def __str__(self):
		return self.name

	def __eq__(self, other):
		if not isinstance(other, Research):
			# don't attempt to compare against unrelated types
			return NotImplemented
	
		return self.name.strip().lower() == other.name().strip().lower()
	
	def __key(self):
		return (self.name, self.email)
	def __hash__(self):
		return hash(self.__key())
	
# 	def delete(self, *args, **kwargs):
# 		"""
# 		try to delete, if not created
# 		"""
# 		if Project.objects.filter(research__pk= self.pk).exists():
# 			raise Exception("This research '{}' has a relation with projects.".format(self.name))  # or you can throw your custom exception here.
# 		super(Research, self).delete(*args, **kwargs)

	#######################################
	## ADD this method
	## translate unique fields
	def _perform_unique_checks(self, unique_checks):
		"""
		this method overrides a method in base Model
			django3.0/lib/python3.6/site-packages/django/db/models/base.py
		line 1070
		"""
		errors = {}

		for model_class, unique_check in unique_checks:
			# Try to look up an existing object with the same values as this
			# object's values for all the unique field.

			lookup_kwargs = {}
			for field_name in unique_check:
				
				## Add by MMP
				if field_name in self.dt_data_uniq_translate: field_name = self.dt_data_uniq_translate[field_name]
				
				f = self._meta.get_field(field_name)
				lookup_value = getattr(self, f.attname)
				if (lookup_value is None or
						(lookup_value == '' and connection.features.interprets_empty_strings_as_nulls)):
					# no value, skip the lookup
					continue
				if f.primary_key and not self._state.adding:
					# no need to check for unique primary key when editing
					continue
				lookup_kwargs[str(field_name)] = lookup_value

			# some fields were skipped, no reason to do the check
			if len(unique_check) != len(lookup_kwargs):
				continue

			qs = model_class._default_manager.filter(**lookup_kwargs)

			# Exclude the current object from the query if we are editing an
			# instance (as opposed to creating a new one)
			# Note that we need to use the pk as defined by model_class, not
			# self.pk. These can be different fields because model inheritance
			# allows single model to have effectively multiple primary keys.
			# Refs #17615.
			model_class_pk = self._get_pk_val(model_class._meta)
			if not self._state.adding and model_class_pk is not None:
				qs = qs.exclude(pk=model_class_pk)
			if qs.exists():
				if len(unique_check) == 1:
					key = unique_check[0]
				else:
					key = NON_FIELD_ERRORS
				errors.setdefault(key, []).append(self.unique_error_message(model_class, unique_check))
		return errors


class EventType(models.Model):
	"""
	Event type
	By default
	Sequencing, Report release, Analyses pipeline, Quotation
	"""
	class Meta:
		permissions = [('can_create_eventtypes', 'Can create event types'), ('can_delete_eventtypes', 'Can delete event types'),\
					('can_view_eventtypes', 'Can view event types'), ('can_update_eventtypes', 'Can update event types')]
		ordering = ['name', ]
		
	name = models.CharField(max_length=100, verbose_name='Name', db_index=True, unique=True)
	description = models.CharField(max_length=250, default='', verbose_name='Description')
	owner = models.ForeignKey(User, related_name='eventtype', on_delete=models.PROTECT)
	creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')
	
	def __str__(self):
		return self.name


class ProjectType(models.Model):
	"""
	Event type
	By default
	WGS, GWAS, RNAseq, ChipSeq
	"""
	class Meta:
		permissions = [('can_create_projecttypes', 'Can create project types'), ('can_delete_projecttypes', 'Can delete project types'),\
					('can_view_projecttypes', 'Can view project types'), ('can_update_projecttypes', 'Can update project types')]
		ordering = ['name', ]
		
	name = models.CharField(max_length=40, verbose_name='Name', db_index=True, unique=True)
	abbreviation = models.CharField(max_length=20, verbose_name='Abbreviation')
	description = models.CharField(max_length=100, default='', blank=True, null=True, verbose_name='Description')
	owner = models.ForeignKey(User, related_name='projectype', on_delete=models.PROTECT)
	creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')
	def __str__(self):
		return self.name

	def __eq__(self, other):
		if not isinstance(other, ProjectType):
			# don't attempt to compare against unrelated types
			return NotImplemented
	
		return self.name.strip().lower() == other.name.strip().lower()
	
	def __key(self):
		return (self.name, self.abbreviation)
	def __hash__(self):
		return hash(self.__key())

class Specie(models.Model):
	"""
	Event type
	By default
	Homo sapiens, Mus musculus, Rattus norvegicus, Candida Albicans, Saccharomyces cerevisiae
	"""
	class Meta:
		permissions = [('can_create_specietypes', 'Can create specie types'), ('can_delete_specietypes', 'Can delete specie types'),\
					('can_view_specietypes', 'Can view specie types'), ('can_update_specietypes', 'Can update specie types')]
		ordering = ['name', ]
		
	name = models.CharField(max_length=100, verbose_name='Name', db_index=True, unique=True)
	owner = models.ForeignKey(User, related_name='specie', on_delete=models.PROTECT)
	creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')
	
	def __str__(self):
		return self.name

class Equipment(models.Model):
	
	class Meta:
		permissions = [('can_create_equipment', 'Can create equipments'), ('can_delete_equipment', 'Can delete equipment'),\
					('can_view_equipment', 'Can view equipment'), ('can_update_equipment', 'Can update equipment')]
		ordering = ['name', ]
		
	name = models.CharField(max_length=100, verbose_name='Name', db_index=True, unique=True)
	room = models.CharField(max_length=50, verbose_name='Room')
	ip = models.GenericIPAddressField(verbose_name='IP address', blank=True, null=True, unique=True)
	description = models.CharField(max_length=100, default='', blank=True, verbose_name='Description')
	owner = models.ForeignKey(User, related_name='equipment', on_delete=models.PROTECT)
	creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')
	
	def __str__(self):
		return self.name
	
	def __eq__(self, other):
		if not isinstance(other, ProjectType):
			# don't attempt to compare against unrelated types
			return NotImplemented
	
		return self.name.strip().lower() == other.name.strip().lower()
	
	def __key(self):
		return (self.name, self.room)
	def __hash__(self):
		return hash(self.__key())
	
class Project(models.Model):
	"""
	Project sequence/cotation
	
	$ sudo vi /home/software/django3.0/lib/python3.6/site-packages/bootstrap_modal_forms/mixins.py
		def post(self, request, *args, **kwargs):
		try:
			httpResponse = super(DeleteMessageMixin, self).delete(request, *args, **kwargs)
			messages.success(request, self.success_message)
			return httpResponse
		except ProtectedError:
			messages.error(request, "Can't remove this item, has a relation in database.")
			return HttpResponseRedirect(self.success_url)

	"""
	class Meta:
		verbose_name = 'Project'
		verbose_name_plural = 'Projects'
		permissions = [('can_create_projects', 'Can create projects'), ('can_delete_projects', 'Can delete projects'),\
					('can_view_projects', 'Can view projects'), ('can_update_projects', 'Can update projects')]
		ordering = ['-start_date', '-id']

	description = models.CharField(max_length=1000, default='', verbose_name='Description') ## to show   {{ value|linebreaks }}
	reference = models.CharField(max_length=50, verbose_name='Reference ID')	## reference number <type project>.<year>.s<sequencing number by year>.v<version number>
																					## sequencing number 
																					## version number is add by the event
	is_deleted = models.BooleanField(default=False, verbose_name='Is Deleted')		## if this file was removed
	research = models.ForeignKey(Research, related_name='project', blank=True, null=True, on_delete=models.PROTECT, verbose_name='Research')
	institute = models.ForeignKey(Institute, related_name='project', blank=True, null=True, on_delete=models.PROTECT, verbose_name='Institute')
	creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')
	owner = models.ForeignKey(User, related_name='project', on_delete=models.PROTECT, verbose_name='Created by')
	delete_date = models.DateTimeField(null=True, verbose_name='Delete Date')
	delete_owner = models.ForeignKey(User, related_name='delete_project', blank=True, null=True, on_delete=models.PROTECT)
	specie = models.ForeignKey(Specie, related_name='project', on_delete=models.PROTECT, verbose_name='Specie')
	project_type = models.ForeignKey(ProjectType, related_name='project', on_delete=models.PROTECT, verbose_name='Proj.Type')
	
	start_date = models.DateField(verbose_name='Start Date', default=now)	### start date
	end_date = models.DateField(verbose_name='End Date', default=now)		### end date
	number_people_allocated = models.IntegerField(blank=False, null=False, default=0)	### total people allocated, it's the sum of the all events
	number_hours = models.IntegerField(blank=False, null=False, default=0)			### total number of hours, it's the sum of the all events
	number_hours_of_equiments = models.IntegerField(blank=False, null=False, default=0)			### total number of hours, for the equipments, it's the sum of the all events
	
	def get_project_reference(self):
		"""
			reference number <type project>.<year>.s<sequencing number by year>.v<version number>
			version number is add by the event 
		"""
		if (self.id is None):
			count_year = self.get_biggest_sequence_number() + 1 
			return "{}.{}.s{}".format(self.project_type.abbreviation, self.start_date.year, count_year)
		elif (self.change_project_type()):
			count_year = self.get_biggest_sequence_number() + 1 
			return "{}.{}.s{}".format(self.project_type.abbreviation, self.start_date.year, count_year)
		else: return self.reference

	def change_project_type(self):
		"""
		return True if self.project_type.abbreviation is different from startWith till dot.
		"""
		return self.project_type.abbreviation != ".".join(self.reference.split('.')[:-2])

	def get_biggest_sequence_number(self):
		"""
		get the biggest number for a specific project type and year
		"""
		
		biggest_number = 0
		for project in Project.objects.filter(project_type=self.project_type, creation_date__year=self.start_date.year):
			try:
				number_os_sequential_project = int(project.reference.split('.')[-1].replace('s', ''))
			except:
				number_os_sequential_project = 0
			if (biggest_number < number_os_sequential_project): biggest_number = number_os_sequential_project
		return biggest_number

	def update_people_and_time(self):
		"""
		Update people and time for this project
		"""
		self.number_hours = 0
		self.number_people_allocated = 0
		
		dict_out_id_user = {}
		for event in list(Event.objects.filter(project__id=self.id, is_deleted=False)):
			if (event.people_in_event.count() == 0): continue
			
			### sum people hours and number
			for person_event in event.people_in_event.filter(is_deleted=False):
				self.number_hours += person_event.number_of_hours
				if (person_event.person.id in dict_out_id_user): continue
				dict_out_id_user[person_event.person.id] = 1
				self.number_people_allocated += 1
				
		### update
		self.save()
	
	def update_equipment_hours(self):
		"""
		Update hours of the equipment
		"""
		self.number_hours_of_equiments = 0
		
		### sum equipment hours
		for event in list(Event.objects.filter(project__id=self.id, is_deleted=False)):
			if (event.equipment_in_event.count() == 0): continue
			for equipment_event in event.equipment_in_event.filter(is_deleted=False):
				self.number_hours_of_equiments += equipment_event.number_of_hours
		### update
		self.save()
	
	
	def to_json(self):
		return serialize('json', [self], cls=LazyEncoder)
	
class Event(models.Model):
	"""
	Events, can be of several types, sequencing, report release, analyses pipeline, quotation, etc...
	"""
	class Meta:
		verbose_name = 'Event'
		verbose_name_plural = 'Events'
		permissions = [('can_create_events', 'Can create events'), ('can_delete_events', 'Can delete events'),\
					('can_view_events', 'Can view events'), ('can_update_events', 'Can update events')]
		ordering = ['-creation_date', ]
	
	creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')
	owner = models.ForeignKey(User, related_name='event', on_delete=models.PROTECT)
	delete_date = models.DateTimeField(null=True, verbose_name='Delete Date')
	delete_owner = models.ForeignKey(User, related_name='delete_event', blank=True, null=True, on_delete=models.PROTECT)
	is_deleted = models.BooleanField(default=False, verbose_name='Is Deleted')			## if this file was removed in file system
	
	### if is a report the reference is a junction of "project.reference"."event.reference"
	event_type = models.ForeignKey(EventType, related_name='event', on_delete=models.PROTECT)
	description = models.CharField(max_length=1000, default='', blank=True, null=True, verbose_name='Description')

	## project
	project = models.ForeignKey(Project, related_name='event', on_delete=models.PROTECT)

	def to_json(self):
		return serialize('json', [self], cls=LazyEncoder)
	
	def get_number_hours(self):
		"""
		return number of hours
		"""
		event_number_people_allocated = 0
		event_number_hours = 0
		event_number_hours_equipment = 0
		dict_out_id_user = {}
		
		### count people and number of hours
		for person_event in self.people_in_event.filter(is_deleted=False):
			event_number_hours += person_event.number_of_hours
			if (person_event.person.id in dict_out_id_user): continue
			dict_out_id_user[person_event.person.id] = 1
			event_number_people_allocated += 1
		
		### count equipment hours
		for equipment in self.equipment_in_event.filter(is_deleted=False):
			event_number_hours_equipment += equipment.number_of_hours
			
		return (event_number_people_allocated, event_number_hours, event_number_hours_equipment)


class PersonInEvent(models.Model):
	"""
	Has the ID of the person in the event and the hours spend
	"""

	class Meta:
		ordering = ['-creation_date', ]
		permissions = [('can_create_person_in_event', 'Can create person in event'), ('can_delete_person_in_event', 'Can delete person in event'),\
					('can_view_person_in_event', 'Can view person in event')]

	person = models.ForeignKey(User, related_name='person_event', on_delete=models.PROTECT)
	owner = models.ForeignKey(User, related_name='owner_person_event', blank=True, null=True, on_delete=models.PROTECT)
	event = models.ForeignKey(Event, related_name='people_in_event', on_delete=models.PROTECT)
	number_of_hours = models.IntegerField(blank=False, null=False, default=0)
	description = models.CharField(max_length=1000, default="", blank=True, null=False, verbose_name='Description')
	creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')
	delete_date = models.DateTimeField(null=True, verbose_name='Delete Date')
	delete_owner = models.ForeignKey(User, related_name='delete_person_event', blank=True, null=True, on_delete=models.PROTECT)
	is_deleted = models.BooleanField(default=False, verbose_name='Is Deleted')			## if this file was removed in file system
	
	def to_json(self):
		return serialize('json', [self], cls=LazyEncoder)

class EquipmentInEvent(models.Model):
	"""
	Has the ID of the equipment in the event and the hours spend
	"""

	class Meta:
		ordering = ['-creation_date', ]
		permissions = [('can_create_equipment_in_event', 'Can create equipment in event'), ('can_delete_equipment_in_event', 'Can delete equipment in event'),\
					('can_view_equipment_in_event', 'Can view equipment in event')]

	equipment = models.ForeignKey(Equipment, related_name='equipment_event', on_delete=models.PROTECT)
	owner = models.ForeignKey(User, related_name='owner_equipment_event', blank=True, null=True, on_delete=models.PROTECT)
	event = models.ForeignKey(Event, related_name='equipment_in_event', on_delete=models.PROTECT)
	number_of_hours = models.IntegerField(blank=False, null=False, default=0)
	description = models.CharField(max_length=1000, default="", blank=True, null=False, verbose_name='Description')
	creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')
	delete_date = models.DateTimeField(null=True, verbose_name='Delete Date')
	delete_owner = models.ForeignKey(User, related_name='delete_equipment_event', blank=True, null=True, on_delete=models.PROTECT)
	is_deleted = models.BooleanField(default=False, verbose_name='Is Deleted')			## if this file was removed in file system
	
	def to_json(self):
		return serialize('json', [self], cls=LazyEncoder)
	

class File(models.Model):
	"""
	has files add in the event/project
	"""
	class Meta:
		permissions = [('can_upload_files', 'Can upload files'), ('can_delete_files', 'Can delete files'),\
					('can_view_files', 'Can view files')]

	file_name = models.CharField(max_length=400)
	path_name = ContentTypeRestrictedFileField(upload_to=user_directory_path, 
						content_types=['application/octet-stream', 'application/gzip', 'application/x-gzip',\
							'application/pdf', 'txt/css', 'text/csv', 'text/txt', 'text/tsv',\
							'text/tab-separated-values', 'text/plain', 'application/octet-stream',\
							'image/png', 'image/jpeg', 'image/pjpeg',\
							### .doc
							'application/vnd.ms-word', 'application/msword',\
							### .docx
							'application/vnd.openxmlformats-officedocument.wordprocessingml.document',\
							### .xls
							'application/vnd.ms-excel', 'application/msexcel',\
							### .xlsx
							'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',\
							### .ppt
							'application/vnd.ms-powerpoint',\
							### .pptx
							'application/vnd.openxmlformats-officedocument.presentationml.presentation',\
							### .ppsx
							'application/vnd.openxmlformats-officedocument.presentationml.slideshow'],
						max_upload_size=settings.MAX_FILE_UPLOAD, max_length=500)

	_hash_file_data = fields.EncryptedCharField(max_length=250, blank=True, null=True)
	hash_file = fields.SearchField(hash_key=settings.HASH_KEY_FILE_HASH, encrypted_field_name="_hash_file_data", )
	
	owner = models.ForeignKey(User, related_name='file', on_delete=models.PROTECT)
	creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')
	delete_date = models.DateTimeField(null=True, verbose_name='Delete Date')
	delete_owner = models.ForeignKey(User, related_name='delete_file', blank=True, null=True, on_delete=models.CASCADE)
	is_deleted = models.BooleanField(default=False, verbose_name='Is Deleted')			## if this file was removed in file system
	event = models.ForeignKey(Event, related_name='file', blank=True, null=True, on_delete=models.PROTECT)
	
	def __str__(self):
		return self.file_name
	
	def is_a_valid_hash(self):
		"""
		return True if after test the file has the same hash when was uploaded
		to prevent change files after upload 
		"""
		utils = Utils()
		return utils.md5sum(self.get_path_root()) == self.hash_file
		
	def get_path_root(self):
		return os.path.join(settings.MEDIA_ROOT, self.path_name.name)
	
	def get_path_web(self):
		"""
		get web path
		"""
		out_file = self.get_path_root()
		if (os.path.exists(out_file)):
			return mark_safe('<a href="{}" target="_blank">{}</a>'.format(os.path.join(settings.MEDIA_URL,
						self.path_name.name), self.file_name))
		return _('File not available yet.')

	def get_only_path_web(self):
		"""
		only path for a 'href' element
		"""
		out_file = self.get_path_root()
		if (os.path.exists(out_file)):
			return os.path.join(settings.MEDIA_URL, self.path_name.name)
		return _('')



class MetaKey(models.Model):
	"""
	Has meta tags to put values, for example, quality in the files, or samples
	"""
	name = models.CharField(max_length=200, db_index=True, blank=True, null=True)
	def __str__(self):
		return self.name
	
	class Meta:
		ordering = ['name', ]


class MetaKeyProjects(models.Model):
	"""
	Relation ManyToMany in 
	"""
	meta_tag = models.ForeignKey(MetaKey, related_name='meta_key_project', on_delete=models.PROTECT)
	project = models.ForeignKey(Project, related_name='meta_key_project', on_delete=models.PROTECT)
	owner = models.ForeignKey(User, related_name='meta_key_project', on_delete=models.PROTECT)
	creation_date = models.DateTimeField(db_index=True, auto_now_add=True)
	value = models.CharField(default=Constants.META_KEY_VALUE_NOT_NEED, max_length=200)
	description = models.TextField(default="")
	
	class Meta:
		ordering = ['project__id', '-creation_date']
	
	def __str__(self):
		return self.meta_tag.name + " " + self.value + " " + self.description


class MetaKeyEvents(models.Model):
	"""
	Relation ManyToMany in 
	"""
	meta_tag = models.ForeignKey(MetaKey, related_name='meta_key_event', on_delete=models.PROTECT)
	event = models.ForeignKey(Event, related_name='meta_key_event', on_delete=models.PROTECT)
	owner = models.ForeignKey(User, related_name='meta_key_event', on_delete=models.PROTECT)
	creation_date = models.DateTimeField(db_index=True, auto_now_add=True)
	value = models.CharField(default=Constants.META_KEY_VALUE_NOT_NEED, max_length=200)
	description = models.TextField(default="")
	
	class Meta:
		ordering = ['event__id', '-creation_date']
	
	def __str__(self):
		return self.meta_tag.name + " " + self.value + " " + self.description

class MetaKeyPersonInEvent(models.Model):
	"""
	Relation ManyToMany in 
	"""
	meta_tag = models.ForeignKey(MetaKey, related_name='meta_key_person_in_event', on_delete=models.PROTECT)
	person_in_event = models.ForeignKey(PersonInEvent, related_name='meta_key_person_in_event', on_delete=models.PROTECT)
	owner = models.ForeignKey(User, related_name='meta_key_person_in_event', on_delete=models.PROTECT)
	creation_date = models.DateTimeField(db_index=True, auto_now_add=True)
	value = models.CharField(default=Constants.META_KEY_VALUE_NOT_NEED, max_length=200)
	description = models.TextField(default="")
	
	class Meta:
		ordering = ['person_in_event__id', '-creation_date']
	
	def __str__(self):
		return self.meta_tag.name + " " + self.value + " " + self.description	

class MetaKeyEquipmentInEvent(models.Model):
	"""
	Relation ManyToMany in 
	"""
	meta_tag = models.ForeignKey(MetaKey, related_name='meta_key_equipment_in_event', on_delete=models.PROTECT)
	equipment_in_event = models.ForeignKey(EquipmentInEvent, related_name='meta_key_equipment_in_event', on_delete=models.PROTECT)
	owner = models.ForeignKey(User, related_name='meta_key_equipment_in_event', on_delete=models.PROTECT)
	creation_date = models.DateTimeField(db_index=True, auto_now_add=True)
	value = models.CharField(default=Constants.META_KEY_VALUE_NOT_NEED, max_length=200)
	description = models.TextField(default="")
	
	class Meta:
		ordering = ['equipment_in_event__id', '-creation_date']
	
	def __str__(self):
		return self.meta_tag.name + " " + self.value + " " + self.description	
	
class LazyEncoder(DjangoJSONEncoder):
	def default(self, obj):
		if isinstance(obj, Project):
			return str(obj)
		return super().default(obj)


