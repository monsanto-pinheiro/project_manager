'''
Created on Dec 6, 2017

@author: mmp
'''

import logging

from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.db import transaction
from django.http import JsonResponse
from constants.meta_key_values import MetaKeyAndValue
from projects.models import Project, Event, File, Research, Specie, Institute, EventType, ProjectType
from projects.models import PersonInEvent, Equipment, EquipmentInEvent
from projects.manage_database import ManageDatabase
from utils.lock_atomic_transaction import LockedAtomicTransaction
from django.db.models import ProtectedError

### Logger
logger_debug = logging.getLogger("projectManager.debug")
logger_production = logging.getLogger("projectManager.production")
	

@transaction.atomic
@csrf_protect
def remove_project(request):
	"""
	remove a project.
	"""
	if request.is_ajax():
		data = { 'is_ok' : False }
		project_id_a = 'project_id'
		
		if (project_id_a in request.GET):
			
			## some pre-requisites
			if (not request.user.is_active or not request.user.is_superuser):
				data['message'] = "User without credentials to remove a project."
				return JsonResponse(data)
			
			with LockedAtomicTransaction(Project):
				project_id = request.GET[project_id_a]
				try:
					project = Project.objects.get(pk=project_id)
				except Project.DoesNotExist:
					data['message'] = "Project id does not exist."
					return JsonResponse(data)
				
				### now you can remove
				project.is_deleted = True
				project.delete_date = datetime.now()
				project.delete_owner = request.user
				project.save()
				
				### set the possible update from the previous
				manage_database = ManageDatabase()
				manage_database.set_project_metakey(project, request.user,\
					MetaKeyAndValue.META_KEY_project_delete, MetaKeyAndValue.META_VALUE_Success,
					project.to_json())
			
			data = { 'is_ok' : True }
			data['message'] = "Project '{}' was removed.".format(project.reference)
		return JsonResponse(data)


@transaction.atomic
@csrf_protect
def remove_event_project(request):
	"""
	remove a project sample.
	"""
	if request.is_ajax():
		data = { 'is_ok' : False }
		event_id_a = 'event_id'
		
		if (event_id_a in request.GET):
			
			## some pre-requisites
			if (not request.user.is_active or not request.user.is_superuser):
				data['message'] = "User without credentials to remove a project."
				return JsonResponse(data)
			
			event_id = request.GET[event_id_a]
			
			with LockedAtomicTransaction(Event):
				try:
					event = Event.objects.get(pk=event_id)
				except Event.DoesNotExist:
					return JsonResponse(data)
				
				### now you can remove
				event.is_deleted = True
				event.delete_owner = request.user
				event.delete_date = datetime.now()
				event.save()
				
				### set the possible update from the previous
				manage_database = ManageDatabase()
				manage_database.set_event_metakey(event, request.user,\
					MetaKeyAndValue.META_KEY_event_delete, MetaKeyAndValue.META_VALUE_Success,
					event.to_json())
				
			data = { 'is_ok' : True }
			data['message'] = "Event '{}' was removed.".format(event.event_type.name)
			
		return JsonResponse(data)


@transaction.atomic
@csrf_protect
def remove_file(request):
	"""
	remove a file
	"""
	if request.is_ajax():
		data = { 'is_ok' : False }
		file_id_a = 'file_id'
		
		if (file_id_a in request.GET):
			
			## some pre-requisites
			if (not request.user.is_active or not request.user.is_superuser):
				data['message'] = "User without credentials to remove a project."
				return JsonResponse(data)
			
			file_id = request.GET[file_id_a]
			
			with LockedAtomicTransaction(File):
				try:
					file = File.objects.get(pk=file_id)
				except File.DoesNotExist:
					return JsonResponse(data)
				
				### now you can remove
				file.is_deleted = True
				file.delete_owner = request.user
				file.delete_date = datetime.now()
				file.save()
			data = { 'is_ok' : True }
			data['message'] = "File '{}' was removed.".format(file.file_name)
			
		return JsonResponse(data)

@transaction.atomic
@csrf_protect
def remove_person_in_event(request):
	"""
	remove a file
	"""
	if request.is_ajax():
		data = { 'is_ok' : False }
		man_power_id_a = 'man_power_id'
		
		if (man_power_id_a in request.GET):
			
			## some pre-requisites
			if (not request.user.is_active or not request.user.is_superuser):
				data['message'] = "User without credentials to remove a project."
				return JsonResponse(data)
			
			man_power_id = request.GET[man_power_id_a]
			with LockedAtomicTransaction(PersonInEvent), LockedAtomicTransaction(Project):
				try:
					person_in_event = PersonInEvent.objects.get(pk=man_power_id)
				except PersonInEvent.DoesNotExist:
					return JsonResponse(data)
				
				### now you can remove
				person_in_event.is_deleted = True
				person_in_event.delete_owner = request.user
				person_in_event.delete_date = datetime.now()
				person_in_event.save()
				
				### set the possible update from the previous
				manage_database = ManageDatabase()
				manage_database.set_person_in_event_metakey(person_in_event, request.user,\
					MetaKeyAndValue.META_KEY_person_in_event_delete, MetaKeyAndValue.META_VALUE_Success,
					person_in_event.to_json())
				
				### update time and people in the project
				project = Project.objects.get(id=person_in_event.event.project.id)
				project.update_people_and_time()
			
			data = { 'is_ok' : True }
			data['message'] = "Person '{}' was removed from the event.".format(person_in_event.person.username)
			
		return JsonResponse(data)
	
