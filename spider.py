import time
import schedule
import requests
import json
import pymysql
import logging

# ------------------------------------------------------------- #
# Date：2023-11-14
# Author：陈某
# Function：获取安XX中，某地的房价，每天23:30运行
# ------------------------------------------------------------- #

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()


# 爬取当天的日期和房价
def get_Data():
    url = ''  # Url敏感已屏蔽，建议自己在F12里找
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    json_data = json.loads(response.text)
    today_data = json_data["data"]["priceTrend"][0]["area"][0]
    date = f'2024-{today_data["date"]}'
    price = today_data['price']
    logger.info(f'{date}的房价为：{price}')
    return date, price


# 将当天的房价写进数据库
def insert_db():
    logger.info('正在连接数据库...')
    date, price = get_Data()
    conn = pymysql.connect(host='', user='', password='', database='HousePrice', port=3306)  # 填入数据库信息
    cursor = conn.cursor()
    logger.info('数据库连接成功!')
    sql = f'INSERT INTO HousePrice (date,price) VALUES ("{date}","{price}");'
    cursor.execute(sql)
    conn.commit()
    cursor.fetchall()
    cursor.fetchone()
    cursor.close()
    conn.close()
    logger.info(f'已将{date},{price}成功写入数据库')
    logger.info(f'数据库已断开')

logger.info('爬虫已启动，等待23:30运行')
schedule.every().day.at("23:30").do(insert_db)
while True:
    schedule.run_pending()
    time.sleep(60)
