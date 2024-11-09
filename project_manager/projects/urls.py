'''
Created on 17/03/2020

@author: mmp
'''
from django.urls import path
from projects import views, ajax_views, views_settings

## same, url is going to be
# url(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive)
# path('articles/<int:year>/', views.year_archive)

urlpatterns = [
		path('projects/', views.ProjectView.as_view(), name='projects'),
		path('project_add/', views.ProjectAddView.as_view(), name='project-add'),
		path('project_update/<int:pk>', views.ProjectUpdateView.as_view(), name='project-update'),
		path('project_events/<int:pk>', views.ProjectEventView.as_view(), name='project-events'),
		
		## events
		path('event_view/<int:pk>/<str:tab_item>', views.EventView.as_view(), name='event-view'),
		path('event_update/<int:pk>', views.EventUpdateView.as_view(), name='event-update'),
		path('event_add/', views.EventAddView.as_view(), name='event-add'),
		
		## research
		path('create_research/', views.ResearchCreateView.as_view(), name='create-research'),
		path('update_research/<int:pk>', views.ResearchUpdateView.as_view(), name='update-research'),
		path('delete_research/<int:pk>', views.ResearchDeleteView.as_view(), name='delete-research'),
		
		## project type
		path('create_project_type/', views.ProjectTypeCreateView.as_view(), name='create-project-type'),
		path('update_project_type/<int:pk>', views.ProjectTypeUpdateView.as_view(), name='update-project-type'),
    	path('delete_project_type/<int:pk>', views.ProjectTypeDeleteView.as_view(), name='delete-project-type'),
    	
    	## specie
		path('create_specie/', views.SpecieCreateView.as_view(), name='create-specie'),
		path('update_specie/<int:pk>', views.SpecieUpdateView.as_view(), name='update-specie'),
    	path('delete_specie/<int:pk>', views.SpecieDeleteView.as_view(), name='delete-specie'),
    	
    	## project type
		path('create_institute/', views.InstituteCreateView.as_view(), name='create-institute'),
		path('update_institute/<int:pk>', views.InstituteUpdateView.as_view(), name='update-institute'),
    	path('delete_institute/<int:pk>', views.InstituteDeleteView.as_view(), name='delete-institute'),
    
    	## event type
		path('create_event_type/', views.EventTypeCreateView.as_view(), name='create-event-type'),
		path('update_event_type/<int:pk>', views.EventTypeUpdateView.as_view(), name='update-event-type'),
    	path('delete_event_type/<int:pk>', views.EventTypeDeleteView.as_view(), name='delete-event-type'),
    	
    	## Equipment
		path('create_equipment/', views.EquipmentCreateView.as_view(), name='create-equipment'),
		path('update_equipment/<int:pk>', views.EquipmentUpdateView.as_view(), name='update-equipment'),
		
    	## man power
		path('create_man_power/', views.PersonInEventCreateView.as_view(), name='create-man-power'),
		path('update_man_power/<int:pk>', views.PersonInEventUpdateView.as_view(), name='update-man-power'),
		path('view_man_power/<int:pk>', views.PersonInEventView.as_view(), name='view-man-power'),
 #   	path('delete_man_power/<int:pk>', views.EventTypeDeleteView.as_view(), name='delete-man-power'),
    	
    	## equipment in Event
		path('create_event_equipment/', views.EquipmentInEventCreateView.as_view(), name='create-event-equipment'),
		path('update_event_equipment/<int:pk>', views.EquipmentInEventUpdateView.as_view(), name='update-event-equipment'),
		path('view_event_equipment/<int:pk>', views.EquipmentInEventView.as_view(), name='view-event-equipment'),
		
    	## Files
    	path('files_add/', views.FileAddView.as_view(), name='files-add'),

		## Settings
		path('settings_research/', views_settings.SettingsResearchView.as_view(), name='settings-research'),
		path('settings_institute/', views_settings.SettingsInstituteView.as_view(), name='settings-institute'),
		path('settings_specie/', views_settings.SettingsSpecieView.as_view(), name='settings-specie'),
		path('settings_project_type/', views_settings.SettingsProjectTypeView.as_view(), name='settings-project-type'),
		path('settings_event_type/', views_settings.SettingsEventTypeView.as_view(), name='settings-event-type'),
		path('settings_equipment/', views_settings.SettingsEquipmentView.as_view(), name='settings-equipment'),
		
		## Regular Ajax	
		path('ajax/remove_project/', ajax_views.remove_project, name='remove-project'),						## remove a project
		path('ajax/remove_event_project/', ajax_views.remove_event_project, name='remove-event-project'),	## remove a event project
		path('ajax/remove_file/', ajax_views.remove_file, name='remove-file'),								## remove a file
		path('ajax/remove_settings/', ajax_views.remove_settings, name='remove-settings'),					## remove something inside settings
		path('ajax/remove_person_in_event/', ajax_views.remove_person_in_event, name='remove-person-in-event'),		## remove person in event
		path('ajax/remove_equipment_in_event/', ajax_views.remove_equipment_in_event, name='remove-equipment-in-event'),	## remove equipment
]




