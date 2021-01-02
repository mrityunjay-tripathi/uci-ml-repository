import csv, re, optparse, notify2

from bs4 import BeautifulSoup
import urllib.request

from Hyperlink import Download, OpenLink    

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
    parser.add_option('--num_threads', dest = "num_threads", help = "Numbers of threads to be used")

    (options, arguments) = parser.parse_args()
    save_to = options.save_to
    num_threads = int(options.num_threads)
    i = 1
    
    notify2.init("Download Notifier")
    n = notify2.Notification(None, icon = "etc/thumbnail.png")
    n.set_urgency(notify2.URGENCY_NORMAL)
    n.set_timeout(2000)

    links = get_datasets_link(URL)
    print(links)
    for link in links:
        pattern = r'href="../machine-learning-databases/.+'
        data_folder_link = re.findall(pattern, OpenLink(URL + link))[0][8:-7]
        
        folder_name = data_folder_link.split('/')[2]
        downloadable_links = [l.split('>')[1][:-3]
                              for l in re.findall(r'href.*', OpenLink(URL + data_folder_link)[2:])][2:]
        for l in downloadable_links:
            dl_url = URL + 'machine-learning-databases/' + folder_name + '/' + l
            saving_dir = save_to + 'UCI-ML-DATASETS/' + str(i) + '.' + folder_name + '/'
            Download(url = dl_url, 
                     saving_dir = saving_dir, 
                     filename = l, 
                     num_threads = num_threads)
            n.update("UCI ML Repository Downloader", f"Downloaded : {folder_name}")
            # print(f"Downloaded : {folder_name}", end = "\r")
            n.show()
        i+=1