@transaction.atomic
@csrf_protect
def remove_equipment_in_event(request):
	"""
	remove a file
	"""
	if request.is_ajax():
		data = { 'is_ok' : False }
		equipment_event_id_a = 'equipment_event_id'
		
		if (equipment_event_id_a in request.GET):
			
			## some pre-requisites
			if (not request.user.is_active or not request.user.is_superuser):
				data['message'] = "User without credentials to remove a project."
				return JsonResponse(data)
			
			equipment_event_id = request.GET[equipment_event_id_a]
			with LockedAtomicTransaction(EquipmentInEvent), LockedAtomicTransaction(Project):
				try:
					equipment_in_event = EquipmentInEvent.objects.get(pk=equipment_event_id)
				except EquipmentInEvent.DoesNotExist:
					return JsonResponse(data)
				
				### now you can remove
				equipment_in_event.is_deleted = True
				equipment_in_event.delete_owner = request.user
				equipment_in_event.delete_date = datetime.now()
				equipment_in_event.save()
				
				### set the possible update from the previous
				manage_database = ManageDatabase()
				manage_database.set_equipment_in_event_metakey(equipment_in_event, request.user,\
					MetaKeyAndValue.META_KEY_equipment_in_event_delete, MetaKeyAndValue.META_VALUE_Success,
					equipment_in_event.to_json())
				
				### update time in the project
				project = Project.objects.get(id=equipment_in_event.event.project.id)
				project.update_equipment_hours()
			
			data = { 'is_ok' : True }
			data['message'] = "Equipment '{}' was removed from the event.".format(equipment_in_event.equipment.name)
			
		return JsonResponse(data)
	
@transaction.atomic
@csrf_protect
def remove_settings(request):
	"""
	remove a file
	"""
	if request.is_ajax():
		data = { 'is_ok' : False }
		table_id = 'table_id'
		table_name = 'table_name'
		
		## some pre-requisites
		if (not request.user.is_active or not request.user.is_superuser):
			data['message'] = "User without credentials to remove a project."
			return JsonResponse(data)
			
		if (table_id in request.GET and table_name in request.GET):
			
			table_name = request.GET[table_name]
			pk = request.GET[table_id]
			
			## research
			if table_name == 'research':
				with LockedAtomicTransaction(Research):
					try:
						research = Research.objects.get(pk=pk)
					except Research.DoesNotExist:
						return JsonResponse(data)
					
					### now you can remove
					try:
						research.delete()
					except ProtectedError as e:
						data['message'] = "Cannot delete some instances of model 'Research' because " +\
        						"they are referenced through a protected foreign key."
						return JsonResponse(data)
				data = { 'is_ok' : True }
				data['message'] = "Research '{}' was removed.".format(research.name)
			## Specie
			elif table_name == 'specie':
				with LockedAtomicTransaction(Specie):
					try:
						specie = Specie.objects.get(pk=pk)
					except Specie.DoesNotExist:
						return JsonResponse(data)
					
					### now you can remove
					try:
						specie.delete()
					except ProtectedError as e:
						data['message'] = "Cannot delete some instances of model 'Specie' because " +\
        						"they are referenced through a protected foreign key."
						return JsonResponse(data)
				data = { 'is_ok' : True }
				data['message'] = "Specie '{}' was removed.".format(specie.name)
			## Institute
			elif table_name == 'institute':
				with LockedAtomicTransaction(Institute):
					try:
						institute = Institute.objects.get(pk=pk)
					except Institute.DoesNotExist:
						return JsonResponse(data)
					
					### now you can remove
					try:
						institute.delete()
					except ProtectedError as e:
						data['message'] = "Cannot delete some instances of model 'Institute' because " +\
        						"they are referenced through a protected foreign key."
						return JsonResponse(data)
				data = { 'is_ok' : True }
				data['message'] = "Institute '{}' was removed.".format(institute.name)
			## EventType
			elif table_name == 'event_type':
				with LockedAtomicTransaction(EventType):
					try:
						eventtype = EventType.objects.get(pk=pk)
					except EventType.DoesNotExist:
						return JsonResponse(data)
					
					### now you can remove
					try:
						eventtype.delete()
					except ProtectedError as e:
						data['message'] = "Cannot delete some instances of model 'EventType' because " +\
        						"they are referenced through a protected foreign key."
						return JsonResponse(data)
				data = { 'is_ok' : True }
				data['message'] = "EventType '{}' was removed.".format(eventtype.name)
			## ProjectType
			elif table_name == 'project_type':
				with LockedAtomicTransaction(ProjectType):
					try:
						projecttype = ProjectType.objects.get(pk=pk)
					except ProjectType.DoesNotExist:
						return JsonResponse(data)
					
					### now you can remove
					try:
						projecttype.delete()
					except ProtectedError as e:
						data['message'] = "Cannot delete some instances of model 'ProjectType' because " +\
        						"they are referenced through a protected foreign key."
						return JsonResponse(data)
				data = { 'is_ok' : True }
				data['message'] = "ProjectType '{}' was removed.".format(projecttype.name)
			## Equipment
			elif table_name == 'equipment':
				with LockedAtomicTransaction(Equipment):
					try:
						equipment = Equipment.objects.get(pk=pk)
					except Equipment.DoesNotExist:
						return JsonResponse(data)
					
					### now you can remove
					try:
						equipment.delete()
					except ProtectedError as e:
						data['message'] = "Cannot delete some instances of model 'Equipment' because " +\
        						"they are referenced through a protected foreign key."
						return JsonResponse(data)
				data = { 'is_ok' : True }
				data['message'] = "Equipment '{}' was removed.".format(equipment.name)
			
		return JsonResponse(data)


