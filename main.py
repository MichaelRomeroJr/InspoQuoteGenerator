# -*- coding: utf-8 -*-
import random
import os 
import pathlib
from selenium import webdriver
from time import sleep

import argparse
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import urllib
import urllib.request

import cv2
import pytesseract
from pytesseract import image_to_string

def configure_chrome_driver():  
	options = webdriver.ChromeOptions()  
	options.add_argument(f"user-data-dir={pathlib.Path(__file__).parent.absolute().joinpath('chrome-profile')}")  		
	
	DRIVER_EXECUTABLE_PATH = pathlib.Path(__file__).parent.absolute().joinpath("chromedriver.exe")  
	the_driver = webdriver.Chrome(executable_path=DRIVER_EXECUTABLE_PATH, options=options)  

	#the_driver = webdriver.Chrome('/mnt/c/Python/chromedriver.exe') # hardcode path
	return the_driver


def query_tumblr(driver):
	"""
		click on search bar and pass "inspirational  quotes" as string
		press Enter
	"""
	
	driver.get("https://www.tumblr.com/")
	sleep(1)

	# click on search bar
	driver.find_element_by_name("q").click()

	# Send keys w/o clicking on element 
	actions = ActionChains(driver)
	actions.send_keys("inspirational  quotes")			

	actions.send_keys(Keys.RETURN)
	actions.perform()			
	return


def get_main_link(links):
	"""
		return largest url of largest image
	"""
	comma_index = links.rfind(",") + 2 # remove ", "
	largest_image = links[comma_index:-5] # remove "540w" 
	return largest_image
	

def get_images(driver):
	"""
		Find url of jpeg from finding elements by class name
		return list of each url
	"""
	sleep(5)

	images = []
	web_elements = driver.find_elements_by_class_name("_3raF7")

	for elem in web_elements:
		try:
			image_elem = elem.find_element_by_class_name("_1czZp ")
			image_links = image_elem.get_attribute("srcset")

			# each image has list of links for different image size
			image_url = get_main_link(links = image_links)
			images.append(image_url)
		except:
			# not an image element
			pass

	return images


def save_image(driver, path):
	"""
		load image url and save in root folder 
		url is either direct link (saved in try block)
		or it's a url of an account (saved in except block)
	"""

	chrome_driver.get(image)

	try:
		img = chrome_driver.find_element_by_xpath("/html/body/img")
		
	except:
		# when image link lands on tumblr page 
		img = chrome_driver.find_element_by_xpath("/html/body/div/div/div[3]/div/div[1]/div/img")	
	
	src = img.get_attribute('src')	
	urllib.request.urlretrieve(src, path)

	return


def get_text(path):
	"""
		load image from saved path
		use pytesseract to extract text from movitional quote image
	"""

	img = cv2.imread(path)
	image_text = pytesseract.image_to_string(img)

	return image_text

if __name__ == '__main__':
	chrome_driver = configure_chrome_driver()
	
	# search for "inspirational quotes" in search bar
	query_tumblr(driver=chrome_driver)

	# list of urls of inspirational  quotes on tumblr
	inspo_images = get_images(driver=chrome_driver)

	count=0
	#root = "/mnt/c/Python/images/" # where to save images
	root = os.path.dirname(os.path.realpath(__file__)) + "/images/"

	for image in inspo_images:	
		# save as 0.png in root folder	
		image_path = root + str(count) + ".png"
		
		# load image url and save to folder
		save_image(driver=chrome_driver, path=image_path)

		# open image from folder and extract text
		inspo_quote = get_text(path=image_path)

		print(f"Quote {count}: {inspo_quote}")
		count+=1


	"""
		debugging loop since images are saved
	"""
	# for count in range(5):
	# 	random_index = random.randint(0, 35)
	# 	image_path = root + str(random_index) + ".png"
		
	# 	#save_image(driver=chrome_driver, path=image_path)

	# 	inspo_quote = get_text(path=image_path)

	# 	print(f"Quote {count}: \n{inspo_quote}")
