#
#   python gelbooru scraper v1.1
#   copyright 2014 qt
#   this program is free software under the GNU GPL version 3
#   usage: python3 $program_name $url $output_dir $num_of_pages [update]
#
#   KNOWN BUGS:
#   - when dealing with a series of images the files can often be out of order.
#	 this is due to the way in which the files are named, however as they are
#	 downloaded in a certain order its quite possible to reorder them though
#	 a batch renaming utility after theyve been downloaded
#   - cant handle backslashes at the end of the output_dir argument
#
#   TODO:
#   - port it to different sites
#
import sys
import os
import re
from time import sleep
from urllib import request


images_per_page = 42
#
#   utility functions
#
def clean_page(page):
	page = str(page).replace(r"\n", "\n")
	page = page.replace(r"\r", "\r")
	page = page.replace(r"\t", "\t")
	page = page.replace(r"amp;", "")
	return(page)
#
#   main functions
#
def get_page(URL):
	#stage 2
	#retrieve and return the index page
	try:
		print(URL)
		page = request.urlopen(URL)
		page = clean_page(page.read())
		page_file = open("index.html", "w+")
		page_file.write(page)
		return(page)
	except:
		raise Exception("cant retrieve and store file located at the given URL")
		sys.exit()
#
def build_list(index_file):
	#stage 3
	#build and return a list of image container page URLs to grab
	try:
		image_page_URL = "index.php?page=post&s=view&id="

		search_expression = '\"index\.php\?page=post\&s=view\&id=([0-9]*?)\"'
		search_results = re.findall(search_expression, index_file)

		page_list = []
		for i in search_results:
			page_list.append("http://gelbooru.com/" + image_page_URL + i)
		return(page_list)
	except:
		raise Exception("cant build wrapper page list")
		sys.exit()
#
def grab_files(page_list, update):
	#stage 4
	#with each container URL get the file, search for the image and then save it
	try:
		image_URL_prefix = r"gelbooru.com//images/" #frequently changed
		search_expression = image_URL_prefix + "(.*?\.jpg|.*?\.png|.*?\.gif|.*?\.jpeg)"
		for i in page_list:
			wrapper_page = get_page(i)
			image_URL_suffix = re.findall(search_expression, wrapper_page, re.IGNORECASE)[0]
			image_URL_domain = "http://simg3."

			image_name = ""
			for c in reversed(image_URL_suffix):
				if c != "/":
					image_name = image_name + c
				else:
					image_name = image_name[::-1]
					break
	
			if not (os.path.exists(output_directory + image_name) and update):
				image = request.urlopen(image_URL_domain + image_URL_prefix + image_URL_suffix)
				image_file = open(output_directory + image_name, "wb+")
				image_file.write(image.read())
			print(image_name + " saved")
	except:
		raise Exception("cant parse containers and/or save images")
		sys.exit()
#
#   main procedure
#

# stage 0
# parse args
if not (len(sys.argv) !=4 or len(sys.argv)) !=5: raise Exception("incorrect number of arguments")

try:
	gallery_URL, output_directory, pages = sys.argv[1], sys.argv[2] + "/", sys.argv[3]
except:
	raise Exception("cant process arguments")
	sys.exit()
try:
	if sys.argv[4] == "update": update = True
except:
	update = False

	
print("stage 0 complete")

# stage 1
# make directory
try:
	if not os.path.exists(output_directory):
		os.makedirs(output_directory)
except:
	raise Exception("cant make target directory")
	sys.exit()
print("stage 1 complete")

#stages 2-4
for i in range (0, int(pages)):
	print("processing page " + str(i))
	page_address = gallery_URL + "&pid=" + str(images_per_page * i)
	
	index_file = get_page(page_address)
	print("stage 2 complete")

	page_list = build_list(index_file)
	print(str(len(page_list)) + "  found")
	print("stage 3 complete")

	grab_files(page_list, update)
	print("stage 4 complete: page " + str(i) + " done")
print("completely fucking done")
#
