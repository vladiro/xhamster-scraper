#============================================
#   python gelbooru scraper v1.1
#   copyright 2014 qt
#   this program is free software under the GNU GPL version 3
#   usage: $program_name $url $output_dir
#
#   KNOWN BUGS:
#   - when dealing with a series of images the files can often be out of order
#	 this is due to the way in which the files are named, however as they are
#	 downloaded in a certain order its quite possible to reorder them though
#	 a batch renaming utility after theyve been downloaded
#   - cant handle backslashes at the end of the output_dir argument
#
#   TODO:
#   - port it to different sites
#============================================

import sys
import os
import re
import subprocess
from urllib import request

images_per_page = 42

#----------------------------------------------------------------------------------------------------------------
#   main procedure
#----------------------------------------------------------------------------------------------------------------
# stage 0
# parse args
try:
	gallery_URL, output_directory, pages = sys.argv[1], sys.argv[2] + "/", sys.argv[3]
except:
	print("fuck, cant process arguments")
	sys.exit()
#----------------------------------------------------------------------------------------------------------------
# stage 1
# enter loop
for i in range (0, int(pages)):
	print("processing page " + str(i))
	page_address = gallery_URL + "&pid=" + str(images_per_page * i)
	process = subprocess.call(["python", "gelbooru.py", page_address, output_directory])

print("completely done")
#----------------------------------------------------------------------------------------------------------------

	






