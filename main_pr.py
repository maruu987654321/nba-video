from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup  
from selenium.common.exceptions import NoSuchElementException        
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import WebDriverException
import requests
import io
import bs4
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
import youtube_dl
import requests
from nba_api.stats.static import teams
import logging
import base64

all_team = teams.get_teams()

title = []
new_date = []
date = []
month_numbers = {'JAN-': '01-', 'FEB-': '02-', 'MAR-': '03-', 'MAY-': '04-', 'JUN-': '05-', 'JUL-': '07-', 'AUG-': '08-', 'SEP-': '09-', 'OCT-': '10-', 'NOV-': '11-', 'DEC-': '12-'}
dict_abbreviture = dict()
list_for_title = []

def login():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--mute-audio")
    #chrome_options.add_argument("--headless") 
    driver = webdriver.Chrome("webdriver/chromedriver", options=chrome_options)
    driver.get('https://watch.nba.com')
    action = action_chains.ActionChains(driver)
    session_id = driver.session_id
    ext_button = driver.find_element_by_class_name('extend-account')
    ext_button.click()
    bitton_login = driver.find_element_by_id('loginButton')
    bitton_login.click()
    time.sleep(3)
    driver.switch_to.frame(driver.find_element_by_id("signInFrame"))
    driver.find_element_by_xpath("//input[@id='iptvauth_field_username']").send_keys("alykhansomani@gmail.com")
    pass_and_enter = driver.find_element_by_xpath("//input[@type='password']")
    pass_and_enter.send_keys("mamlakahat32")
    driver.find_element_by_class_name('nba-signin-btn').click()
    
    return driver

def get_date(j):
    for k, v in month_numbers.items():
        if k in j:
            date2 = j.replace(k, v)
            date3 = date2.split('-')
            new_date2 = date3[2] + date3[0] + date3[1]
            new_date2 = new_date2.replace(' ', '')
    return new_date2

def down_new_video(url):
    all_links =[]
    page = requests.get(url)
    c = page.content
    soup = BeautifulSoup(c)
    mydivs = soup.findAll("a", {"class": "medium square otw-button"})
    for i in mydivs:
        all_links.append(i['href'])
    for j in all_links:
        if 'st' in j:
            video = requests.get(j)
            c2 = video.content
            soup2 = BeautifulSoup(c2)
            sr_vi = soup2.find_all('iframe')[0]['src']
            name_vid = sr_vi.split('/')[-1]
            ydl_opts = {'outtmpl': name_vid}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([sr_vi])
                subprocess.call("ffmpeg -i {} -vcodec copy -acodec copy -ss 00:00:12 {}.mp4".format(name_vid, name_vid), shell=True)
                os.remove(name_vid)
                print('Download {}'.format(name_vid))


def hight_light(url):
    driver.get(url)
    driver.find_element_by_class_name("cookie-close").click();
    driver.find_element_by_xpath("/html/body/div[8]/div[2]/div[4]/div[3]").click()
    name_info = driver.find_element_by_id('components')
    soup = BeautifulSoup(name_info.get_attribute('innerHTML'))
    divs_name_video = soup.findAll("div", {"class": "desc-lines"})
    for i in divs_name_video:
        list_for_title.append(i['title'])
    actions = ActionChains(driver)
    for _ in range(1):
        actions.send_keys(Keys.SPACE).perform()
    
    
    video_img = driver.find_elements_by_class_name('video-play')
    for k, v in zip(range(1, len(list_for_title)), list_for_title):
        time.sleep(3)
        video_img[k].click()
        time.sleep(8)
        driver.switch_to.frame(driver.find_element_by_id("videoPlayer"))
        video_info = driver.find_element_by_id("playerContainer")
        soup = BeautifulSoup(video_info.get_attribute('innerHTML'))
        url_video = soup.find("video").get("src")
        driver.find_element_by_class_name('closeBtn').click()
        driver.switch_to.default_content()
        ydl_opts = {'outtmpl': v}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url_video])
                
                
if __name__ == '__main__':
    what_need = b'aHR0cDovL25iYWhkcmVwbGF5LmNvbS8=' 
    page = requests.get(base64.b64decode(what_need).decode("utf-8") )
    c = page.content
    soup = BeautifulSoup(c)
    mydivs = soup.findAll("a", {"class": "clip-link"})
    driver = login()
    print('Login successful')
    session_id = driver.session_id
    for i in mydivs:
        down_new_video(i['href'])
        j = i['title'].split('–')[1]
        new_date2 = get_date(j)
        file1 = open("all_team_and_date.txt","w") 
        file1.writelines(i['title'])
        file1.close()
        name = i['title'].split('–')[0]
        a = i['title'].split('–')[0].split('vs')
        first = a[0].lstrip()
        first = first.strip()
        second = a[1].strip()
        second = second.lstrip()
        if second == 'LA Clippers':
            second = teams.find_teams_by_full_name('Los Angeles Clippers')[0]['abbreviation']
        elif first == 'LA Clippers':
            first = teams.find_teams_by_full_name('Los Angeles Clippers')[0]['abbreviation']
        else:
    
            frst = teams.find_teams_by_full_name(first)[0]['abbreviation']
            sec = teams.find_teams_by_full_name(second)[0]['abbreviation']
            url_for_high = 'https://watch.nba.com/game/{}/{}'.format(new_date2, frst + sec)
            hight_light(url_for_high)
    logging.basicConfig(filename="sample.log", level=logging.INFO)
