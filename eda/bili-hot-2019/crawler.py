import requests
import csv
import random
import requests
import json
import threading
import time
import csv
import requests
import concurrent.futures
from threading import Lock
from itertools import cycle

# 代理池
proxy_list = cycle([
    'http://xuser1356:pass2356@216.170.122.111:6149',
    'http://xuser1356:pass2356@216.170.122.97:6135',
    'http://xuser1356:pass2356@45.196.33.88:6069',
    'http://xuser1356:pass2356@154.194.16.89:6008',
    'http://xuser1356:pass2356@45.196.52.190:6205',
    'http://xuser1356:pass2356@193.160.83.178:6499',
    'http://xuser1356:pass2356@154.194.24.186:5796',
    'http://xuser1356:pass2356@45.196.63.92:6726',
    'http://xuser1356:pass2356@192.46.200.219:5889',
    'http://xuser1356:pass2356@45.196.52.174:6189',
    'http://xuser1356:pass2356@192.53.137.0:6288',
    'http://xuser1356:pass2356@154.194.16.213:6132',
    'http://xuser1356:pass2356@45.196.54.246:6825',
    'http://xuser1356:pass2356@192.53.69.55:6693',
    'http://xuser1356:pass2356@185.253.122.209:6018',
    'http://xuser1356:pass2356@185.253.122.150:5959',
    'http://xuser1356:pass2356@185.253.122.249:6058',
    'http://xuser1356:pass2356@193.160.83.184:6505',
    'http://xuser1356:pass2356@193.160.82.26:5998',
    'http://xuser1356:pass2356@193.160.82.36:6008' 
])

# headers
headers_list = [
    {
        "Connection": "keep-alive",
        "DNT": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    },
    {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
        "Accept-Encoding": "gzip, deflate", 
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", 
        "Dnt": "1", 
        "Host": "httpbin.org", 
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36", 
    },
    {
        "Connection": "keep-alive",
        "DNT": "1",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    },
    {
        "Connection": "keep-alive",
        "DNT": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    },
    {
        "Connection": "keep-alive",
        "DNT": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5"
    },
    {
        "Connection": "keep-alive",
        "DNT": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-us"
    }
]

month_to_days = {
    1: '31',
    2: '28',
    3: '31',
    4: '30',
    5: '31',
    6: '30',
    7: '31',
    8: '31',
    9: '30',
    10: '31',
    11: '30',
    12: '31',
}

HOT_VIDEOS_API = 'https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=click&copy_right=-1&cate_id={cate_id}&page={page}&pagesize={page_size}&jsonp=jsonp&time_from={timestamp_start}&time_to={timestamp_end}'
USER_STAT_API = 'https://api.bilibili.com/x/relation/stat?vmid={vmid}'
VIDEO_INFO_API = 'https://api.bilibili.com/x/web-interface/archive/stat?bvid={bvid}'
PAGE_RANGE = range(1, 11)
SLEEP_TIME_LOW = 5
SLEEP_TIME_HIGH = 15
PAGE_SIZE = 100
THREAD_COUNT = 30
RETRY_COUNT = 3

# 5月份首次尝试过的分类 '121', '122', '124', '126', '127',
TEST_CATE_IDS = ['121', '122']
CATEGORY_IDS = ['121', '122', '124', '126', '127','130', '136', '137', '138', '145', '146', '147', '152', '153', '154', '156', '157', '158', '159', '161', '162', '164', '168', '169', '17', '170', '171', '172', '173', '174', '176', '178', '179', '182', '183', '184', '185', '187', '19', '193', '195', '197', '198', '199', '20', '200', '201', '203', '204', '205', '206', '207', '208', '209', '21', '210', '212', '213', '214', '215', '216', '218', '219', '22', '220', '221', '222', '227', '229', '230', '231', '232', '233', '235', '236', '237', '238', '239', '24', '240', '241', '242', '243', '244', '245', '246', '247', '248', '249', '25', '250', '251', '252', '253', '254', '255', '26', '27', '28', '29', '30', '31', '32', '33', '37', '47', '51', '59', '65', '71', '75', '76', '83', '85', '86', '95']
# CATEGORY_IDS = ['169', '17', '170', '171', '172', '173', '174', '176', '178', '179', '182', '183', '184', '185', '187', '19', '193', '195', '197', '198', '199', '20', '200', '201', '203', '204', '205', '206', '207', '208', '209', '21', '210', '212', '213', '214', '215', '216', '218', '219', '22', '220', '221', '222', '227', '229', '230', '231', '232', '233', '235', '236', '237', '238', '239', '24', '240', '241', '242', '243', '244', '245', '246', '247', '248', '249', '25', '250', '251', '252', '253', '254', '255', '26', '27', '28', '29', '30', '31', '32', '33', '37', '47', '51', '59', '65', '71', '75', '76', '83', '85', '86', '95']
YEARS = [2021, 2022, 2023]

