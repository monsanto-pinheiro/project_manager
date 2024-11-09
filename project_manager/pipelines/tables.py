'''
Created on 19/03/2020

@author: mmp
'''

import os
import django_tables2 as tables
from constants.constants import Constants
from .models import Pipeline
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.conf import settings

class PipelineTable(tables.Table):
#   Renders a normal value as an internal hyperlink to another page.
	name = tables.Column("Name", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	number_of_files = tables.Column("#Files", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	owner = tables.Column("Created by", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	creation_date = tables.Column("Creation Date", orderable=True, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	options = tables.Column("Options", orderable=False, empty_values=(), attrs={"td": {"class": "text-center"}, "th": {"class": "text-center orderable"}})
	constants = Constants()
	
	class Meta:
		model = Pipeline
		fields = ("name", 'creation_date', 'owner', "number_of_files", "options")
		attrs = {"class": "table-striped table-bordered"}
		empty_text = "There are no pipelines to show..."

#	def render_name(self, record):
# 		from crequest.middleware import CrequestMiddleware
# 		current_request = CrequestMiddleware.get_request()
# 		user = current_request.user
# 		"""
# 		get group name that can delete it
# 		"""
# 		if (user.username == record.owner.username and record.project.all().filter(is_deleted=False).count() == 0):	## it can't be in any active project
# 			return mark_safe('<a href="#modal_remove_reference" id="id_remove_reference_modal" data-toggle="modal"' +\
# 					' ref_name="' + record.name + '" pk="' + str(record.pk) + '"><i class="fa fa-trash"></i></span> </a>' + record.name)
#		return record.name;

	def render_creation_date(self, **kwargs):
		record = kwargs.pop("record")
		return record.creation_date.strftime(settings.DATE_FORMAT_FOR_TABLE)

# 	def order_owner(self, queryset, is_descending):
# 		queryset = queryset.annotate(owner_name = F('owner__username')).order_by(('-' if is_descending else '') + 'owner_name')
# 		return (queryset, True)

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
		## Edit
		str_links += '<a href=' + reverse('project-update', args=[record.pk]) + ' data-toggle="tooltip" title="Edit"><span ><i class="fa fa-2x fa-pencil padding-button-table"></i></span></a>'
		## Remove
		str_links += '<a href="#id_remove_project_modal" id="id_remove_project" data-toggle="modal" data-toggle="tooltip" title="Delete"' +\
 					' ref_name="' + record.name + '" pk="' + str(record.pk) + '"><span ><i class="fa fa-2x fa-trash padding-button-table" style="color:red;">' +\
					'</i></span> </a>'
		return mark_safe(str_links)


