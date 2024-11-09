'''
Created on 03/07/2020

@author: mmp
'''
from utils.lock_atomic_transaction import LockedAtomicTransaction
from .models import MetaKey, MetaKeyProjects, MetaKeyEvents, MetaKeyPersonInEvent, MetaKeyEquipmentInEvent

class ManageDatabase(object):
	'''
	classdocs
	'''
	def __init__(self):
		'''
		Constructor
		'''
		pass
	
	def _get_metakey(self, meta_key_name):
		"""
		get metakey with lock table
		"""
		with LockedAtomicTransaction(MetaKey):
			try:
				metaKey = MetaKey.objects.get(name=meta_key_name)
			except MetaKey.DoesNotExist:
				metaKey = MetaKey()
				metaKey.name = meta_key_name
				metaKey.save()
		return metaKey
	

	##########################################################
	## TO projects
	##
	def set_project_metakey(self, project, owner, meta_key_name, value, description):
		"""
		save a meta key
		"""
		metaKey = self._get_metakey(meta_key_name)
		
		metaKey_project = MetaKeyProjects()
		metaKey_project.project = project
		metaKey_project.meta_tag = metaKey
		metaKey_project.owner = owner
		metaKey_project.value = value
		metaKey_project.description = description
		metaKey_project.save()
		return metaKey_project

	def get_project_metakey(self, project, meta_key_name, value = None):
		"""
		value = None, return a list
		"""
		try:
			if (value == None): return MetaKeyProjects.objects.filter(project__id=project.id, meta_tag__name=meta_key_name).order_by('-creation_date')
			return MetaKeyProjects.objects.get(project__id=project.id, meta_tag__name=meta_key_name, value=value)
		except MetaKeyProjects.DoesNotExist:
			return None
	
	def get_project_metakey_last(self, project, meta_key_name, value = None):
		"""
		value = None, return a list
		"""
		try:
			if (value == None): query_set = MetaKeyProjects.objects.filter(project__id=project.id, meta_tag__name=meta_key_name).order_by('-creation_date')
			else: query_set = MetaKeyProjects.objects.filter(project__id=project.id, meta_tag__name=meta_key_name, value=value).order_by('-creation_date')
			if (query_set.count() > 0 ): return query_set[0]
			return None
		except MetaKeyProjects.DoesNotExist:
			return None	
	
	##########################################################
	## TO events
	##
	def set_event_metakey(self, event, owner, meta_key_name, value, description):
		"""
		save a meta key
		"""
		metaKey = self._get_metakey(meta_key_name)
		
		metaKey_event = MetaKeyEvents()
		metaKey_event.event = event
		metaKey_event.meta_tag = metaKey
		metaKey_event.owner = owner
		metaKey_event.value = value
		metaKey_event.description = description
		metaKey_event.save()
		return metaKey_event

	def get_event_metakey(self, event, meta_key_name, value = None):
		"""
		value = None, return a list
		"""
		try:
			if (value == None): return MetaKeyEvents.objects.filter(event__id=event.id, meta_tag__name=meta_key_name).order_by('-creation_date')
			return MetaKeyEvents.objects.get(event__id=event.id, meta_tag__name=meta_key_name, value=value)
		except MetaKeyEvents.DoesNotExist:
			return None
	
	def get_event_metakey_last(self, event, meta_key_name, value = None):
		"""
		value = None, return a list
		"""
		try:
			if (value == None): query_set = MetaKeyEvents.objects.filter(event__id=event.id, meta_tag__name=meta_key_name).order_by('-creation_date')
			else: query_set = MetaKeyEvents.objects.filter(event__id=event.id, meta_tag__name=meta_key_name, value=value).order_by('-creation_date')
			if (query_set.count() > 0 ): return query_set[0]
			return None
		except MetaKeyEvents.DoesNotExist:
			return None
	
	
	##########################################################
	## TO person in events
	##
	def set_person_in_event_metakey(self, person_in_event, owner, meta_key_name, value, description):
		"""
		save a meta key
		"""
		metaKey = self._get_metakey(meta_key_name)
		
		metaKey_person_in_event = MetaKeyPersonInEvent()
		metaKey_person_in_event.person_in_event = person_in_event
		metaKey_person_in_event.meta_tag = metaKey
		metaKey_person_in_event.owner = owner
		metaKey_person_in_event.value = value
		metaKey_person_in_event.description = description
		metaKey_person_in_event.save()
		return metaKey_person_in_event

	def get_person_in_event_metakey(self, person_in_event, meta_key_name, value = None):
		"""
		value = None, return a list
		"""
		try:
			if (value == None): return MetaKeyPersonInEvent.objects.filter(person_in_event__id=person_in_event.id, meta_tag__name=meta_key_name).order_by('-creation_date')
			return MetaKeyPersonInEvent.objects.get(person_in_event__id=person_in_event.id, meta_tag__name=meta_key_name, value=value)
		except MetaKeyPersonInEvent.DoesNotExist:
			return None
	
	def get_person_in_event_metakey_last(self, person_in_event, meta_key_name, value = None):
		"""
		value = None, return a list
		"""
		try:
			if (value == None): query_set = MetaKeyPersonInEvent.objects.filter(person_in_event__id=person_in_event.id, meta_tag__name=meta_key_name).order_by('-creation_date')
			else: query_set = MetaKeyPersonInEvent.objects.filter(person_in_event__id=person_in_event.id, meta_tag__name=meta_key_name, value=value).order_by('-creation_date')
			if (query_set.count() > 0 ): return query_set[0]
			return None
		except MetaKeyPersonInEvent.DoesNotExist:
			return None


	##########################################################
	## TO equipment in events
	##
	def set_equipment_in_event_metakey(self, equipment_in_event, owner, meta_key_name, value, description):
		"""
		save a meta key
		"""
		metaKey = self._get_metakey(meta_key_name)
		
		metaKey_equipment_in_event = MetaKeyEquipmentInEvent()
		metaKey_equipment_in_event.equipment_in_event = equipment_in_event
		metaKey_equipment_in_event.meta_tag = metaKey
		metaKey_equipment_in_event.owner = owner
		metaKey_equipment_in_event.value = value
		metaKey_equipment_in_event.description = description
		metaKey_equipment_in_event.save()
		return metaKey_equipment_in_event

	def get_equipment_in_event_metakey(self, equipment_in_event, meta_key_name, value = None):
		"""
		value = None, return a list
		"""
		try:
			if (value == None): return MetaKeyEquipmentInEvent.objects.filter(equipment_in_event__id=equipment_in_event.id, meta_tag__name=meta_key_name).order_by('-creation_date')
			return MetaKeyEquipmentInEvent.objects.get(equipment_in_event__id=equipment_in_event.id, meta_tag__name=meta_key_name, value=value)
		except MetaKeyEquipmentInEvent.DoesNotExist:
			return None
	
	def get_equipment_in_event_metakey_last(self, equipment_in_event, meta_key_name, value = None):
		"""
		value = None, return a list
		"""
		try:
			if (value == None): query_set = MetaKeyEquipmentInEvent.objects.filter(equipment_in_event__id=equipment_in_event.id, meta_tag__name=meta_key_name).order_by('-creation_date')
			else: query_set = MetaKeyEquipmentInEvent.objects.filter(equipment_in_event__id=equipment_in_event.id, meta_tag__name=meta_key_name, value=value).order_by('-creation_date')
			if (query_set.count() > 0 ): return query_set[0]
			return None
		except MetaKeyEquipmentInEvent.DoesNotExist:
			return None








