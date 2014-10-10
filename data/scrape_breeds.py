from bs4 import BeautifulSoup
import requests

class Writer(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, text, mode="a"):
        f = open(self.file_name, mode)
        f.write(text.encode('utf-8'))
        f.close()


def get_breeds_on_type_page(url, type_name, writer):
  page = requests.get(url).text
  soup = BeautifulSoup(page)
  for breedPost in soup.findAll('div', { 'class': 'breedPost' }):
    name = breedPost.find('h3').text
    writer.write(name + "," + type_name + "\n")

def run():
  writer = Writer("breed_index.csv")
  writer.write("breed,breed_type\n")

  base_url = "http://www.ckc.ca/en/Choosing-a-Dog/Choosing-a-Breed"
  page = requests.get(base_url).text
  soup = BeautifulSoup(page)
  for breedType in soup.find('div', {'id': 'bodyContent'}).findAll('div', { 'class': 'featured' }):
    header = breedType.find('h2')
    if header:
      if header.text == "All Dogs":
        continue
      type_name = header.text
      print type_name
      url = "http://www.ckc.ca" + header.find('a').get('href')
      print "Visiting " + url
      get_breeds_on_type_page(url, type_name, writer)

run()