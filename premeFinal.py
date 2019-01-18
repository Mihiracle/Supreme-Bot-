import mechanize 
import BeautifulSoup
from bs4 import BeautifulSoup
import time

REALNAME = ""
email = ""
tel = "" 
zipcode = ""
street = ""
city = ""
state = "WA"
cType = ""
cNumberTest = "1234123412341234"
cNumberReal = ""
cMonth = ""
cYear = ""
cvv = "" 
url = "http://www.supremenewyork.com/shop/all/"
checkoutUrl = "https://www.supremenewyork.com/checkout"
hostUrl = "http://www.supremenewyork.com"

# Initialize mechanize headless browser
br = mechanize.Browser(factory=mechanize.RobustFactory())
br.set_handle_robots(False)
br.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'), 
				 ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
]

#This method takes the gzipped checkout form and makes it usable by mechanize
def soupify_form(soup, form_id):
    if not soup:
        soup = BeautifulSoup(br.response().read(), "html.parser")
    form = soup.find('form', attrs={'id': form_id})
    html = str(form)
    resp = mechanize.make_response(
        html, 
        [("Content-Type", "text/html")],
        br.geturl(),
        200, "OK"
    )
    br.set_response(resp)

def findItem(categoryUrl):
	foundItem = False #found item is false on drop days
	count = 0 #initialize keyword counter to match keywords to item 
	while (foundItem == False): #it will keep looking for the link while it hasnt found the item 
		br.open(categoryUrl) #opens us category url 
		print "-----refresh-----"
		for link in br.links(): #gets all links in category url and cycles throuhg them 
			#print "Looking for item"
			nameArray = link.text.lower().split() #gets text of the 'a' tag, puts to lower case and splits into an array 
			for key in keywords: # for loop throuhg keywords
				for name in nameArray: #for loop through name array 
					if key == name: #if a keywword equals part of the name 
						count += 1 #add 1 to count
						#print "Keyword match " + str(count) + "/2"
						if count > 1: #if there are two matching key words
							itemAddress = link.url #set item address to the url of that 'a' tag
							itemValues = itemAddress.split('/') #then split that
							for itemValue in itemValues: #for loop through it for the right color
								if itemValue == color: #if one of the link values is the right color
									finalItemAddress = itemAddress #set the final item address to that time
									foundItem = True #once item is found it breaks from for loop and sets foundItem to be true then moves on 
									print "Item found"
									return finalItemAddress
									break

def getSize(itemUrl):
	br.open(itemUrl) #open that item url 
	soup = BeautifulSoup(br.response().read(), "html.parser") #this segment of code gets the correct size 
	options = soup.findAll('option')
	for option in options: 
		sizeName = option.getText()
		sizeVal = option['value']
		sizeArray = [sizeName, sizeVal] 
		print sizeArray
		if sizeArray[0].lower() == size: 
			tempSizeVal = sizeArray[1]
			break 
	finalSizeVal = tempSizeVal
	print finalSizeVal 
	return finalSizeVal

def atc(finalSizeVal):
	#this segment submits the atc 
	br.select_form(nr=0)
	br.form.set_all_readonly(False) 
	form = br.form 
	if finalSizeVal == None:
		atc = br.submit()
	else:
		form['size'] = [finalSizeVal]
		atc = br.submit()
	print "\n"
	for link in br.links(): 
		ckout = link.text.lower()
		if ckout == "checkout now":
			print "Successfully Added to cart"
	print "\n"

def cartCheck(checkoutUrl): 
	br.open(checkoutUrl) #opens the checkout url and prints the item price 
	soup = BeautifulSoup(br.response().read(), "html.parser")
	ss = soup.findAll('strong')
	for s in ss:
		if not s: 
			print "Item is not in cart, you might have gotten cart jacked"
		else: 
			print s.string
	print "\n"

def checkOut(REALNAME, email, tel, street, zipcode, city, state, cType, cNumberTest, cNumberReal, cMonth, cYear, cvv):
	soupify_form(soup=None,form_id="checkout_form") #takes the gzipped form and makes it mechanizable 
	br.select_form(nr=0)
	br.form.set_all_readonly(False)
	form = br.form
	formName = [f for f in br.forms()] #fills out form 
	form[formName[0].controls[2].name] = REALNAME
	form[formName[0].controls[3].name] = email 
	form[formName[0].controls[4].name] = tel 
	form[formName[0].controls[5].name] = street
	form[formName[0].controls[7].name] = zipcode
	form[formName[0].controls[8].name] = city 
	form[formName[0].controls[9].name] = [state]
	form[formName[0].controls[14].name] = [cType]
	form[formName[0].controls[15].name] = cNumberTest #<-- test number for testing cNumberReal is real number 
	form[formName[0].controls[16].name] = [cMonth]
	form[formName[0].controls[17].name] = [cYear]
	form[formName[0].controls[18].name] = cvv
	br.form.find_control(id=formName[0].controls[20].id).__setattr__("value", ['1'])
	purchase = br.submit() 
	print "checkout done"

def checkSuccess():
	soup = BeautifulSoup(br.response().read(), "html.parser") #checks if purchase was successful or not 
	ii = soup.find('p')
	for i in ii:
		print i.string

############################################CODE STARTS HERE###############################################################################################


keywords = "".split()
size = "1"
category = "hats"
color = ""

start_time = time.time()

#ITEM FIND AND ATC BLOCK 
categoryUrl = url + category
finalItemAddress = findItem(categoryUrl); 
itemUrl = hostUrl + finalItemAddress #append that final search address to host url 
print itemUrl + " <--- Item URL "
finalSizeVal = getSize(itemUrl)
atc(finalSizeVal) 

# CHECKOUT BLOCK 
cartCheck(checkoutUrl)
time.sleep(3)
checkOut(REALNAME, email, tel, street, zipcode, city, state, cType, cNumberTest, cNumberReal, cMonth, cYear, cvv)
checkSuccess()

print("--- %s seconds ---" % (time.time() - start_time))














