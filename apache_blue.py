#!/usr/bin/env python3

import os, sys, re, shutil, tempfile, colorama
from datetime import datetime
from colorama import Fore, Back, Style

log_file = list()
dtnow = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# print the banner
def banner_print():
	print("\n\n\n")
	print(Fore.CYAN + " ______     ______   ______     ______     __  __     ______        ______     __         __  __     ______    " + Style.RESET_ALL)
	print(Fore.BLUE + "/" + Fore.CYAN + "\  __ \   " + Fore.BLUE + "/" + Fore.CYAN + "\  == \ " + Fore.BLUE + "/" + Fore.CYAN + "\  __ \   " + Fore.BLUE + "/" + Fore.CYAN + "\  ___\   " + Fore.BLUE + "/" + Fore.CYAN + "\ \_\ \   " + Fore.BLUE + "/" + Fore.CYAN + "\  ___\      " + Fore.BLUE + "/" + Fore.CYAN + "\  == \   " + Fore.BLUE + "/" + Fore.CYAN + "\ \       " + Fore.BLUE + "/" + Fore.CYAN + "\ \\" + Fore.BLUE + "/" + Fore.CYAN + "\ \   " + Fore.BLUE + "/" + Fore.CYAN + "\  ___\   ")
	print(Fore.BLUE + "\ " + Fore.CYAN + "\  __ \  " + Fore.BLUE + "\ " + Fore.CYAN + "\  _-/ " + Fore.BLUE + "\ " + Fore.CYAN + "\  __ \  " + Fore.BLUE + "\ " + Fore.CYAN + "\ \____  " + Fore.BLUE + "\ " + Fore.CYAN + "\  __ \  " + Fore.BLUE + "\ " + Fore.CYAN + "\  __\      " + Fore.BLUE + "\ " + Fore.CYAN + "\  __<   " + Fore.BLUE + "\ " + Fore.CYAN + "\ \____  " + Fore.BLUE + "\ " + Fore.CYAN + "\ \_\ \  " + Fore.BLUE + "\ " + Fore.CYAN + "\  __\   ")
	print(Fore.BLUE + " \ " + Fore.CYAN + "\_\ \_\  " + Fore.BLUE + "\ " + Fore.CYAN + "\_\    " + Fore.BLUE + "\ " + Fore.CYAN + "\_\ \_\  " + Fore.BLUE + "\ " + Fore.CYAN + "\_____\  " + Fore.BLUE + "\ " + Fore.CYAN + "\_\ \_\  " + Fore.BLUE + "\ " + Fore.CYAN + "\_____\     " + Fore.BLUE + "\ " + Fore.CYAN + "\_____\  " + Fore.BLUE + "\ " + Fore.CYAN + "\_____\  " + Fore.BLUE + "\ " + Fore.CYAN + "\_____\  " + Fore.BLUE + "\ " + Fore.CYAN + "\_____\ ")
	print(Fore.BLUE + "  \/_/\/_/   \/_/     \/_/\/_/   \/_____/   \/_/\/_/   \/_____/      \/_____/   \/_____/   \/_____/   \/_____/ " + Style.RESET_ALL)
	
	print("\n\n\n\nThank you for using " + Fore.CYAN + "apache_blue! " + Style.RESET_ALL + "Your Apache config files are now being scanned to find settings that can be\nchanged to make your server more secure. We will let you know what the best practice settings are below:\n\n")

# check current directory for apache_blue directory. creates it if not present
def ab_dir_check():
	if os.path.isdir('./apache_blue') is True:
		if os.path.isdir('./apache_blue/backup_files') is True:
			if os.path.isdir('./apache_blue/log_files') is False:
				os.mkdir('./apache_blue/log_files')
		else:
			os.mkdir('./apache_blue/backup_files')
			if os.path.isdir('./apache_blue/log_files') is False:
				os.mkdir('./apache_blue/log_files')
	else:
		os.mkdir('./apache_blue')
		os.mkdir('./apache_blue/backup_files')
		os.mkdir('./apache_blue/log_files')

