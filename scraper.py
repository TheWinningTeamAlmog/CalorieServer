from instagram_scraper.app import InstagramScraper
from selenium import webdriver
import json
from flask import Flask, request
import os
import requests
from threading import Thread

app = Flask(__name__)

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
    multiplier = 1
    if content[followers_pos_end-1] == 'k':
        followers_pos_end-=1
        multiplier = 1000
    elif content[followers_pos_end-1] == 'm':
        followers_pos_end-=1
        multiplier = 1000000


    return int(float(content[followers_pos_start:followers_pos_end].replace(',', ''))*multiplier)
def get_avg_likes(username):
    return 112   
def get_full_info_local(username, max):
    output_path = "/tmp/inst_scraper/"

    #Get data
    if not os.path.isfile(output_path + username + ".json"):
        scraper = InstagramScraper(usernames=[username], 
                                   comments=True,
                                   media_types=["none"],
                                   tag=True,
                                   maximum=max,
                                   destination=output_path)
        scraper.authenticate_as_guest()
        scraper.scrape()

    # Parse json
    json_path = output_path + username + ".json"
    
    parsed_json = {}
    output_json = {}

    with open(json_path, "r") as json_file:
        parsed_json = json.loads(json_file.read())
    
    output_json["name"] = username
    output_json["followers"] = get_followers(username)
    output_json["photos"] = []

    total_likes = 0
    for obj in parsed_json["GraphImages"]:
        photo_obj = {}
        image = obj["display_url"]
        tags = obj.get("tags", [])
        likes = obj["edge_media_preview_like"]["count"]

        comments = []
        for comment in obj["comments"]["data"]:
            comments.append(comment["text"])

        total_likes += likes

        photo_obj["image"] = image
        photo_obj["comment"] = comments
        photo_obj["tags"] = tags
        photo_obj["likes"] = likes

        output_json["photos"].append(photo_obj)
    
    output_json["likes_avg"] = total_likes / len(parsed_json["GraphImages"])

    return json.dumps(output_json, ensure_ascii=False).encode('utf-8')

@app.route("/user_full_info")
def get_full_info():
    username = request.args.get('user')
    max  = int(request.args.get('max', 50))


    return get_full_info_local(username, max)
def research_local():
    if os.path.isfile("res"):
        with open("res", "r") as res:
            return res.read()

    return ""

@app.route("/db")
def research():
    return research_local()
    return "db"


@app.route("/")
def hello():
    return "Hello World"

def get_lables(url):
    resp = requests.get(url ="https://eu-gb.functions.cloud.ibm.com/api/v1/web/shmueljacobs%40gmail.com_dev/Test/weather.json",
                    params={"url" : url})
    resp_json = json.loads(resp.text)
    
    if "features" not in resp_json:
        print("Featureless")
        return []

    return json.loads(resp.text)["features"]
     
def get_features_local():
    db = json.loads(research_local())["db"]
    output_json = {}
    output_json["persons"] = []

    if os.path.isfile("feat"):
        with open("feat", "r") as feat:
            return feat.read()
    for person in db:
        inner_obj = {}
        inner_obj["name"] = person["name"]
        inner_obj["likes_avg"] = person["likes_avg"]
        inner_obj["followers"] = person["followers"]
        print(person["name"])

        photos = person["photos"]
        inner_obj["photos"] = []
        
        counter = 0
        for photo in photos:
            inner_photo = {}
            inner_photo["tags"] = photo["tags"]
            inner_photo["likes"] = photo["likes"]
            inner_photo["lables"] = get_lables(photo["image"])
            inner_photo["commnets"] = photo["comment"]
            inner_obj["photos"].append(inner_photo)
            counter+=1
            print(str(counter) + "/" + str(len(photos)))
            
        print("done")
        
        output_json["persons"].append(inner_obj)
    
    feat_dump = json.dumps(output_json)

    with open("feat", "w") as feat:
            feat.write(feat_dump)

    return feat_dump
    

@app.route("/feat")
def get_features():
    return get_features_local()

@app.route("/user_meta_data")
def get_user_metadata():
    username = request.args.get('user')

    followers = get_followers(username)
    avg_likes = get_avg_likes(username)

    data = {}
    data['name']      = username
    data['followers'] = followers
    data['avg_likes'] = avg_likes

    return json.dumps(data)

app.run()

