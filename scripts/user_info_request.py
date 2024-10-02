import hashlib
import os
import requests
import concurrent.futures
import json
from functools import reduce
import urllib.parse
import time
import random
import sys
from queue import Queue

# 代理池
proxy_list = [
    'http://xuser1356:pass2356@193.160.82.132:6104',
]

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
    },
    {
        "Connection": "keep-alive",
        "DNT": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5"
    },
    {
        "Connection": "keep-alive",
        "DNT": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-us"
    },
    {
        "Connection": "keep-alive",
        "DNT": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-us"
    },
    {
        "Connection": "keep-alive",
        "DNT": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5"
    }
]

# API URL
USER_INFO_API = "https://api.bilibili.com/x/space/wbi/acc/info"
SLEEP_TIME_MIN = 1
SLEEP_TIME_MAX = 3


def read_mid_chunks():
    # 读取命令行参数并将其转换为整数
    try:
        mid_file_id = int(sys.argv[1])
    except ValueError:
        print("参数必须是一个整数")
        sys.exit(1)

    # Load mids from JSON file
    with open(f'mid_chunk_{mid_file_id}.json', 'r') as f:
        mids = json.load(f)
    return mids


def read_failure_mids(file_name):
    mids = []
    # 打开文件并逐行读取
    with open(file_name, 'r') as file:
        # 逐行读取文件内容
        for line in file:
            # 尝试将每行的内容转换为整数
            try:
                number = int(line.strip())
                mids.append(number)
            except ValueError:
                # 若转换失败则忽略该行
                print("not a valid number, skip this line")
                continue
    return mids

    """failure mids retry

    Returns:
        _type_: _description_
    """
# if len(sys.argv) > 1:
#     try:
#         failure_mids_file = sys.argv[1]
#     except ValueError:
#         sys.exit(1)
#     mids = read_failure_mids(failure_mids_file)
# print("xx len(mids):", len(mids))
# time.sleep(5)


mids = read_mid_chunks()

# Calculate chunk size
chunk_size = len(mids) // len(proxy_list)

# Split mids into chunks of calculated size
mid_chunks = [mids[i:i + chunk_size] for i in range(0, len(mids), chunk_size)]

wbi_img = {
    "img_url": "https://i0.hdslb.com/bfs/wbi/e117dc3d5f5a4c1b9a98ca8c77fda9bd.png",
    "sub_url": "https://i0.hdslb.com/bfs/wbi/727ddd621e1e4e99ab98d52d7de22f5b.png"
}


def split(key):
    return wbi_img.get(key).split("/")[-1].split(".")[0]


def get_mixin_key() -> str:
    ae = split("img_url") + split("sub_url")
    oe = [46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13,
          37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52]
    le = reduce(lambda s, i: s + (ae[i] if i < len(ae) else ""), oe, "")
    return le[:32]


mixin_key = get_mixin_key()
NUM_PER_BUCKET = 20


def enc_wbi(params: dict, mixin_key: str):
    """
    更新请求参数

    Args:
        params (dict): 原请求参数

        mixin_key (str): 混合密钥
    """
    params["wts"] = int(time.time())
    keys = sorted(filter(lambda k: k != "w_rid", params.keys()))
    Ae = "&".join(f"{key}={params[key]}" for key in keys)
    w_rid = hashlib.md5(
        (Ae + mixin_key).encode(encoding="utf-8")
    ).hexdigest()
    params["w_rid"] = w_rid


def send_request(proxy, headers, mid_chunks, worker_id):
    # if worker_id == 1 or worker_id == 11:
    #     with open(f'failure_mids_worker_{worker_id}.txt', 'a') as file:
    #         for author in mid_chunks:
    #             file.write(str(author['mid'][0]) + '\n')
    #     return
    results = []
    for i, author in enumerate(mid_chunks):
        try:
            # 这里的failure_mids是一个列表，里面存放的是请求失败的mid
            mid = author

            params = {"mid": mid}
            enc_wbi(params, mixin_key)
            print(
                f">>> Sending 第{i}个 author request for mid {mid}, params: {params}")
            response = requests.get(USER_INFO_API, proxies={
                                    "http": proxy, "https": proxy}, headers=headers, params=params)
            results.append(response.json())
            sleep_time = random.randint(SLEEP_TIME_MIN, SLEEP_TIME_MAX)
            print(
                f"$$$ 第{i}个 author {author} request 请求收到响应 {response.status_code} *** sleeping {sleep_time} s....")
            time.sleep(sleep_time)
            if (i + 1) % NUM_PER_BUCKET == 0 or i == len(mid_chunks) - 1:
                res_file_name = f'user_info_worker_{
                    worker_id}_checkpoint_{i // NUM_PER_BUCKET}.json'
                if i == len(mid_chunks) - 1:
                    print(f"$$$ 已经处理完所有author, 保存结果到文件 {res_file_name} ....")
                print(
                    f"@@@ 已经处理了{i + 1}个author, 保存结果到文件 {res_file_name} ....")
                # 检查文件是否存在
                if os.path.isfile(res_file_name):
                    # 文件存在，读取文件内容
                    with open(res_file_name, "r") as file:
                        existing_data = json.load(file)
                    # 将新的结果添加到文件内容中
                    existing_data.extend(results)
                    with open(res_file_name, "w") as file:
                        json.dump(existing_data, file)
                else:
                    # 文件不存在，新建文件并写入初始内容
                    with open(res_file_name, "w") as file:
                        json.dump(results, file)
                results = []  # Clear the results list
        except requests.exceptions.JSONDecodeError:
            sleep_time = random.randint(SLEEP_TIME_MIN, SLEEP_TIME_MAX)
            print(
                f"XXX 请求 author {author} 失败了, proxy 代理信息 {proxy} 添加到失败mid文件 xx_retry_{worker_id}.txt, 睡眠 {sleep_time // 2} s....")
            with open(f'xx_retry_{worker_id}.txt', 'a') as file:
                file.write(str(mid) + '\n')
            time.sleep(sleep_time // 2)
    return results


tasks = [(proxy_list[i % len(proxy_list)], headers_list[i % len(headers_list)], mid_chunks[i], i)
         for i in range(len(mid_chunks))]

# 开始计时
start_time = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=len(proxy_list)) as executor:
    futures = {executor.submit(send_request, *task)
                               : i for i, task in enumerate(tasks)}
    for i, future in enumerate(concurrent.futures.as_completed(futures)):
        result = future.result()
# 结束计时
end_time = time.time()

# 计算经过的时间
elapsed_time = end_time - start_time

# 打印结果
print("经过的时间：", elapsed_time, "秒")
