'''
Created on Oct 13, 2017

@author: mmp
'''
from enum import Enum
import os

class Constants(object):
	'''
	classdocs
	'''
	
	### default user that has the default references to be used in mapping
	DEFAULT_USER = "system"
	DEFAULT_USER_PASS = "default_user_123_$%_2"
	META_KEY_VALUE_NOT_NEED = "value not needed"
	
	DIR_PROCESSED_FILES_UPLOADS = "uploads"
	
	### separators
	SEPARATOR_COMMA = ','
	SEPARATOR_TAB = '\t'

	## DIR_PROCESSED_FILES_FROM_WEB/userId_<id>/refId_<id>
	DIR_PROCESSED_FILES_PROJECT_EVENT = os.path.join(DIR_PROCESSED_FILES_UPLOADS, "project_event")

	DIR_ICONS = "icons"
	DIR_TEMPLATE_INPUT = "template_input"
	TEMP_DIRECTORY = "/tmp"
	COUNT_DNA_TEMP_DIRECTORY = "project_manager"

	EXTENSION_ZIP = ".gz"
	
	#### default event types
	VECT_EVENT_TYPES = ["Sequencing", "Report release", "Analyzes pipeline", "Quotation"]
	VECT_EVENT_TYPES_DESCRIPTION = ["Sequencing results", "Report release", "Analyzes pipeline", "Quotation"]
	
	#####
	DIR_STATIC = "static"
	DIR_ICONS = "icons"
	ICON_GREEN_16_16 = "bullet_ball_glass_green.png"
	ICON_YELLOW_16_16 = "bullet_ball_glass_yellow.png"
	ICON_RED_16_16 = "bullet_ball_glass_red.png"
	ICON_GREEN_24_24 = "bullet_ball_glass_green_24_24.png"
	ICON_YELLOW_24_24 = "bullet_ball_glass_yellow_24_24.png"
	ICON_RED_24_24 = "bullet_ball_glass_red_24_24.png"
	ICON_GREEN_32_32 = "bullet_ball_glass_green_32_32.png"
	ICON_YELLOW_32_32 = "bullet_ball_glass_yellow_32_32.png"
	ICON_RED_32_32 = "bullet_ball_glass_red_32_32.png"
	
	AJAX_LOADING_GIF = "ajax-loading-gif.gif"
	AJAX_LOADING_GIF_13 = "ajax-loading-gif-13.gif"
	
	### data_set 
	DATA_SET_GENERIC = "Generic"	## default name for a dataset
	
	## NUMBER OF SETs to paginate
	PAGINATE_NUMBER = 12			## projects and events
	PAGINATE_NUMBER_SETTINGS = 15	## only for settings
	PAGINATE_NUMBER_SMALL = 2

	## tag for sessions
	SESSION_PROJECTS_PK_KEY = 'session_project_pk_key'
	SESSION_EVENT_PK_KEY = 'session_event_pk_key'
	
	
	### empty value used in tables
	EMPTY_VALUE_TABLE = "-"
	
	### 
	EMPTY_VALUE_TYPE_SUBTYPE = "Not assigned"
	
	## errors
	PROJECT_NAME = 'project_name'
	ERROR_REFERENCE = 'error_reference'
	ERROR_PROJECT_NAME = 'error_project_name'

	def get_extensions_by_file_type(self, file_name, file_type):
		"""
		get extensions by file type
		"""
		if (file_type == FileType.FILE_BAM): return "{}.bam".format(file_name)
		if (file_type == FileType.FILE_BAM_BAI): return "{}.bam.bai".format(file_name)
		if (file_type == FileType.FILE_CONSENSUS_FA): return "{}.consensus.fa".format(file_name)
		if (file_type == FileType.FILE_CONSENSUS_FASTA): return "{}{}".format(file_name, FileExtensions.FILE_CONSENSUS_FASTA)
		if (file_type == FileType.FILE_CSV): return "{}.csv".format(file_name)
		if (file_type == FileType.FILE_DEPTH): return "{}.depth".format(file_name)
		if (file_type == FileType.FILE_DEPTH_GZ): return "{}.depth.gz".format(file_name)
		if (file_type == FileType.FILE_DEPTH_GZ_TBI): return "{}.depth.gz.tbi".format(file_name)
		if (file_type == FileType.FILE_TAB): return "{}.tab".format(file_name)
		if (file_type == FileType.FILE_VCF): return "{}.vcf".format(file_name)
		if (file_type == FileType.FILE_VCF_GZ): return "{}.vcf.gz".format(file_name)
		if (file_type == FileType.FILE_VCF_GZ_TBI): return "{}.vcf.gz.tbi".format(file_name)
		if (file_type == FileType.FILE_REF_FASTA): return "ref.fa"
		if (file_type == FileType.FILE_REF_FASTA_FAI): return "ref.fa.fai"
		return ""

	def short_name(self, name, max_size):
		"""
		short the name for the size of max_size
		"""
		if (len(name) > max_size): return "{}...{}".format(name[:int(max_size/2)], name[int(len(name) - (max_size/2)):])
		return name
	
