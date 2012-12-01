# -*- coding: utf-8 -*-
import sublime, sublime_plugin
import subprocess, platform, re, os

#define methods to convert css, either the current file or all
class Compiler:
	def __init__(self, view):
		self.view = view

	# for command 'LessToCssCommand' and 'AutoLessToCssCommand'
	def convertOne(self, is_auto_save = False):
		fn = self.view.file_name().encode("utf_8")
		localview = self.view
		if not fn.endswith(".less"):
			return ''

		settings = sublime.load_settings('less2css.sublime-settings')
		base_dir = localview.settings().get('lessBaseDir', settings.get("lessBaseDir"))
		output_dir = localview.settings().get('outputDir', settings.get("outputDir"))
		#input one less file for compiling
		one_file = localview.settings().get('oneFile', settings.get('oneFile'))
		minimised = settings.get("minify", True)
		auto_compile = settings.get("autoCompile", True)

		if auto_compile == False and is_auto_save == True:
			return ''

		dirs = self.parseBaseDirs(base_dir, output_dir, one_file)
		
		if one_file != False:
			fn = dirs['one']
			dirs['less'] = dirs['project'] + '\less'
		
		return self.convertLess2Css(dirs = dirs, file = fn, minimised = minimised)

	# for command 'AllLessToCssCommand'
	def convertAll(self):
		err_count = 0;

		#default_base
		settings = sublime.load_settings('less2css.sublime-settings')
		base_dir = settings.get("lessBaseDir")
		output_dir = settings.get("outputDir")
		minimised = settings.get("minify", True)

		dirs = self.parseBaseDirs(base_dir, output_dir)

		for r,d,f in os.walk(dirs['less']):
			for files in f:
				if files.endswith(".less"):
					#add path to file name
					fn = os.path.join(r, files)
					#call compiler
					resp = self.convertLess2Css(dirs, file = fn, minimised = minimised)

					if resp != "":
						err_count = err_count + 1

		if err_count > 0:
			return "There were errors compiling all LESS files"
		else:
			return ''


	# do convert
	def convertLess2Css(self, dirs, file = '', minimised = True):
		out = ''

		#get the current file & its css variant
		if file == "":
			less = self.view.file_name().encode("utf_8")
		else:
			less = file

		if not less.endswith(".less"):
			return ''

		css = re.sub('\.less$', '.css', less)
		sub_path = css.replace(dirs['less'] + os.path.sep, '')
		css = os.path.join(dirs['css'], sub_path)


		# create directories
		output_dir = os.path.dirname(css)
		if not os.path.isdir(output_dir):
			os.makedirs(output_dir)

		if minimised == True:
			cmd = ["lessc", less, css, "-x", "--verbose"]
		else:
			cmd = ["lessc", less, css, "--verbose"]

		print "[less2css] Converting " + less + " to "+ css

		if platform.system() != 'Windows':
			# if is not Windows, modify the PATH
			env = os.getenv('PATH')
			env = env + ':/usr/local/bin:/usr/local/sbin'
			os.environ['PATH'] = env
		else:
			# change command from lessc to lessc.cmd on Windows,
			# only lessc.cmd works but lessc doesn't
			cmd[0] = 'lessc.cmd'
		
		#run compiler
		p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True) #not sure if node outputs on stderr or stdout so capture both
		stdout, stderr = p.communicate()

		#blank lines and control characters
		blank_line_re = re.compile('(^\s+$)|(\033\[[^m]*m)', re.M)

		#decode and replace blank lines
		out = stderr.decode("utf_8")
		out = blank_line_re.sub('', out)

		if out != '':
			print '----[less2cc] Compile Error----'
			print out
		else:
			print '[less2css] Convert completed!'

		return out
	

	# try to find project folder,
	# and normalize relative paths such as /a/b/c/../d to /a/b/d
	def parseBaseDirs(self, base_dir = './', output_dir = '', one_file = ''): 
		fn = self.view.file_name().encode("utf_8")
		file_dir = os.path.dirname(fn)

		# find project path
		# it seems that there is no shortcuts to get the active project folder,
		# it returns all, so need to find the active one
		proj_dir = ''
		window = sublime.active_window()
		proj_folders = window.folders()
		for folder in proj_folders:
			if fn.startswith(folder):
				proj_dir = folder
				break

		# normalize less base path
		if not base_dir.startswith('/'):
			base_dir = os.path.normpath(os.path.join(proj_dir, base_dir))

		# normalize css output base path
		if not output_dir.startswith('/'):
			output_dir = os.path.normpath(os.path.join(proj_dir, output_dir))
		
		if one_file != False:
			if not one_file.startswith('/'):
				one_file = os.path.normpath(os.path.join(proj_dir, one_file))

		return { 'project': proj_dir, 'less': base_dir, 'css' : output_dir, 'one' : one_file }