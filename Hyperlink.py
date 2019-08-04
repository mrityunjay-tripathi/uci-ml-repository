import os, requests

def download_link(link, saving_dir, filename):
    page = requests.get(link, stream = True)
    os.makedirs(saving_dir, exist_ok = True)
    with open(saving_dir + filename, 'wb') as f:
        for chunk in page.iter_content(chunk_size = 2):
            if chunk:
                f.write(chunk)


def open_link(url):
    
    page = requests.get(url)
    return page.content.decode('utf-8')

