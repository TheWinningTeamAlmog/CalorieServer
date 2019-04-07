from instagram_scraper.app import InstagramScraper
from selenium import webdriver
import argparse

def get_followers(username):
    # download html
    url = "https://www.instagram.com/" + username

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)

    browser.get(url)
    content = browser.page_source

    followers_start = "<link rel=\"canonical\" href=\"https://www.instagram.com/" + username + "/\" />"
    followers_pos = content.find(followers_start)
    followers_pos_start = content.find("content", followers_pos) + len("content=\"")
    followers_pos_end   = content.find(" ", followers_pos_start)
    print(int(content[followers_pos_start:followers_pos_end]))

def get_full_info(username):
    output_path = "/tmp/inst_scraper/"

    # Get data
    scraper = InstagramScraper(usernames=[username], 
                                 login_user="hackathon1293", 
                                 login_pass="ibmRULZ7419",
                                 comments=True,
                                 media_types=["none"],
                                 destination=output_path)
    scraper.authenticate_with_login()
    scraper.scrape()

    # Parse json
    json_path = output_path + username
    
def get_avg_likes(username):


def get_user_metadata(usrname):
    followers = get_followers(username)




def main():
    get_followers("netaalon22")

main()


{
        "name": "\\",
        "followers": "\\number\\",
        "photos": [ { 
                "image" : "\\base64\\",
                "comments" : [""],
                "description": "",
                "tags": [""],
                "likes": "\\number\\"
        } ]
}
