# bilibili-assistant-extension

<a href="docs/README_CN.md"><img src="https://img.shields.io/badge/文档-中文版-blue.svg" alt="CN doc"></a> <a href="README.md"><img src="https://img.shields.io/badge/Document-English-blue.svg" alt="EN doc"></a>

欢迎在 Chrome Web Store 下载体验拓展程序 [bilibili 哔哩哔哩推荐助手](https://chromewebstore.google.com/detail/bilibili%E5%93%94%E5%93%A9%E5%93%94%E5%93%A9%E6%8E%A8%E8%8D%90%E5%8A%A9%E6%89%8B/ebfdljhnmngegkbcllapegggoeopaicl)

## 爬虫程序

### `user_info_request.py` 是用来爬取 up 主相关个人信息例如头像链接,签名,大会员信息等的脚本

- 运行命令 `python3 user_info_request.py 0`
- 需要传入一个整数来确定运行哪一个 mid*chunk*{x}.json

### `hot_videos_crawler.py` 是用来爬取每个 category 当月热门排行的前 1000 个视频的脚本

- 运行命令 `python3 hot_videos_crawler.py`
- 每个类别的结果会单独保存到 csv 文件中
- 需要手动修改程序中的 year=20xx 来确定爬取哪一年的数据

## 数据处理脚本

数据处理脚本最后会生成一个 json 文件包含了每个 B 站 up 主 id 和对应相似 Up 主的 id list，然后再结合 user_info.json 来过滤筛选能够展示头像和签名的 Up 主，因为 user_info_request.py 爬虫可能没有爬到某些 up 主的账号信息

## EDA 数据分析

`/eda` 文件夹包括：

- **样例数据集**：`bili-hot-2019` 一个用于展示数据探索过程的代表性数据集。

- **用于 EDA 的 Python 脚本**：`bili-eda.ipynb` 一个用于对数据集进行探索性数据分析(EDA)和数据预处理的 Jupyter Notebook
