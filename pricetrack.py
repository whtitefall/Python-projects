import requests 
from bs4 import BeautifulSoup 

import smtplib

URL = 'https://www.amazon.ca/DualShock%C2%AE4-Wireless-Controller-Gold-PlayStation/dp/B06Y4G5K5X?pf_rd_p=098688f8-6894-4652-bba1-98a4f36a372d&pf_rd_r=RYYCW7GA5JQGM4B6XEEM'


headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}

page = requests.get(URL,headers = headers) 

soup = BeautifulSoup(page.content,'html.parser')

title = soup.find(id ="productTitle")

price = soup.find(id = 'priceblock_ourprice').get_text()

converted_price = float(price[5:7])




def send_email():
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('whtitefall@gmail.com','chjakmdcpbwsiieg')

    subject = 'Price fell down'
    body = 'Check amazon link https://www.amazon.ca/DualShock%C2%AE4-Wireless-Controller-Gold-PlayStation/dp/B06Y4G5K5X?pf_rd_p=098688f8-6894-4652-bba1-98a4f36a372d&pf_rd_r=RYYCW7GA5JQGM4B6XEEM'

    msg = f"Subject : {subject}\n\n {body} "
    server.sendmail('whtitefall@gmail.com','bhu078@uottawa.ca',msg) 
    print ('email sent')
    server.close()


if (converted_price < 100):
    send_email()