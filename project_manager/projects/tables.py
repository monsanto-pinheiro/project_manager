'''
Created on 19/03/2020

@author: mmp
'''

import os
import django_tables2 as tables
from constants.constants import Constants
from projects.models import Project, Event, File, Research, Institute, Specie, ProjectType, EventType, PersonInEvent, EquipmentInEvent
from django.utils.safestring import mark_safe
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.db.models import F

## check tooltip
## comment = tables.TemplateColumn('<data-toggle="tooltip" title="{{record.comment}}">{{record.comment|truncatewords:5}}')

class ProjectTable(tables.Table):
#   Renders a normal value as an internal hyperlink to another page.
	research = tables.Column("Customer", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	reference = tables.Column("Reference ID", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	project_type = tables.Column("Proj.Type", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	number_of_events = tables.Column("Number of Events", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	research = tables.Column("Research", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	options = tables.Column("Options", orderable=False, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	start_date = tables.Column("Start Date", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	owner = tables.Column("Created by", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	constants = Constants()
	
	class Meta:
		model = Project
		fields = ("reference", 'number_of_events', "research", "project_type", 'owner', 'start_date', "options")
		attrs = {"class": "table-striped table-bordered"}
		empty_text = "There are no Projects to show..."

	def render_start_date(self, **kwargs):
		record = kwargs.pop("record")
		return record.start_date.strftime(settings.DATE_FORMAT_FOR_TABLE)

	def order_owner(self, queryset, is_descending):
		queryset = queryset.annotate(owner_name = F('owner__username')).order_by(('-' if is_descending else '') + 'owner_name')
		return (queryset, True)

	def render_number_of_events(self, **kwargs):
		record = kwargs.pop("record")
		return Event.objects.filter(project__id=record.id, is_deleted=False).count()

	def render_reference(self, **kwargs):
		"""
		draw reference and name
		"""
		record = kwargs.pop("record")
		return mark_safe('<a href=' + reverse('project-events', args=[record.pk]) + ' data-toggle="tooltip" title="View">' +\
			record.reference + '</a>')
		
	def render_options(self, **kwargs):
		record = kwargs.pop("record")
		
		## View
		str_links = '<a href=' + reverse('project-events', args=[record.pk]) + ' data-toggle="tooltip" title="View"><span ><i class="fa fa-2x fa-eye padding-button-table"></i></span></a>'

		### test anonymous account
		if (self.request.user.is_superuser and self.request.user.is_active):
			## Edit
			str_links += '<a href=' + reverse('project-update', args=[record.pk]) + ' data-toggle="tooltip" title="Edit"><span ><i class="fa fa-2x fa-pencil padding-button-table"></i></span></a>'
			## Remove
			str_links += '<a href="#id_remove_project_modal" id="id_remove_project" data-toggle="modal" data-toggle="tooltip" title="Delete"' +\
	 					' ref_name="' + record.reference + '" pk="' + str(record.pk) + '"><span ><i class="fa fa-2x fa-trash padding-button-table" style="color:red;">' +\
						'</i></span> </a>'

		return mark_safe(str_links)


class ProjectEventsTable(tables.Table):
#   Renders a normal value as an internal hyperlink to another page.
	event_type = tables.Column("Event Type", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	number_of_files = tables.Column("#Files", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	number_of_persons = tables.Column("#People", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	number_of_hours = tables.Column("#P.Hours", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	owner = tables.Column("Created by", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	creation_date = tables.Column("Creation Date", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	options = tables.Column("Options", orderable=False, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center"}})
	constants = Constants()
	
	class Meta:
		model = Event
		fields = ("event_type", "number_of_files", "number_of_persons", 'number_of_hours', 'creation_date', 'owner', "options")
		attrs = {"class": "table-striped table-bordered"}
		empty_text = "There are no Events to show..."

	def render_creation_date(self, **kwargs):
		record = kwargs.pop("record")
		return record.creation_date.strftime(settings.DATETIME_FORMAT_FOR_TABLE)

	def order_owner(self, queryset, is_descending):
		queryset = queryset.annotate(owner_name = F('owner__username')).order_by(('-' if is_descending else '') + 'owner_name')
		return (queryset, True)

	def render_event_type(self, **kwargs):
		record = kwargs.pop("record")
		return mark_safe('<a href=' + reverse('event-view', kwargs={'pk': record.pk, 'tab_item': 'tab_files'}) +\
			' data-toggle="tooltip" title="View">' + record.event_type.name + '</a>')
		
	def render_number_of_files(self, **kwargs):
		record = kwargs.pop("record")
		return File.objects.filter(event__id=record.id, is_deleted=False).count()
	
	def render_number_of_persons(self, **kwargs):
		record = kwargs.pop("record")
		return PersonInEvent.objects.filter(event__id=record.id, is_deleted=False).count()
	
	def render_number_of_hours(self, **kwargs):
		record = kwargs.pop("record")
		total_hours = 0
		for person_in_event in list(PersonInEvent.objects.filter(event__id=record.id, is_deleted=False)):
			total_hours += person_in_event.number_of_hours
		return total_hours

	def render_options(self, **kwargs):
		record = kwargs.pop("record")
		
		## View
		str_links = '<a href=' + mark_safe(reverse('event-view', kwargs={'pk': record.pk, 'tab_item': 'tab_files'})) +\
			' data-toggle="tooltip" title="View"><span ><i class="fa fa-2x fa-eye padding-button-table"></i></span></a>'
		
		### test anonymous account
		if (self.request.user.is_superuser and self.request.user.is_active):
			## Edit
			str_links += '<a href=' + mark_safe(reverse('event-update', kwargs={'pk': record.pk})) + ' data-toggle="tooltip" title="Edit"><span><i class="fa fa-2x fa-pencil padding-button-table"></i></span></a>'
			## Remove
			str_links += '<a href="#id_remove_event_modal" id="id_remove_event" data-toggle="modal" data-toggle="tooltip" title="Delete"' +\
	 					' ref_name="' + record.event_type.name + '" pk="' + str(record.pk) + '"><span ><i class="fa fa-2x fa-trash padding-button-table" style="color:red;">' +\
						'</i></span> </a>'
		return mark_safe(str_links)


class FilesEventTable(tables.Table):
#   Renders a normal value as an internal hyperlink to another page.
	file_name = tables.Column("Name", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	owner = tables.Column("Created by", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	creation_date = tables.Column("Creation Date", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	is_valid = tables.Column("Is it Valid?", orderable=False, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	
	## you can remove, download or view
	options = tables.Column("Options", orderable=False, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center"}})
	constants = Constants()
	
	class Meta:
		model = File
		fields = ('file_name', 'creation_date', 'owner', 'is_valid', "options")
		attrs = {"class": "table-striped table-bordered"}
		empty_text = "There are no Files to show..."

	def render_creation_date(self, **kwargs):
		record = kwargs.pop("record")
		return record.creation_date.strftime(settings.DATETIME_FORMAT_FOR_TABLE)

	def render_is_valid(self, **kwargs):
		record = kwargs.pop("record")
		if (record.is_a_valid_hash()): return mark_safe('<img title="Validation signature: is valid" class="tip" src="{}">'.format(
			os.path.join("/" + Constants.DIR_STATIC, Constants.DIR_ICONS, Constants.ICON_GREEN_32_32)))
		else: return mark_safe('<img title="Validation signature: is not valid" class="tip" src="{}">'.format(
			os.path.join("/" + Constants.DIR_STATIC, Constants.DIR_ICONS, Constants.ICON_RED_32_32)))
		
	def order_owner(self, queryset, is_descending):
		queryset = queryset.annotate(owner_name = F('owner__username')).order_by(('-' if is_descending else '') + 'owner_name')
		return (queryset, True)

	def render_file_name(self, **kwargs):
		record = kwargs.pop("record")
		return record.get_path_web()

	def render_options(self, **kwargs):
		record = kwargs.pop("record")
		
		## Download
		str_links = '<a href="{}" data-toggle="tooltip" title="Download" download>'.format(record.get_only_path_web()) +\
					'<span><i class="fa fa-2x fa-download padding-button-table"></i></span></a>'
		
		### test anonymous account
		if (self.request.user.is_superuser and self.request.user.is_active):
			## Remove
			str_links += '<a href="#id_remove_file_modal" id="id_remove_file" data-toggle="modal" data-toggle="tooltip" title="Delete"' +\
 					' ref_name="' + record.file_name + '" pk="' + str(record.pk) + '"><span ><i class="fa fa-2x fa-trash padding-button-table" style="color:red;">' +\
					'</i></span> </a>'
		return mark_safe(str_links)


class ManPowerEventTable(tables.Table):
#   Renders a normal value as an internal hyperlink to another page.
	person = tables.Column("Person", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	number_of_hours = tables.Column("#Hours", orderable=False, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center"}})
	description = tables.Column("Description", orderable=False, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center"}})
	owner = tables.Column("Created by", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	creation_date = tables.Column("Creation Date", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	
	options = tables.Column("Options", orderable=False, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center"}})
	## you can remove, download or view
	constants = Constants()
	
	class Meta:
		model = PersonInEvent
		fields = ('person', 'number_of_hours', 'description', 'owner', 'creation_date', 'options')
		attrs = {"class": "table-striped table-bordered"}
		empty_text = "There are no man power to show..."

	def render_person(self, **kwargs):
		record = kwargs.pop("record")
		return mark_safe('<a href="javascript:;" data-toggle="tooltip" title="View" id="id_view_man_edit_modal" ' +\
					'data-id="/projects/view_man_power/' + str(record.pk) + '" class="view-man-power" data-reverse="event-view">' +\
 					record.person.username + '</a>')

	def render_creation_date(self, **kwargs):
		record = kwargs.pop("record")
		return record.creation_date.strftime(settings.DATETIME_FORMAT_FOR_TABLE)

	def render_description(self, **kwargs):
		record = kwargs.pop("record")
		if len(record.description) > 15: record.description[:15] + "..."
		return record.description
	
	def order_owner(self, queryset, is_descending):
		queryset = queryset.annotate(owner_name = F('owner__username')).order_by(('-' if is_descending else '') + 'owner_name')
		return (queryset, True)
	
	def order_person(self, queryset, is_descending):
		queryset = queryset.annotate(person_name = F('person__username')).order_by(('-' if is_descending else '') + 'person_name')
		return (queryset, True)

	def render_options(self, **kwargs):
		record = kwargs.pop("record")

		str_links = '<a href="javascript:;" data-toggle="tooltip" title="View" id="id_view_man_edit_modal" ' +\
					'data-id="/projects/view_man_power/' + str(record.pk) + '" class="view-man-power" data-reverse="event-view">' +\
 					'<span><i class="fa fa-2x fa-eye padding-button-table"></i></span></a>'
		
		### test anonymous account
		if (self.request.user.is_superuser and self.request.user.is_active):
			## Update
			str_links += '<a href="javascript:;" data-toggle="tooltip" title="Edit" id="id_update_man_edit_modal" ' +\
						'data-id="/projects/update_man_power/' + str(record.pk) + '" class="update-man-power" data-reverse="event-view">' +\
	 					'<span><i class="fa fa-2x fa-pencil padding-button-table"></i></span></a>'
			
			## Remove
			str_links += '<a href="#id_remove_person_in_even_modal" id="id_remove_person_in_event" data-toggle="modal" data-toggle="tooltip" title="Delete"' +\
	 					' ref_name="' + record.person.username + '" hours_of_work="' + ", with {} hour{}".format(record.number_of_hours,\
						"" if (record.number_of_hours == 1) else "s") +\
	 					'" pk="' + str(record.pk) + '"><span ><i class="fa fa-2x fa-trash padding-button-table" style="color:red;">' +\
						'</i></span> </a>'
		return mark_safe(str_links)
	

class EquipmentEventTable(tables.Table):
#   Renders a normal value as an internal hyperlink to another page.
	equipment = tables.Column("Equipment", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	number_of_hours = tables.Column("#Hours", orderable=False, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center"}})
	description = tables.Column("Description", orderable=False, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center"}})
	owner = tables.Column("Created by", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	creation_date = tables.Column("Creation Date", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	
	options = tables.Column("Options", orderable=False, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center"}})
	## you can remove, download or view
	constants = Constants()
	
	class Meta:
		model = EquipmentInEvent
		fields = ('equipment', 'number_of_hours', 'description', 'owner', 'creation_date', 'options')
		attrs = {"class": "table-striped table-bordered"}
		empty_text = "There are no man power to show..."

	def render_equipment(self, **kwargs):
		record = kwargs.pop("record")
		tag_equipment = "View equipment" if record.equipment.ip is None else "View equipment, IP:" + str(record.equipment.ip)
		return mark_safe('<a href="javascript:;" data-toggle="tooltip" title="' + tag_equipment + '" id="id_view_equipment_edit_modal" ' +\
					'data-id="/projects/view_event_equipment/' + str(record.pk) + '" class="view-event-equipment" data-reverse="event-view">' +\
 					record.equipment.name+ '</a>')

	def render_creation_date(self, **kwargs):
		record = kwargs.pop("record")
		return record.creation_date.strftime(settings.DATETIME_FORMAT_FOR_TABLE)

	def render_description(self, **kwargs):
		record = kwargs.pop("record")
		if len(record.description) > 15: record.description[:15] + "..."
		return record.description
	
	def order_owner(self, queryset, is_descending):
		queryset = queryset.annotate(owner_name = F('owner__username')).order_by(('-' if is_descending else '') + 'owner_username')
		return (queryset, True)
	
	def order_equipment(self, queryset, is_descending):
		queryset = queryset.annotate(equipment_name = F('equipment__name')).order_by(('-' if is_descending else '') + 'equipment_name')
		return (queryset, True)

	def render_options(self, **kwargs):
		record = kwargs.pop("record")

		str_links = '<a href="javascript:;" data-toggle="tooltip" title="View" id="id_view_man_edit_modal" ' +\
					'data-id="/projects/view_event_equipment/' + str(record.pk) + '" class="view-event-equipment" data-reverse="event-view">' +\
 					'<span><i class="fa fa-2x fa-eye padding-button-table"></i></span></a>'
		
		### test anonymous account
		if (self.request.user.is_superuser and self.request.user.is_active):
			## Update
			str_links += '<a href="javascript:;" data-toggle="tooltip" title="Edit" id="id_update_man_edit_modal" ' +\
						'data-id="/projects/update_event_equipment/' + str(record.pk) + '" class="update-event-equipment" data-reverse="event-view">' +\
	 					'<span><i class="fa fa-2x fa-pencil padding-button-table"></i></span></a>'
			
			## Remove
			str_links += '<a href="#id_remove_equipment_in_even_modal" id="id_remove_equipment_in_event" data-toggle="modal" data-toggle="tooltip" title="Delete"' +\
	 					' ref_name="' + record.equipment.name + '" hours_of_work="' + ", with {} hour{}".format(record.number_of_hours,\
						"" if (record.number_of_hours == 1) else "s") +\
	 					'" pk="' + str(record.pk) + '"><span ><i class="fa fa-2x fa-trash padding-button-table" style="color:red;">' +\
						'</i></span> </a>'
		return mark_safe(str_links)


class ResearchTable(tables.Table):
#   Renders a normal value as an internal hyperlink to another page.
	_name_data = tables.Column("Name", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	_email_data = tables.Column("Email", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	_phone_data = tables.Column("Phone", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	owner = tables.Column("Created by", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	creation_date = tables.Column("Creation Date", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	
	## you can remove, download or view
	options = tables.Column("Options", orderable=False, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	constants = Constants()
	
	class Meta:
		model = Research
		fields = ('_name_data', '_email_data', '_phone_data', 'creation_date', 'owner', "options")
		attrs = {"class": "table-striped table-bordered"}
		empty_text = "There are no Researches to show..."

	def render_creation_date(self, **kwargs):
		record = kwargs.pop("record")
		return record.creation_date.strftime(settings.DATETIME_FORMAT_FOR_TABLE)

	def order_owner(self, queryset, is_descending):
		queryset = queryset.annotate(owner_name = F('owner__username')).order_by(('-' if is_descending else '') + 'owner_username')
		return (queryset, True)

	def render_options(self, **kwargs):
		record = kwargs.pop("record")
		
		str_links = ""
		### test anonymous account
		if (self.request.user.is_superuser and self.request.user.is_active):
			## Update
			str_links = '<a href="javascript:;" data-toggle="tooltip" title="Edit" id="id_research_edit_modal" ' +\
						'data-id="/projects/update_research/' + str(record.pk) + '" class="update-research" data-reverse="settings-research">' +\
	 					'<span><i class="fa fa-2x fa-pencil padding-button-table"></i></span></a>'
	
			## Remove
			str_links += '<a href="#id_remove_settings_modal" id="id_remove_settings" data-toggle="modal" data-toggle="tooltip" title="Delete" ' +\
	 					'ref_name="' + record.name + '" pk="' + str(record.pk) + '" message_header="Remove Research" ' +\
	 					'table_name="research"><span >' +\
	 					'<i class="fa fa-2x fa-trash padding-button-table" style="color:red;">' +\
						'</i></span> </a>'
		return mark_safe(str_links)


class InstituteTable(tables.Table):
#   Renders a normal value as an internal hyperlink to another page.
	name = tables.Column("Name", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	abbreviation = tables.Column("Abbreviation", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	city = tables.Column("City", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	owner = tables.Column("Created by", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	creation_date = tables.Column("Creation Date", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	
	## you can remove, download or view
	options = tables.Column("Options", orderable=False, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	constants = Constants()
	
	class Meta:
		model = Institute
		fields = ('name', 'abbreviation', 'city', 'creation_date', 'owner', "options")
		attrs = {"class": "table-striped table-bordered"}
		empty_text = "There are no Institute to show..."

	def render_creation_date(self, **kwargs):
		record = kwargs.pop("record")
		return record.creation_date.strftime(settings.DATETIME_FORMAT_FOR_TABLE)

	def order_owner(self, queryset, is_descending):
		queryset = queryset.annotate(owner_name = F('owner__username')).order_by(('-' if is_descending else '') + 'owner_name')
		return (queryset, True)

	def render_options(self, **kwargs):
		record = kwargs.pop("record")
		
		str_links = ""
		### test anonymous account
		if (self.request.user.is_superuser and self.request.user.is_active):
			## Update
			str_links = '<a href="javascript:;" data-toggle="tooltip" title="Edit" id="id_institute_edit_modal" ' +\
						'data-id="/projects/update_institute/' + str(record.pk) + '" class="update-institute" data-reverse="settings-institute">' +\
	 					'<span><i class="fa fa-2x fa-pencil padding-button-table"></i></span></a>'
	
			## Remove
			str_links += '<a href="#id_remove_settings_modal" id="id_remove_settings" data-toggle="modal" data-toggle="tooltip" title="Delete" ' +\
	 					'ref_name="' + record.name + '" pk="' + str(record.pk) + '" message_header="Remove Institute" ' +\
	 					'table_name="institute"><span >' +\
	 					'<i class="fa fa-2x fa-trash padding-button-table" style="color:red;">' +\
						'</i></span> </a>'
		return mark_safe(str_links)

class SpecieTable(tables.Table):
#   Renders a normal value as an internal hyperlink to another page.
	name = tables.Column("Name", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	owner = tables.Column("Created by", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	creation_date = tables.Column("Creation Date", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	
	## you can remove, download or view
	options = tables.Column("Options", orderable=False, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	constants = Constants()
	
	class Meta:
		model = Specie
		fields = ('name', 'creation_date', 'owner', "options")
		attrs = {"class": "table-striped table-bordered"}
		empty_text = "There are no Species to show..."

	def render_creation_date(self, **kwargs):
		record = kwargs.pop("record")
		return record.creation_date.strftime(settings.DATETIME_FORMAT_FOR_TABLE)

	def order_owner(self, queryset, is_descending):
		queryset = queryset.annotate(owner_name = F('owner__username')).order_by(('-' if is_descending else '') + 'owner_name')
		return (queryset, True)

	def render_options(self, **kwargs):
		record = kwargs.pop("record")
		
		str_links = ""
		### test anonymous account
		if (self.request.user.is_superuser and self.request.user.is_active):
			## Update
			str_links = '<a href="javascript:;" data-toggle="tooltip" title="Edit" id="id_specie_edit_modal" ' +\
						'data-id="/projects/update_specie/' + str(record.pk) + '" class="update-specie" data-reverse="settings-specie">' +\
	 					'<span><i class="fa fa-2x fa-pencil padding-button-table"></i></span></a>'
	
			## Remove
			str_links += '<a href="#id_remove_settings_modal" id="id_remove_settings" data-toggle="modal" data-toggle="tooltip" title="Delete" ' +\
	 					'ref_name="' + record.name + '" pk="' + str(record.pk) + '" message_header="Remove Specie" ' +\
	 					'table_name="specie"><span >' +\
	 					'<i class="fa fa-2x fa-trash padding-button-table" style="color:red;">' +\
						'</i></span> </a>'
		return mark_safe(str_links)
	

class EventTypeTable(tables.Table):
#   Renders a normal value as an internal hyperlink to another page.
	name = tables.Column("Name", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	description = tables.Column("Description", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	owner = tables.Column("Created by", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	creation_date = tables.Column("Creation Date", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	
	## you can remove, download or view
	options = tables.Column("Options", orderable=False, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	constants = Constants()
	
	class Meta:
		model = EventType
		fields = ('name', 'description', 'creation_date', 'owner', "options")
		attrs = {"class": "table-striped table-bordered"}
		empty_text = "There are no Event Types to show..."

	def render_creation_date(self, **kwargs):
		record = kwargs.pop("record")
		return record.creation_date.strftime(settings.DATETIME_FORMAT_FOR_TABLE)

	def order_owner(self, queryset, is_descending):
		queryset = queryset.annotate(owner_name = F('owner__username')).order_by(('-' if is_descending else '') + 'owner_name')
		return (queryset, True)

	def render_options(self, **kwargs):
		record = kwargs.pop("record")
		
		str_links = ""
		### test anonymous account
		if (self.request.user.is_superuser and self.request.user.is_active):
			## Update
			str_links = '<a href="javascript:;" data-toggle="tooltip" title="Edit" id="id_event_type_edit_modal" ' +\
						'data-id="/projects/update_event_type/' + str(record.pk) + '" class="update-event_type" data-reverse="settings-event-type">' +\
	 					'<span><i class="fa fa-2x fa-pencil padding-button-table"></i></span></a>'
	
			## Remove
			str_links += '<a href="#id_remove_settings_modal" id="id_remove_settings" data-toggle="modal" data-toggle="tooltip" title="Delete" ' +\
	 					'ref_name="' + record.name + '" pk="' + str(record.pk) + '" message_header="Remove Event Type" ' +\
	 					'table_name="event_type"><span >' +\
	 					'<i class="fa fa-2x fa-trash padding-button-table" style="color:red;">' +\
						'</i></span> </a>'
		return mark_safe(str_links)



class EquipmentTable(tables.Table):
#   Renders a normal value as an internal hyperlink to another page.
	name = tables.Column("Name", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	room = tables.Column("Room", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	ip = tables.Column("IP address", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	description = tables.Column("Description", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	owner = tables.Column("Created by", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	creation_date = tables.Column("Creation Date", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	
	## you can remove, download or view
	options = tables.Column("Options", orderable=False, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	constants = Constants()
	
	class Meta:
		model = EventType
		fields = ('name', 'room', 'ip', 'description', 'creation_date', 'owner', "options")
		attrs = {"class": "table-striped table-bordered"}
		empty_text = "There are no Event Types to show..."

	def render_creation_date(self, **kwargs):
		record = kwargs.pop("record")
		return record.creation_date.strftime(settings.DATETIME_FORMAT_FOR_TABLE)
	
	def render_ip(self, **kwargs):
		record = kwargs.pop("record")
		return "" if record.ip is None else record.ip

	def order_owner(self, queryset, is_descending):
		queryset = queryset.annotate(owner_name = F('owner__username')).order_by(('-' if is_descending else '') + 'owner_name')
		return (queryset, True)

	def render_options(self, **kwargs):
		record = kwargs.pop("record")
		
		str_links = ""
		### test anonymous account
		if (self.request.user.is_superuser and self.request.user.is_active):
			## Update
			str_links = '<a href="javascript:;" data-toggle="tooltip" title="Edit" id="id_equipment_edit_modal" ' +\
						'data-id="/projects/update_equipment/' + str(record.pk) + '" class="update-equipment" data-reverse="settings-equipment">' +\
	 					'<span><i class="fa fa-2x fa-pencil padding-button-table"></i></span></a>'
	
			## Remove
			str_links += '<a href="#id_remove_settings_modal" id="id_remove_settings" data-toggle="modal" data-toggle="tooltip" title="Delete" ' +\
	 					'ref_name="' + record.name + '" pk="' + str(record.pk) + '" message_header="Remove Equipment" ' +\
	 					'table_name="equipment"><span >' +\
	 					'<i class="fa fa-2x fa-trash padding-button-table" style="color:red;">' +\
						'</i></span> </a>'
		return mark_safe(str_links)
	

class ProjectTypeTable(tables.Table):
#   Renders a normal value as an internal hyperlink to another page.
	name = tables.Column("Name", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	abbreviation = tables.Column("Abbreviation", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	description = tables.Column("Description", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	owner = tables.Column("Created by", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	creation_date = tables.Column("Creation Date", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	
	## you can remove, download or view
	options = tables.Column("Options", orderable=False, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	constants = Constants()
	
	class Meta:
		model = ProjectType
		fields = ('name', 'abbreviation', 'description', 'creation_date', 'owner', "options")
		attrs = {"class": "table-striped table-bordered"}
		empty_text = "There are no Project Types to show..."

	def render_creation_date(self, **kwargs):
		record = kwargs.pop("record")
		return record.creation_date.strftime(settings.DATETIME_FORMAT_FOR_TABLE)

	def order_owner(self, queryset, is_descending):
		queryset = queryset.annotate(owner_name = F('owner__username')).order_by(('-' if is_descending else '') + 'owner_name')
		return (queryset, True)

	def render_options(self, **kwargs):
		record = kwargs.pop("record")
		
		str_links = ""
		### test anonymous account
		if (self.request.user.is_superuser and self.request.user.is_active):
			## Update
			str_links = '<a href="javascript:;" data-toggle="tooltip" title="Edit" id="id_project_type_edit_modal" ' +\
						'data-id="/projects/update_project_type/' + str(record.pk) + '" class="update-project_type" data-reverse="settings-project-type">' +\
	 					'<span><i class="fa fa-2x fa-pencil padding-button-table"></i></span></a>'
	
			## Remove
			str_links += '<a href="#id_remove_settings_modal" id="id_remove_settings" data-toggle="modal" data-toggle="tooltip" title="Delete" ' +\
	 					'ref_name="' + record.name + '" pk="' + str(record.pk) + '" message_header="Remove Project Type" ' +\
	 					'table_name="project_type"><span >' +\
	 					'<i class="fa fa-2x fa-trash padding-button-table" style="color:red;">' +\
						'</i></span> </a>'
		return mark_safe(str_links)