# find all config files
def conf_files(path):
	config_files = list()
	for pd, directories, files in os.walk(path):
		for file in files:
			if file.endswith('.conf'):
				fname = os.path.join(pd, file)
				config_files.append(fname)
	return config_files

# make backups of config files
def backup_files(conf_list):
	global dtnow
	with tempfile.TemporaryDirectory() as directory:
		for files in conf_list:
			shutil.copy2(files, directory)
		shutil.make_archive('./apache_blue/backup_files/' + dtnow, 'zip', directory)
	print('All configuration files were backed up and zipped inside ./apache_blue/backup_files\n')


# check config file for a setting
def check_file(file, content):
	re_content = r'\b' + content + r'\b'
	with open(file, 'r') as x:
		for lines in x:
			if re.match(re_content, lines):
				return True

# generate a list of config files with the setting to change
def get_working_list(f_list, setting):
	working_list = list()
	for names in f_list:
		if check_file(names, setting):
			working_list.append(names)
	return working_list

# function to find and replace lines in config files
def find_replace(file, item, new_line):
	rewritten_file = []
	re_item = r'\b' + re.escape(item) + r'\b'
	with open(file, 'r') as open_file:
		for lines in open_file:
			if re.match(re_item, lines):
				rewritten_file.append(new_line + '\n')
			else:
				rewritten_file.append(lines)
	try:
		with open(file, 'w+') as new_config:
					for lines in rewritten_file:
						new_config.write(lines)
	except:
		print("You don\'t have permission to write to configuration files. Are you root?\n")
		sys.exit(1)
						
# change the setting with proper function
def change_setting(w_list, setting, new_setting, set_func):
	if set_func == 'find_replace':
		for items in w_list:
			#print(items)
			find_replace(items, setting, new_setting)
			add_to_log(items, new_setting)
	w_list.clear()
	print('\n')

# prompt user to make change to settings
def user_prompt_settings(setting, url, new_setting):
	print(f'{setting}: ' + Fore.YELLOW + 'Do you want to change setting to: ' + Fore.CYAN + f'{new_setting}' + '\n' + Style.RESET_ALL + url)
	yes_no = input('Would you like to change this setting?' + Fore.CYAN + ' [Y/n]: ' + Style.RESET_ALL)
	while yes_no != 'Y' and yes_no != 'y' and yes_no != 'N' and yes_no != 'n':
		yes_no = input('Would you like to change this setting? ' + Fore.CYAN + '[Y/n]: ' + Style.RESET_ALL)
	if yes_no == 'Y' or yes_no == 'y':
		return True
	elif yes_no == 'N' or yes_no == 'n':
		return False

# add setting change to the log file
def add_to_log(file, new_setting):
	global log_file
	dtnow = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	log_line = dtnow + ': ' + file + ': ' + 'Changed setting to: ' + new_setting
	return log_file.append(log_line)		

# main function to change a rule in a config file
def change_rule(file_list, setting, bp_setting, ch_setting_func, user_change):
	if user_change:
		working_list = get_working_list(file_list, setting)
		if not working_list:
			for x in file_list:
				if 'apache2.conf' in x:
					working_list.append(x)
					create_rule(bp_setting, working_list)
		else:
			change_setting(working_list, setting, bp_setting, ch_setting_func)
		working_list.clear()
	else:
		print('\n')

# a rule change that prompts the user for input
def change_rule_prompt(file_list, setting, bp_setting, ch_setting_func, user_change):
	if user_change:
		working_list = get_working_list(file_list, setting)
		user_def = input(f'Enter new {setting} setting' + Fore.CYAN + ' (in # of seconds): ' + Style.RESET_ALL)
		bp_setting = setting + ' ' + user_def
		change_setting(working_list, setting, bp_setting, ch_setting_func)
		working_list.clear()
	else:
				print('\n')

