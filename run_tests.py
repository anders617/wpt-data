import requests
from time import sleep
from csv import writer
import os


def download(url, filename):
    req = requests.get(url)
    with open(filename, 'wb') as download_file:
        for chunk in req.iter_content(chunk_size=128):
            download_file.write(chunk)


def main():
    if not os.path.exists('data'):
        os.mkdir('data')
    with open('urls.txt', 'r') as urls, open('data/names.csv', 'w') as names_file:
        names_writer = writer(names_file)
        detail_urls = {}
        for url in urls:
            params = {
                'url': url,
                'f': 'json',
            }
            req = requests.get('http://76.112.208.162:18855/runtest.php', params=params)
            json = req.json()
            data = json['data']
            detail_urls[data['testId']] = data['detailCSV']
            names_writer.writerow([url, data['testId']])
        print(detail_urls)
        sleep(5)
        for test_id in detail_urls:
            finished = False
            while not finished:
                sleep(10)
                params = {
                    'test': test_id,
                    'f': 'json',
                }
                req = requests.get('http://76.112.208.162:18855/testStatus.php', params=params)
                json = req.json()
                status = int(json['statusCode'])
                finished = status == 200
            filename = 'data/' + test_id + '.csv'
            download(detail_urls[test_id], filename)
            pcap_url = 'http://76.112.208.162:18855/pcap/' + test_id + '_1.pcapng'
            filename = 'data/' + test_id + '.pcapng'
            download(pcap_url, filename)




if __name__ == '__main__':
    main()