# 创建一个锁对象来保护错误日志文件的写入操作
lock = Lock()

def fetch_data(cate_id, page, year, month):
    if month < 10:
        month_string = f'0{month}'
    else:
        month_string = str(month)
    timestamp_start = f'{year}' + month_string + '01'
    timestamp_end = f'{year}' + month_string + month_to_days[month] 
    url = HOT_VIDEOS_API.format(cate_id=cate_id, page=page, page_size=PAGE_SIZE, timestamp_start=timestamp_start, timestamp_end=timestamp_end)
    for count in range(RETRY_COUNT):
        try:
            sleep_time = random.randint(SLEEP_TIME_LOW, SLEEP_TIME_HIGH)
            with lock:  # 添加锁来保证线程安全
                proxy = next(proxy_list)
                headers = random.choice(headers_list)
            response = requests.get(url, timeout=20, proxies={"http": proxy, "https": proxy}, headers=headers)
            if (response.status_code == 403):
                print(f'XXXX 爬取category {cate_id} year {year} month {month} 第{page}页 第{count}次 请求出错, sleep {sleep_time} 秒后重试, 收到403 response, response.text: {response.text}')
                time.sleep(sleep_time)
                continue
            if (response.status_code == 200):
                print(f'*** 200 OK 请求, 爬取category {cate_id} year {year} month {month} 第{page}页 第{count}次成功, sleep {sleep_time} 秒')
            response.raise_for_status()
            time.sleep(sleep_time)
            return response.json()
        except requests.RequestException as e:
            with lock:
                with open('error.txt', 'a') as f:
                    f.write(f'爬取category {cate_id} year {year} month {month} 第{page}页 第{count}次请求 报错' + str(e) + '\n')
            print(f'XXX 爬取category {cate_id} year {year} month {month} 第{page}页 第{count}次 请求出错, 报错 + {str(e)} sleep {RETRY_COUNT * 5} 秒后重试')
            time.sleep(RETRY_COUNT * 5)
    return None
    
def worker(cate_id):
    year = 2019
    filename = f'cate_id_{cate_id}_{year}.csv'
    header = ['bvid', 'arcurl', 'title', 'pubdate', 'rank_offset', 'author', 'mid', 'play', 'review', 'video_review', 'favorites', 'duration', 'tag', 'description' ]
    # header = ['BVid', '视频链接', '视频标题', '视频发布时间', '视频当月排名','视频作者', '作者mid', '视频播放量', '视频评论数', '视频弹幕数', '视频收藏量', '视频时长-秒数', '视频标签', '视频描述']
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for month in range(1, 12):
            for page in PAGE_RANGE:
                data = fetch_data(cate_id, page, year=year, month = month)
                parsed_rows = parse_data(data)
                if parsed_rows:
                    # 写入csv文件，需要根据实际的数据结构进行修改
                    writer.writerows(parsed_rows)
                else:
                    print(f"XXX no results, 爬取 爬取category {cate_id} year {year} month {month} 第{page}页 第{count}次 失败, response 结果" + str(data))

def parse_data(data):
    rows = []
    keys_to_select = ['bvid', 'arcurl', 'title', 'pubdate', 'rank_offset', 'author', 'mid', 'play', 'review', 'video_review', 'favorites', 'duration', 'tag', 'description' ]
    for item in data['result']:
        rows.append([item[key] for key in keys_to_select])
    return rows

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        # update this CATE_IDS field to the category ids you want to crawl
        executor.map(worker, CATEGORY_IDS)

if __name__ == "__main__":
    main()
