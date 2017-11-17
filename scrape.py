import time
import requests
import os
import click
from PIL import Image
from io import BytesIO
from selenium import webdriver


"""
Usage: scrape.py [OPTIONS]
  Web scraper, works with Image, Doc, Video
Options:
  --url TEXT           Website that you want to scrape
  --file_type TEXT     Type of files you want to scrape (Image, Doc, Video)
  --folder_prefix TEXT Folder prefix, where files will go
  --search BOOL          You want to search?
  --search_by TEXT     Seach keyword
  --help               Show this message and exit.
"""


driver = webdriver.Firefox(executable_path=r'geckodriver')


def open_url(url):
  # use Selenium web driver to open a page
  driver.get(url)


def get_images(url, selector, folder):
  ''' 
      Scrape image from provided URL and save 
      into provided folder
  '''

  # sroll the page and wait for 5s
  driver.execute_script("window.scrollTo(0, 500);")
  time.sleep(2)

  # select image elements and print their urls
  image_elements = driver.find_elements_by_css_selector(selector)

  for i, image_element in enumerate(image_elements):
    image_url = image_element.get_attribute("src")
    # use requests lib to download image and save into .images/ folder
    image_obj = requests.get(image_url)
    image = Image.open(BytesIO(image_obj.content))
    image.save(folder + "/image_" + str(i) + "." + image.format, image.format)


def do_search(search, search_by):
  # search for
  if search:
    inputElement = driver.find_element_by_id('searchKeyword')
    inputElement.send_keys(search_by)
    time.sleep(5)


def build_folder(folder_prefix, url):
  name = url
  if 'http' in url:
    name = url.split('.')[0].split('/')[-1]
  return folder_prefix + "-" + name


def create_folder(folder):
  # create a directory for future images
  if not os.path.exists(folder):
    os.makedirs(folder)


@click.command()
@click.option('--url', default='https://unsplash.com', help='Website that you want to scrape')
@click.option('--selector', default='#gridMulti img', help='Selector to where to get stuff from website')
@click.option('--file_type', default='image', help='Type of files you want to scrape (Image, Doc, Video)')
@click.option('--folder_prefix', default='./.images', help='Folder prefix, where files will go')
@click.option('--search', default=False, help='You want to search?')
@click.option('--search_by', default='', help='Seach keyword')
def scrape(url, selector, file_type, folder_prefix, search, search_by):
  try:
    folder = './.dir-' + build_folder(folder_prefix, url)
    create_folder(folder)
    open_url(url)
    if file_type == 'image':
      do_search(search, search_by)
      get_images(url, selector, folder)

    driver.quit()
  except Exception as ex:
    print("Exception: " + str(ex))
    driver.quit()

if __name__ == '__main__':
  scrape()