class TypePath(Enum):
	"""
	Has the type of paths you can get from file paths
	"""
	MEDIA_ROOT = 0
	MEDIA_URL = 1


class FileType(Enum):
	"""
	Has the type of files
	[06:29:16] * /tmp/insafli/xpto/xpto.bam
	[06:29:16] * /tmp/insafli/xpto/xpto.bam.bai
	[06:29:16] * /tmp/insafli/xpto/xpto.bed
	[06:29:16] * /tmp/insafli/xpto/xpto.consensus.fa
	[06:29:16] * /tmp/insafli/xpto/xpto.consensus.subs.fa
	[06:29:16] * /tmp/insafli/xpto/xpto.csv
	[06:29:16] * /tmp/insafli/xpto/xpto.depth.gz
	[06:29:16] * /tmp/insafli/xpto/xpto.depth.gz.tbi
	[06:29:16] * /tmp/insafli/xpto/xpto.filt.subs.vcf
	[06:29:16] * /tmp/insafli/xpto/xpto.filt.subs.vcf.gz
	[06:29:16] * /tmp/insafli/xpto/xpto.filt.subs.vcf.gz.tbi
	[06:29:16] * /tmp/insafli/xpto/xpto.filt.vcf
	[06:29:16] * /tmp/insafli/xpto/xpto.gff
	[06:29:16] * /tmp/insafli/xpto/xpto.html
	[06:29:16] * /tmp/insafli/xpto/xpto.log
	[06:29:16] * /tmp/insafli/xpto/xpto.raw.vcf
	[06:29:16] * /tmp/insafli/xpto/xpto.tab
	[06:29:16] * /tmp/insafli/xpto/xpto.txt
	[06:29:16] * /tmp/insafli/xpto/xpto.vcf
	[06:29:16] * /tmp/insafli/xpto/xpto.vcf.gz
	[06:29:16] * /tmp/insafli/xpto/xpto.vcf.gz.tbi
				/tmp/insafli/xpto/ref/ref.fa
	"""
	FILE_BAM = 0
	FILE_BAM_BAI = 1
	FILE_CONSENSUS_FA = 2
	FILE_CONSENSUS_FASTA = 3
	FILE_DEPTH = 4
	FILE_DEPTH_GZ = 5
	FILE_DEPTH_GZ_TBI = 6
	FILE_TAB = 7
	FILE_VCF = 8
	FILE_VCF_GZ = 9
	FILE_VCF_GZ_TBI = 10
	FILE_CSV = 11
	FILE_REF_FASTA = 12		## ref/ref.fa
	FILE_REF_FASTA_FAI = 13		## ref/ref.fa.fai

class TypeFile(object):
	
	TYPE_FILE_fastq_gz = "fastq.gz"								## fastq.fz files
	TYPE_FILE_sample_file = "sample-file imported" 				## file that the user import with sample descriptions
	TYPE_FILE_sample_file_metadata = "sample-file metadata" 	## file that the user import with new metadata

	
class FileExtensions(object):
	"""
	file extensions
	"""
	FILE_TSV = '.tsv'
	FILE_TXT = '.txt'
	FILE_TAB = '.tab'
	FILE_VCF = '.vcf'
	FILE_VCF_BGZ = 'vcf.bgz'
	FILE_VCF_BGZ_TBI = 'vcf.bgz.tbi'
	FILE_VCF_GZ = 'vcf.gz'
	FILE_CSV = '.csv'
	FILE_PNG = '.png'
	FILE_GBK = '.gbk'
	FILE_GB = '.gb'
	FILE_FASTA = '.fasta'
	FILE_FASTQ = '.fastq'
	FILE_FNA = '.fna'
	FILE_FAA = '.faa'
	FILE_FA = '.fa'
	FILE_FAI = '.fai'
	FILE_CONSENSUS_FASTA = '.consensus.fasta'
	FILE_TREE = '.tree'
	FILE_NWK = '.nwk'
	FILE_GZ = '.gz'
	FILE_BED = '.bed'
	FILE_TBI = '.tbi'	### create with tabix
	FILE_IDX = '.idx'	### created from igvtools
	FILE_JSON = '.json'

	### all GBK
	VECT_ALL_GBK_EXTENSIONS = [FILE_GBK, FILE_GB] 
