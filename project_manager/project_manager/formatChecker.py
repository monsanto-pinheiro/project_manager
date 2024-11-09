from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
import logging

## logging
logger_debug = logging.getLogger("project_manager.debug")
logger_production = logging.getLogger("project_manager.production")

class ContentTypeRestrictedFileField(FileField):
	"""
	Same as FileField, but you can specify:
		* content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg', 'video/x-msvideo', 'video/mp4', 'audio/mpeg', 'txt/css', 
						'application/octet-stream']
		* max_upload_size - a number indicating the maximum file size allowed for upload.
			#	2.5MB -   2621440
			#	5MB   -   5242880
			#	10MB  -  10485760
			#	20MB  -  20971520
			#	50MB  -  52428800
			#	100MB - 104857600
			#	250MB - 214958080
			#	500MB - 429916160
	"""
	

	
	def __init__(self, *args, **kwargs):
		if ("max_upload_size" in kwargs): self.max_upload_size = kwargs.pop("max_upload_size")
		else: self.max_upload_size = 10
		if ("content_types" in kwargs): self.content_types = kwargs.pop("content_types")
		else: self.content_types = ['application/pdf', 'txt/css']
		
		super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

	def clean(self, *args, **kwargs):
		data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)
		try:
			file = data.file
			content_type = file.content_type
			
			### Important to catch the content_type
			message = "Read '{}' size '{}' content type: {}".format(file.name, file.size, content_type) 
			logger_production.info(message)
			logger_debug.info(message)
			if content_type in self.content_types:
				if file.size > self.max_upload_size:
					message = _('Please keep file size under %s. Current file size %s') % (filesizeformat(self.max_upload_size), filesizeformat(file._size))
					logger_debug.warning(message)
					logger_production.warning(message)
					raise forms.ValidationError(message)
			else:
				message = _("File type '{}' not supported.".format(content_type))
				logger_debug.warning(message)
				logger_production.warning(message)
				raise forms.ValidationError(message)
		except AttributeError:
			raise forms.ValidationError(_("File not supported."))
		return data

class ContentTypeRestrictedFileFieldForm(forms.FileField):
	"""
	To use on the forms directly
	Same as FileField, but you can specify:
		* content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg', 'video/x-msvideo', 'video/mp4', 'audio/mpeg', 'txt/css', 
						'application/octet-stream']
		* max_upload_size - a number indicating the maximum file size allowed for upload.
			#	2.5MB -   2621440
			#	5MB   -   5242880
			#	10MB  -  10485760
			#	20MB  -  20971520
			#	50MB  -  52428800
			#	100MB - 104857600
			#	250MB - 214958080
			#	500MB - 429916160
	"""
	
	## logging
	logger_debug = logging.getLogger("project_manager.debug")
	logger_production = logging.getLogger("project_manager.production")
	
	def __init__(self, *args, **kwargs):
		self.max_upload_size = None
		if ("max_upload_size" in kwargs): self.max_upload_size = kwargs.pop("max_upload_size")
		super(ContentTypeRestrictedFileFieldForm, self).__init__(*args, **kwargs)

	def to_python(self, data):
		data= super(ContentTypeRestrictedFileFieldForm, self).to_python(data)
		
		## there's no files to threat
		if (data is None): return data
		
		file_size = data.size
		file_name = data.name
		if (not self.max_upload_size is None and file_size > self.max_upload_size):
			message = _('Please keep file {} size under {}. Current file size {}').format(
				file_name, filesizeformat(self.max_upload_size), filesizeformat(file_size))
			logger_debug.warning(message)
			logger_production.warning(message)
			raise forms.ValidationError(message)
		return data

