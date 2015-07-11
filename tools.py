#!/usr/bin/python

import os
from sys import argv
from os import listdir
from os.path import isfile, join
import logging

COMMENT_CHAR = '#'
OPTION_CHAR = '='

#Function for parsing config file
def parse_config(filename):
  options = {}

  try:
    f = open(filename)
  except IOError:
    return 1

  for line in f:

    # First, remove comments:
    if COMMENT_CHAR in line:
      # split on comment char, keep only the part before
      line, comment = line.split(COMMENT_CHAR, 1)
    # Second, find lines with an option=value:
    if OPTION_CHAR in line:
      # split on option char:
      option, value = line.split(OPTION_CHAR, 1)
      option = option.strip()
      value = value.strip()
      #store in dictionary:
      #print option + '~' + value + '\n'
      options[option] = value
  f.close()
  return options

# Function for creating directories
def make_dirs(dir):
  if not os.path.exists(dir):
    os.makedirs(dir)

# Function for pid file creation
def create_pid(pidfile):
  if not os.path.exists(pidfile):
    try:
      fp = open(pidfile, 'w')
      fp.write(str(os.getpid()))
      return 0
    except Exception, e:
      print 'Unable to create pid file.', e
      return 1
  else:
    print "PID file already exists. Cannot run multiple instances."
    return 2

# remove lock file
def removeFile(lockfile):
  try:
    os.remove(lockfile)
  except Exception, e:
    return 1
  return  0

# function to get read in a directory
def list_dir(path, prefix, suffix):
  raw_file_list = [f for f in os.listdir(path) if isfile(join(path,f)) ]
  file_list = []
  for file in raw_file_list:
    if file.endswith(suffix) and file.startswith(prefix):
      file_list.append(file)
  return file_list

# Function in creating log file
def create_log(log_file):
  try:
      logging.basicConfig(filename=log_file, format='%(asctime)s | %(levelname)s : %(message)s', datefmt='%m/%d/%Y %H:%M:%S',level=logging.INFO)
      #logging.info('---------------------------Started------------------------------')
      return 0
  except Exception, e:
      print('Failed to initialize logger (%s)' % e)
      return 1

# Function for loading a reference file to dictionary
def digilist(file_list):
  ref_list = {}
  try:
    fp = open(file_list, 'r')
  except Exception, e:
    print 'Unable to read reference file.', e
    return 1

  for line in fp:
    line = line.strip()
    key, val = line.split('~', 1)
    ref_list[key] = val
  return ref_list

# Function for Serching in a dictionary #Sorting is made for LDM
def find_digilist(str, slist):
  for prefix in sorted(slist, reverse=True):
    if str.startswith(prefix):
      return prefix
  return ''

# Function for creating alarm file
def writeAlarm(alarm_dir, agent_id, module_id, mod_instance, error_id, date_time):
  filename = alarm_dir + agent_id + '_' + module_id + '_' + mod_instance + '_' + error_id + '_' + date_time + ".alarm"
  alarm_file = open(filename,'w')
  print 'alarm file created [%s]' % error_id
  alarm_file.write('')

# Function for emqil file creation.
def writeEmail(email_file, emlStr):
  try:
      fp = open(email_file, 'w')
      fp.write(str(emlStr))
      return 0
  except Exception, e:
      print 'Unable to create email file.', e
      return e
