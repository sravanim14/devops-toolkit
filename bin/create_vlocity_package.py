#!/usr/bin/env python

# author        : Stepan Ruzicka
# e-mail	: stepan.ruzicka@gmail.com
# date          : 2018.05.24

import sys
import os
import argparse
from argparse import RawTextHelpFormatter
import json
import subprocess
import re
from distutils.dir_util import copy_tree

# script context variables
SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
CURRENT_WORKING_PATH = os.getcwd()
this = sys.modules[__name__]
SCRIPT_NAME = os.path.basename(__file__)

# default config values
DEBUG = False
IGNORE_ERRORS = False
DEBUG_LEVEL = 1

# configuration folders and files
CONFIG = '../etc'
DEFAULT_OUTPUT_PATH = 'packages'

class Color:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    GREY = '\033[90m'
    BLACK = '\033[90m'
    DEFAULT = '\033[99m'
    ENDC = '\033[0m'

class Format:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

def color_string(string, color):
   if(color == Color.BLUE):
      return Color.BLUE + string + Color.ENDC
   elif(color == Color.RED):
      return Color.RED + string + Color.ENDC
   elif(color == Color.GREEN):
      return Color.GREEN + string + Color.ENDC
   elif(color == Color.CYAN):
      return Color.CYAN + string + Color.ENDC
   elif(color == Color.WHITE):
      return Color.WHITE + string + Color.ENDC
   elif(color == Color.MAGENTA):
      return Color.MAGENTA + string + Color.ENDC
   elif(color == Color.GREY):
      return Color.GREY + string + Color.ENDC
   elif(color == Color.BLACK):
      return Color.BLACK + string + Color.ENDC
   elif(color == Color.YELLOW):
      return Color.YELLOW + string + Color.ENDC
   else:
      return string

def format_string(string, format):
   if(color == Color.UNDERLINE):
      return Format.UNDERLINE + string + Format.ENDC
   elif(color == Format.BOLD):
      return Format.BOLD + string + Format.ENDC
   else:
      return string

def print_info(info):
   if(DEBUG):
      print(info)

def print_error(message):
   print color_string(message, Color.RED)

def is_tool(name):
   return find_executable(name) is not None

def get_parent_folder(path):
   path_folders = re.split(r'\/', path)
   
   number_of_folders = len(path_folders)
   counter = 0
   for folder_name in path_folders:
      if counter + 1 != number_of_folders:
         if counter == 0:
            partial_path = folder_name
         else:
            partial_path += '/' + folder_name

      counter += 1 
   return partial_path

def main():
   parser = argparse.ArgumentParser(description='Creates vlocity package.\n' +
                                                'Example:\n' +
                                                '\t' + SCRIPT_NAME + ' -d',
						formatter_class=RawTextHelpFormatter)
   parser.add_argument(
        "-d", "--debug", dest="debug",
        help="Debug mode", action="store_true")

   parser.add_argument(
        "-o", "--output", dest="output",
        help="Output folder")

   parser.add_argument(
        "--debug-level", dest="debug_level",type=int,
        help="Debug level from {1, 2}")

   parser.add_argument(
        "--ignore-errors", dest="ignore_errors",
        help="Will keep on processing despite errors", action="store_true")

   args = parser.parse_args()

   # arguments assignment to global variables
   this.DEBUG = args.debug
   #this.IGNORE_ERRORS = args.ignore_errors
   if(args.debug_level == 2):
      this.DEBUG_LEVEL = 2

   this.IGNORE_ERRORS = args.ignore_errors

   if(args.output):
      output_folder = args.output
   else:
      output_folder = DEFAULT_OUTPUT_PATH

   print_info(color_string('Identifying changes', Color.GREEN))

   added_or_modified = []
   for line in sys.stdin:
      # split by tab
      line_array = re.split(r'\t+', line)

      # get a list of added or modified files beginning with "vlocity"
      pattern = re.compile("^vlocity.*")
      if (line_array[0] == 'A' or line_array[0] == 'M') and pattern.match(line_array[1]):
         if line_array[1].rstrip() not in added_or_modified:
            vlocity_folder_to_be_copied = get_parent_folder(line_array[1].rstrip())
            if vlocity_folder_to_be_copied not in  added_or_modified:
               added_or_modified.append(vlocity_folder_to_be_copied)
      elif(pattern.match(line_array[0])):
         if line_array[2].rstrip() not in added_or_modified:
            vlocity_folder_to_be_copied = get_parent_folder(line_array[2].rstrip())
            if vlocity_folder_to_be_copied not in  added_or_modified:
               added_or_modified.append(vlocity_folder_to_be_copied)            

   for folder in added_or_modified:
      parent_folder = get_parent_folder(folder)
      destination_folder_path = output_folder + '/' + folder
      print_info('Copying folder ' + color_string(folder, Color.MAGENTA) + ' to ' + color_string(destination_folder_path, Color.MAGENTA))
      try:
         copy_tree(folder, destination_folder_path)
      except Exception as e:
         error_message = "Unable copy folder " + folder  + ". If you want to ignore errors during the processing you can run it with --ignore-errors parameter. Please, also use -d parameter for more details: " + e.message
         if(not IGNORE_ERRORS):
            raise RuntimeError(error_message)
         else:
            print_error(error_message)

if __name__ == "__main__":
   main()
