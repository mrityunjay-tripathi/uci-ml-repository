import os, requests, threading

def Handler(url, saving_dir, filename, start, end):
    headers = {f"Range":"bytes={start}-{end}"}
    page = requests.get(url = url, headers = headers, stream = True)
    os.makedirs(saving_dir, exist_ok = True)
    with open(saving_dir + filename, 'w+b') as f:
        f.seek(start)
        # current_pos = f.tell()
        for chunk in page.iter_content(chunk_size = 2):
            if chunk:
                f.write(chunk)

def Download(url, saving_dir, filename, num_workers = 1):
    file_size = requests.head(url).headers['content-length']
    part = int(file_size)//num_workers
    remaining = int(file_size)%num_workers

    for i in range(num_workers):
        start = i*part
        if i==num_workers-1:
            end = start + part + remaining
        end = start + part
        t = threading.Thread(target = Handler, 
                             kwargs = {'url':url, 'saving_dir':saving_dir, 'start':start, 'end':end, 'filename':filename})
        t.setDaemon(True)
        t.start()
    
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()


def OpenLink(url):
    page = requests.get(url)
    return page.content.decode('utf-8')