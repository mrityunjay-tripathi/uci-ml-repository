import urllib.request
import os, sys, re, getpass, requests
from Hyperlink import download_link, open_link
from bs4 import BeautifulSoup

URL = "https://archive.ics.uci.edu/ml/"
SAVE_TO = sys.argv[1]

def get_datasets_link(URL):
    
    page = urllib.request.urlopen(URL + 'datasets.php')
    soup = BeautifulSoup(page, 'lxml')

    table = soup.find_all('table')
    i=0
    links = []
    for row in table:
        link = row.a
        if link:
            l = link.get('href')
            links.append(l)
            
    return links[5:]



if __main__ == '__main__':
    for link in get_datasets_link(URL):

        PATTERN = r'href="../machine-learning-databases/.+'
        HTML_CODE = open_link(URL + link)
        data_folder_link = re.findall(PATTERN, HTML_CODE)[0][8:-7]
        
        FOLDER_NAME = data_folder_link.split('/')[2]
        downloadable_links = [l.split('>')[1][1:-3]
                              for l in re.findall(r'href.*', open_link(URL + data_folder_link)[2:])]

        for l in downloadable_links:
            
            if l != 'Parent Directory':
                dl_url = URL + 'machine-learning-databases/' + FOLDER_NAME + '/' + l
                #saving_dir = '/home/{}/Downloads/UCI-ML-DATASETS/'.format(getpass.getuser()) + FOLDER_NAME + '/'
                saving_dir = SAVE_TO + 'UCI-ML-DATASETS/' + FOLDER_NAME + '/'
                download_link(dl_url, saving_dir, l)

    
    
