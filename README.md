# bilibili-assistant-extension

<a href="docs/README_CN.md"><img src="https://img.shields.io/badge/文档-中文版-blue.svg" alt="CN doc"></a> <a href="README.md"><img src="https://img.shields.io/badge/Document-English-blue.svg" alt="EN doc"></a>

You can install the extension from the Chrome Web Store [here](https://chromewebstore.google.com/detail/bilibili%E5%93%94%E5%93%A9%E5%93%94%E5%93%A9%E6%8E%A8%E8%8D%90%E5%8A%A9%E6%89%8B/ebfdljhnmngegkbcllapegggoeopaicl)

## Crawler Scripts

### `user_info_request.py`

This file is a script used to crawl personal information related to bilibili content creators, such as avatar links, signatures, premium membership info, etc.

- Run command: `python3 user_info_request.py 0`
- You need to pass an integer to determine which `mid*chunk*{x}.json` to use.

### `hot_videos_crawler.py`

This file is a script used to crawl the top 1000 videos of the current month's popular rankings for each category.

- Run command: `python3 hot_videos_crawler.py`
- The result for each category will be saved separately into a CSV file.
- You need to manually modify `year=20xx` in the program to specify which year's data to crawl.

## Data Processing Scripts

The data processing scripts will eventually generate a JSON file that includes each bilibili content creator and their corresponding similar author list. Currently, 30 users are selected, and then combined with `user_info.json` to filter bilibili content creators whose avatars and signatures can be displayed. This is because the `user_info_request.py` crawler might not have retrieved account information for some UP users.

## Exploratory Data Analysis

The `/eda` folder contains:

- **Sample Dataset**: `bili-hot-2019`, a representative dataset used to demonstrate the data exploration process.

- **Python Script for EDA**: `bili-eda.ipynb`, a Jupyter Notebook for performing Exploratory Data Analysis (EDA) and data preprocessing on the dataset.
