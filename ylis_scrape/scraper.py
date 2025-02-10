from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import mariadb
import sys
import os
from dotenv import load_dotenv
#import openai 

load_dotenv()


try:
    conn = mariadb.connect(
        user = os.getenv('SQL_USER'),
        password = os.getenv('SQL_PASS'),
        host = "127.0.0.1",
        port = 3306,
        database = os.getenv('DATABASE')

    )
except mariadb.Error:
    print(mariadb.Error)
    sys.exit(1)

cursor = conn.cursor()


options = webdriver.ChromeOptions()
options.add_argument("--headless") 
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")





msg_limit = 1000

def get_matching_posts(id_and_msg, key):

     
    matched_posts = {}
    
    for thread_id, message in id_and_msg.items():
        if key.lower() in message.lower():
            matched_posts[thread_id] = message
            

    return matched_posts



        
def get_all_posts(url, keyword):
    driver = webdriver.Chrome(options=options)

    try:

        driver.get(url)
        time.sleep(1)

        id_and_message = {}


        soup = BeautifulSoup(driver.page_source, "html.parser")
        threads = soup.find_all('div', class_="card thread op-post op has-file")
        body = driver.find_element(By.TAG_NAME, 'body')
        scroll_pause_time = 0.005
        scroll_count = 0

        while len(id_and_message) != msg_limit:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            threads = soup.find_all('div', class_="card thread op-post op has-file")
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(scroll_pause_time)

            for i in threads:
                thread_ids = i.get("data-thread-id")
                message_tag = i.find("div", class_="message")
                message = message_tag.get_text()
                id_and_message[thread_ids] = message
                
                matched_post_dict = get_matching_posts(id_and_message, keyword)
            print(f"Collected {len(id_and_message)} posts so far...")
            scroll_count += 1
            if scroll_count == 60:
                print("max scrolls")
                break
    finally:
        driver.quit()   
        return matched_post_dict

    


def add_to_db(matched, key,):
    for i, j in matched.items():
        cursor.execute(
            "INSERT INTO post_and_keyword (id, message, keyword) VALUES (?, ?, ?)",
            (i, j, key)
        )
    conn.commit()

"""def sentiments_analysis(posts_to_analyze):
    openai.api_key = os.getenv('GPT_KEY')
    
    results = []
    for i in posts_to_analyze.items():

        
        completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a sentiment analyzer who analyzes message forum posts. Only use the words positive, negative, neutral."},
            
        ])
        results.append(completion.choices[0].message)
"""


    


        


#if __name__ == "__main__":
 #   all_posts_dict = get_all_posts()
  #  matched_posts = get_matching_posts(all_posts_dict, KEYWORD)
   # print(matched_posts)
    #if len(matched_posts) != 0:
     #   add_to_db(matched_posts, KEYWORD)
    #else:
     #   print("No matching posts")