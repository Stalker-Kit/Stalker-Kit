from Stalker import *
import sys

#run it from the comand line as: python3 test.py *fb username* *fb password*
a = Stalker()

print("login in to facebook")
a.login_facebook(sys.argv[1],sys.argv[2])
print("login successful")

print("Getting your friends list")
#Get your friends list URL
soup =  bs.BeautifulSoup(a.sess.body(), 'lxml')
link = soup.find('div', class_= '_5s61 _15n-').a['href']
a.sess.visit(link)
soup =  bs.BeautifulSoup(a.sess.body(), 'lxml')
link = soup.find_all('div', class_= '_4g34 _1hb')[2].a['href']

#actually gets your friends lits
b = a.get_friends_list(link)
print("done")

print("getting mutual friends with %s" %(list(b.keys())[0]))
c = a.get_friends_list(b[list(b.keys())[0]]['friends'])
f_list = [b,c]
mutual = Stalker.get_mutual_friends(f_list)

print("You and %s have %d mutual friends, here are their names:" %(list(b.keys())[0], len(mutual)) )
print (mutual)
