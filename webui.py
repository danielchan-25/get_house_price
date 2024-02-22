import time
import pymysql
import matplotlib.pyplot as plt
import datetime
import schedule

# -------------------------- #
# Date：2023-11-14
# Author：陈某
# Function：获取房价数据并画图
# -------------------------- #


# 获取历史数据
def get_data():
    conn = pymysql.connect(host='', user='', password='', database='HousePrice', port=3306)  # 填入数据库信息
    cursor = conn.cursor()
    cursor.execute(f'SELECT date,price FROM HousePrice;')
    conn.commit()
    result = cursor.fetchall()
    cursor.fetchone()
    cursor.close()
    conn.close()
    return result


# 生成曲线图
def main():
    data_list = [i for i in get_data()]
    date_list = []
    price_list = []

    for i in data_list:
        date_list.append(i[0])
        price_list.append(i[1])

    plt.figure(figsize=(10,7))
    plt.title('House Price')
    plt.xlabel('Date')
    plt.xticks(rotation=25)

    plt.ylabel('Price')
    plt.yticks()

    plt.plot(date_list, price_list)
    plt.savefig(r'static/HousePrice')
    plt.show()


schedule.every().day.at('06:00').do(main)
if __name__ == '__main__':
    while True:
        schedule.run_pending()
        print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} 已生成')
        time.sleep(60)