# create a rule if it does not exist in any conf files
def create_rule(bestprac, file):
	file_str = file.pop()
	with open(file_str, 'a+') as new_config:
		new_config.write(bestprac + '\n\n')
	add_to_log(file_str, bestprac)
	print('\n')

# write log file to directroy
def write_log(log_file):
	global dtnow
	if log_file:
		log_name = dtnow + "_apache_blue.log"
		# write the log file
		with open('./apache_blue/log_files/' + log_name, 'w+') as final_log:
			for events in log_file:
				final_log.write(events + '\n')
		print(f"\nTo review the settings that were changed, please see " + Fore.GREEN + f"./apache_blue/log_files/{log_name}" + Style.RESET_ALL)
	else:
		print("\nNo settings were changed, no log created.\n")

def main():
	#print program's banner
	banner_print()
	# directroy of apache config files
	directory = sys.argv[1]
	# find all config files
	file_list = conf_files(directory)
	# creates an archive of all config as backups
	backup_files(file_list)
	# check if apache_blue directory exists
	ab_dir_check()

	# Server Tokens setting
	setting = 'ServerTokens'
	bp_setting = 'ServerTokens Prod'
	url = Fore.GREEN + 'For more info see --> [20] ' + Style.RESET_ALL + 'at https://apache-blue.gitbook.io/guide/info-leakage'
	ch_setting_func = 'find_replace'
	user_change = user_prompt_settings(setting, url, bp_setting)
	change_rule(file_list, setting, bp_setting, ch_setting_func, user_change)

	# Server signature setting
	setting = 'ServerSignature'
	bp_setting = 'ServerSignature Off'
	url = Fore.GREEN + 'For more info see --> [21] ' + Style.RESET_ALL + 'at https://apache-blue.gitbook.io/guide/info-leakage'
	ch_setting_func = 'find_replace'
	user_change = user_prompt_settings(setting, url, bp_setting)
	change_rule(file_list, setting, bp_setting, ch_setting_func, user_change)

	# Keep Alive setting
	setting = 'KeepAlive'
	bp_setting = 'KeepAlive On'
	url = Fore.GREEN + 'For more info see --> [24] ' + Style.RESET_ALL + 'at https://apache-blue.gitbook.io/guide/dos-attacks'
	ch_setting_func = 'find_replace'
	user_change = user_prompt_settings(setting, url, bp_setting)
	change_rule(file_list, setting, bp_setting, ch_setting_func, user_change)
	
	# ETag settings
	setting = 'FileETag'
	bp_setting = 'FileETag None'
	url = Fore.GREEN + 'For more info see --> [22] ' + Style.RESET_ALL + 'at https://apache-blue.gitbook.io/guide/info-leakage'
	ch_setting_func = 'find_replace'
	user_change = user_prompt_settings(setting, url, bp_setting)
	change_rule(file_list, setting, bp_setting, ch_setting_func, user_change)
	
	# Timeout settings
	setting = 'Timeout'
	bp_setting = 'Timeout <TIME IN SECONDS> [Ideal setting is 10 or less]'
	url = Fore.GREEN + 'For more info see --> [23] ' + Style.RESET_ALL + 'at https://apache-blue.gitbook.io/guide/dos-attacks'
	ch_setting_func = 'find_replace'
	user_change = user_prompt_settings(setting, url, bp_setting)
	change_rule_prompt(file_list, setting, bp_setting, ch_setting_func, user_change)
	
	# Max Keep Alive Requests
	setting = 'MaxKeepAliveRequests'
	bp_setting = 'MaxKeepAliveRequests 100'
	url = Fore.GREEN + 'For more info see --> [25] ' + Style.RESET_ALL + 'at https://apache-blue.gitbook.io/guide/dos-attacks'
	ch_setting_func = 'find_replace'
	user_change = user_prompt_settings(setting, url, bp_setting)
	change_rule(file_list, setting, bp_setting, ch_setting_func, user_change)
	
	# Keep Alive Timeout
	setting = 'KeepAliveTimeout'
	bp_setting = 'KeepAliveTimeout <TIME IN SECONDS> [Ideal setting is 15 or less]'
	url = Fore.GREEN + 'For more info see --> [26] ' + Style.RESET_ALL + 'at https://apache-blue.gitbook.io/guide/dos-attacks'
	ch_setting_func = 'find_replace'
	user_change = user_prompt_settings(setting, url, bp_setting)
	change_rule_prompt(file_list, setting, bp_setting, ch_setting_func, user_change)

	# Disable Trace enable
	setting = 'TraceEnable'
	bp_setting = 'TraceEnable Off'
	url = Fore.GREEN + 'For more info see --> [17] ' + Style.RESET_ALL + 'at https://apache-blue.gitbook.io/guide/attack-surface'
	ch_setting_func = 'find_replace'
	user_change = user_prompt_settings(setting, url, bp_setting)
	change_rule(file_list, setting, bp_setting, ch_setting_func, user_change)

	# Set log level
	setting = 'LogLevel'
	#bp_setting = 'LogLevel info'
	bp_setting = 'LogLevel notice core:info'
	url = Fore.GREEN + 'For more info see --> [18] ' + Style.RESET_ALL + 'at https://apache-blue.gitbook.io/guide/logs'
	ch_setting_func = 'find_replace'
	user_change = user_prompt_settings(setting, url, bp_setting)
	change_rule(file_list, setting, bp_setting, ch_setting_func, user_change)
	
	# Limit Requestline
	setting = 'LimitRequestline'
	bp_setting = 'LimitRequestline 512'
	url = Fore.GREEN + 'For more info see --> [29] ' + Style.RESET_ALL + 'https://apache-blue.gitbook.io/guide/bof-attacks'
	ch_setting_func = 'find_replace'
	user_change = user_prompt_settings(setting, url, bp_setting)
	change_rule(file_list, setting, bp_setting, ch_setting_func, user_change)

	# Limit Request Fields
	setting = 'LimitRequestFields'
	bp_setting = 'LimitRequestFields 100'
	url = Fore.GREEN + 'For more info see --> [30] ' + Style.RESET_ALL + 'https://apache-blue.gitbook.io/guide/bof-attacks'
	ch_setting_func = 'find_replace'
	user_change = user_prompt_settings(setting, url, bp_setting)
	change_rule(file_list, setting, bp_setting, ch_setting_func, user_change)

	# Limit Request Field size
	setting = 'LimitRequestFieldsize'
	bp_setting = 'LimitRequestFieldsize 1024'
	url = Fore.GREEN + 'For more info see --> [31] ' + Style.RESET_ALL + 'https://apache-blue.gitbook.io/guide/bof-attacks'
	ch_setting_func = 'find_replace'
	user_change = user_prompt_settings(setting, url, bp_setting)
	change_rule(file_list, setting, bp_setting, ch_setting_func, user_change)

	# Limit Request Body
	setting = 'LimitRequestBody'
	bp_setting = 'LimitRequestBody 102400'
	url = Fore.GREEN + 'For more info see --> [32] ' + Style.RESET_ALL + 'https://apache-blue.gitbook.io/guide/bof-attacks'
	ch_setting_func = 'find_replace'
	user_change = user_prompt_settings(setting, url, bp_setting)
	change_rule(file_list, setting, bp_setting, ch_setting_func, user_change)
		
	print(f"\n\n\nLooks like you're all set!")

	write_log(log_file)
	
	#print(f"\n\n\nLooks like you're all set! To review the settings that were changed, please see " + Fore.GREEN + f"./apache_blue/log_files/{log_name}" + Style.RESET_ALL)
	print(Fore.CYAN + "\nFor more information about hardening Apache servers, visit https://apache-blue.gitbook.io/guide" + Style.RESET_ALL)
	print("\nThanks again for using " + Fore.CYAN + "apache_blue. " + Style.RESET_ALL + "Have a great day!\n\n")

if __name__ == "__main__":
	main()
