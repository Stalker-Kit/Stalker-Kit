import bs4 as bs
import requests
from requests.exceptions import HTTPError
import dryscrape
import time
from collections import Counter
def get_num(x):
    return int(''.join(ele for ele in x if ele.isdigit()))

class Stalker(object):
    
    def login_facebook(self, user, password):
        self.sess = dryscrape.Session(base_url="https://www.facebook.com/")
        sess = self.sess
        sess.set_attribute('auto_load_images', False)
        sess.visit("/login")
        f = sess.at_xpath('//*[@name="email"]')
        f.set(user)
        f = sess.at_xpath('//*[@name="pass"]')
        f.set(password)
        f.form().submit()
        # sess.visit("/")
        #sess.render("login.png")

    def get_friends_list(self, url):
        sess = self.sess
        sess.visit(url)
        elem = sess.wait_for_safe(lambda: sess.at_xpath('//*[@class="_3d0"]')) #Waits until for right class to be loaded
        friends = {}
        
        soup =  bs.BeautifulSoup(sess.body(), 'lxml')
        #Get the total amount of friends available, if the text is empty(protected) just assume a lage number
        if (soup.find('div', class_= '_5h60 _30f').find(class_ = '_3d0').text != ''):
            print(soup.find('div', class_= '_5h60 _30f').find(class_ = '_3d0').text)
            num_friends = get_num(soup.find('div', class_= '_5h60 _30f').find(class_ = '_3d0').text) 
        else:
            num_friends = 5000
        
        #Try to get at least 98% of the friends list or do 100 trys
        trys = 0
        while((len(soup.find('div', class_= '_5h60 _30f').find_all('li', class_ = '_698')) < (float(num_friends)*0.98)) and (trys < 100)):
            trys += 1
            sess.exec_script("scroll(0, 99999);")
            time.sleep(0.1)
            soup =  bs.BeautifulSoup(sess.body(), 'lxml')
            print(len(soup.find('div', class_= '_5h60 _30f').find_all('li', class_ = '_698')), trys)
        
        #Put all friends found in a dictionary
        soup =  bs.BeautifulSoup(sess.body(), 'lxml')
        for c in soup.find_all('li', class_ = '_698'):
            #print(c)
            if (c.find('div', class_ = 'fsl fwb fcb') != None):
                name = c.find('div', class_ = 'fsl fwb fcb')
                page = c.find('div', class_ = 'fsl fwb fcb').a
                link = c.find('a', class_ = '_39g5')
            else:
                name = None
                page = None
                link = None

            if((name != None) and (link != None) and (page != None)):
                friends.update({name.text : {'page': page['href'], 'friends': link['href']} })
            elif((name != None) and (page != None)):
                friends.update({name.text : {'page': page['href']}})
        return friends
    
    #Get the mutual friends between a list of dictionaries of N friends
    def get_mutual_friends(friends_list):
        mutual = {}
        i = 0
        for a in friends_list:
            if i == 0:
                mutual = a.keys()
                i = 1
            mutual = a.keys() & mutual
        return mutual
    
    #Get the popularity index of a person among a list of friends
    def get_popularity(friends_list):
        l = []
        for a in friends_list:
            for b in a.keys():
                l.append(b)
        data = Counter(l)
        return data.most_common()

