'''
Created on Oct 31, 2017

@author: mmp
'''
from constants.constants import Constants, FileExtensions
from django.utils.translation import ugettext_lazy as _
import os, random, logging, ntpath, stat, secrets
from django.conf import settings

class Utils(object):
	'''
	class docs
	'''

	## logging
	logger_debug = logging.getLogger("project_manager.debug")
	logger_production = logging.getLogger("project_manager.production")

	def __init__(self):
		'''
		Constructor
		'''
		pass
	
	def get_path_to_project_event_file(self, project_pk, event_pk, user_pk):
		"""
		get the path to reference
		"""
		return os.path.join(Constants.DIR_PROCESSED_FILES_PROJECT_EVENT, "projectId_{}".format(project_pk),\
				"eventId_{}".format(event_pk), "userId_{}".format(user_pk))

	def get_path_to_project_event_file_with_random(self, project_pk, event_pk, user_pk):
		"""
		get the path to reference
		"""
		randon_path = secrets.token_hex(5)
		root_dir = settings.MEDIA_ROOT
		path_to_test = os.path.join(root_dir, self.get_path_to_project_event_file(project_pk, event_pk, user_pk),\
				randon_path)

		while os.path.exists(path_to_test):
			randon_path = secrets.token_hex(5)
			path_to_test = os.path.join(root_dir, self.get_path_to_project_event_file(project_pk, event_pk, user_pk), randon_path)
		return os.path.join(self.get_path_to_project_event_file(project_pk, event_pk, user_pk), randon_path)


	def get_unique_file(self, file_name):
		"""
		get unique file name from a file_name
		return '<path file_name>/<random number>_<file_name>'
		"""
		temp_file_name = "{}_{}".format(random.randrange(10000000, 99999999, 10), ntpath.basename(file_name))
		main_path = os.path.dirname(file_name)
		if (not os.path.exists(main_path)): os.makedirs(main_path)
		while 1:
			if (not os.path.exists(os.path.join(main_path, temp_file_name))): break
			temp_file_name = "{}_{}".format(random.randrange(10000000, 99999999, 10), ntpath.basename(file_name))
		return os.path.join(main_path, temp_file_name.replace(" ", "_"))

	def get_temp_file(self, file_name, sz_type):
		"""
		return a temp file name
		"""
		main_path = os.path.join(Constants.TEMP_DIRECTORY, Constants.COUNT_DNA_TEMP_DIRECTORY)
		if (not os.path.exists(main_path)): os.makedirs(main_path)
		self.touch_file(main_path)
		while 1:
			return_file = os.path.join(main_path, "projects_" + file_name + "_" + str(random.randrange(10000000, 99999999, 10)) + "_file" + sz_type)
			if (os.path.exists(return_file)): continue
			try:
				os.close(os.open(return_file, os.O_CREAT | os.O_EXCL))
				return return_file
			except FileExistsError:
				pass
			
	def get_temp_file_from_dir(self, dir_out, file_name, sz_type):
		"""
		return a temp file name
		"""
		if (not os.path.exists(dir_out)): os.makedirs(dir_out)
		self.touch_file(dir_out)
		while 1:
			return_file = os.path.join(dir_out, "projects_" + file_name + "_" + str(random.randrange(10000000, 99999999, 10)) + "_file" + sz_type)
			if (os.path.exists(return_file)): continue
			try:
				os.close(os.open(return_file, os.O_CREAT | os.O_EXCL))
				return return_file
			except FileExistsError:
				pass
			
	def touch_file(self, file_name):
		"""
		Uptodate dir name/file to not be removed by file system 
		"""
		if (os.path.exists(file_name)):
			cmd = "touch {}".format(file_name)
			os.system(cmd)

	def get_temp_dir(self):
		"""
		return a temp directory
		"""
		main_path = os.path.join(Constants.TEMP_DIRECTORY, Constants.COUNT_DNA_TEMP_DIRECTORY)
		if (not os.path.exists(main_path)): os.makedirs(main_path)
		self.touch_file(main_path)
		while 1:
			return_path = os.path.join(main_path, "projects_" + str(random.randrange(10000000, 99999999, 10)))
			if (not os.path.exists(return_path)):
				os.makedirs(return_path)
				return return_path
	
	def get_file_name_without_extension(self, file_name):
		"""
		return file name without extension
		"""
		return os.path.splitext(os.path.basename(file_name))[0]
		
		
	def remove_temp_file(self, sz_file_name):
		"""
		prevent to remove files outside of temp directory
		"""
		if (sz_file_name == None): return
		
		if os.path.exists(sz_file_name) and len(sz_file_name) > 0 and sz_file_name.startswith(Constants.TEMP_DIRECTORY):
			cmd = "rm " + sz_file_name
			exist_status = os.system(cmd)
			if (exist_status != 0):
				self.logger_production.error('Fail to run: ' + cmd)
				self.logger_debug.error('Fail to run: ' + cmd)
				raise Exception("Fail to remove a file") 

	def remove_file(self, sz_file_name):
		"""
		Remove files
		return True if the file exists and was removed
		"""
		if (sz_file_name == None): return False
		
		if os.path.exists(sz_file_name) and len(sz_file_name) > 0:
			cmd = "rm " + sz_file_name
			exist_status = os.system(cmd)
			if (exist_status != 0):
				self.logger_production.error('Fail to run: ' + cmd)
				self.logger_debug.error('Fail to run: ' + cmd)
				raise Exception("Fail to remove a file")
			return True
		return False

	def remove_dir(self, path_name):
		if (path_name != None and os.path.isdir(path_name)):
			cmd = "rm -r %s*" % (path_name); os.system(cmd)

	def move_file(self, sz_file_from, sz_file_to):
		if os.path.exists(sz_file_from):
			self.make_path(os.path.dirname(sz_file_to))
			cmd = "mv " + sz_file_from + " " + sz_file_to
			exist_status = os.system(cmd)
			if (exist_status != 0):
				self.logger_production.error('Fail to run: ' + cmd)
				self.logger_debug.error('Fail to run: ' + cmd)
				raise Exception("Fail to make a move a file") 
	
			### set attributes to file 664
			os.chmod(sz_file_to, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH)
			
	def link_file(self, sz_file_from, sz_file_to):
		if os.path.exists(sz_file_from):
			self.make_path(os.path.dirname(sz_file_to))
			cmd = "ln -f -s " + sz_file_from + " " + sz_file_to
			exist_status = os.system(cmd)
			if (exist_status != 0):
				self.logger_production.error('Fail to run: ' + cmd)
				self.logger_debug.error('Fail to run: ' + cmd)
				raise Exception("Fail to link a file") 
			
	def copy_file(self, sz_file_from, sz_file_to):
		if os.path.exists(sz_file_from):
			self.make_path(os.path.dirname(sz_file_to))
			cmd = "cp " + sz_file_from + " " + sz_file_to
			exist_status = os.system(cmd)
			if (exist_status != 0):
				self.logger_production.error('Fail to run: ' + cmd)
				self.logger_debug.error('Fail to run: ' + cmd)
				raise Exception("Fail to make a move a file") 
			
			### set attributes to file 664
			os.chmod(sz_file_to, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH)
			
	def make_path(self, path_name):
		if (not os.path.isdir(path_name) and not os.path.isfile(path_name)):
			cmd = "mkdir -p " + path_name
			os.system(cmd)
			exist_status = os.system(cmd)
			if (exist_status != 0):
				self.logger_production.error('Fail to run: ' + cmd)
				self.logger_debug.error('Fail to run: ' + cmd)
				raise Exception("Fail to make a path") 
		
	def is_integer(self, n_value):
		try:
			int(n_value)
			return True
		except ValueError: 
			return False


	def is_float(self, n_value):
		try:
			float(n_value)
			return True
		except ValueError: 
			return False

	def is_gzip(self, file_name):
		"""
		test if the file name ends in gzip
		""" 
		return file_name.endswith(".gz")
	
	def read_text_file(self, file_name):
		"""
		read text file and put the result in an vector
		"""
		if (not os.path.exists(file_name)):
			self.logger_production.error("Fail to read '" + file_name)
			self.logger_debug.error("Fail to test '" + file_name)
			raise IOError(_("Error: file '" + file_name + "' doens't exist."))
		
		vect_out = []
		with open(file_name) as handle: 
			for line in handle:
				sz_temp = line.strip()
				if (len(sz_temp) == 0): continue
				vect_out.append(sz_temp)
		return vect_out
	
	def get_all_files(self, directory):
		"""
		return all files from a directory
		"""
		return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


	def compress_files(self, software, file_name):
		"""
		compress files
		"""
		### get extension of output
		# extension = FileExtensions.FILE_BGZ if software == SoftwareNames.SOFTWARE_BGZIP_name else FileExtensions.FILE_GZ
		extension = FileExtensions.FILE_GZ
		
		## test if the file exists
		if (os.path.exists(file_name + extension)): return
		
		cmd = "{} -c {} > {}{}".format(software, file_name, file_name, extension)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			self.logger_production.error('Fail to run: ' + cmd)
			self.logger_debug.error('Fail to run: ' + cmd)
			raise Exception("Fail to compress file") 
		
	def uncompress_files(self, software, file_name_in, file_name_out):
		"""
		compress files
		"""
		## test if the file exists
		if (not os.path.exists(file_name_in)): return
		
		cmd = "{} -cd {} > {}".format(software, file_name_in, file_name_out)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			self.logger_production.error('Fail to run: ' + cmd)
			self.logger_debug.error('Fail to run: ' + cmd)
			raise Exception("Fail to compress file") 

	def str2bool(self, v):
		"""
		str to bool
		"""
		return v.lower() in ("yes", "true", "t", "1", "y")
	
	
	def md5sum(self, filename):
		"""
		read file and transform to md5sum
		"""
		temp_file = self.get_temp_file("md5_sum_", ".txt")
		cmd = "md5sum {} > {}".format(filename, temp_file)
		os.system(cmd)
		
		exist_status = os.system(cmd)
		if (exist_status != 0):
			if (os.path.exists(temp_file)): os.unlink(temp_file)
			self.logger_production.error('Fail to run: ' + cmd)
			self.logger_debug.error('Fail to run: ' + cmd)
			raise Exception("Fail to create md5sum")
		
		### read output
		vect_key_out = self.read_text_file(temp_file)
		
		if (len(vect_key_out) == 0):
			if (os.path.exists(temp_file)): os.unlink(temp_file)
			self.logger_production.error('Fail to read output from: ' + cmd)
			self.logger_debug.error('Fail to read output from: ' + cmd)
			raise Exception("Fail to create md5sum")
		
		if (os.path.exists(temp_file)): os.unlink(temp_file)
		return vect_key_out[0].split()[0]


	def clean_name(self, name_to_clean, dict_to_clean = { ' ' : '_', '(' : '', ')' : '', '$' : '', '#' : '', '&' : '', '/' : '', '\\' : '' }):
		"""
		clean a name based on dictionary, dict_to_clean = { ' ' : '_', '(' : '' , ')' : '' }
		
		"""
		for key in dict_to_clean:
			name_to_clean = name_to_clean.replace(key, dict_to_clean[key])
		return name_to_clean
	
		