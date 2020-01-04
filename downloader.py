import re, optparse

from bs4 import BeautifulSoup
import urllib.request, requests

from Hyperlink import Download, OpenLink


URL = "https://archive.ics.uci.edu/ml/"

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


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--save_to', dest = "save_to", help = "download location")
    parser.add_option('--num_workers', dest = "num_workers", help = "Numbers of threads to be used")

    (options, arguments) = parser.parse_args()
    save_to = options.save_to
    num_workers = int(options.num_workers)
    i = 1
    
    for link in get_datasets_link(URL):
        pattern = r'href="../machine-learning-databases/.+'
        data_folder_link = re.findall(pattern, OpenLink(URL + link))[0][8:-7]
        
        folder_name = data_folder_link.split('/')[2]
        downloadable_links = [l.split('>')[1][:-3]
                              for l in re.findall(r'href.*', OpenLink(URL + data_folder_link)[2:])][2:]
        for l in downloadable_links:
            dl_url = URL + 'machine-learning-databases/' + folder_name + '/' + l
            saving_dir = save_to + 'UCI-ML-DATASETS/' + str(i) + '.' + folder_name + '/'
            print(f"Downloading : {folder_name}", end = "\r")
            Download(url = dl_url, 
                     saving_dir = saving_dir, 
                     filename = l, 
                     num_workers = num_workers)
        i+=1