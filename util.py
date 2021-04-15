import os

def get_all_files(path):
  list_of_files = []

  for root, dirs, files in os.walk(path):
	  for file in files:
		  list_of_files.append(file)
  
  return list_of_files