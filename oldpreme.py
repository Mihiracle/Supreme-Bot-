import mechanize 
import BeautifulSoup
from bs4 import BeautifulSoup
from selenium import webdriver
import regex
import time

#fully functional chekcout and buy normal bot, doesnt work for drops yet, and is not robust 


REALNAME = "Mihir Venkatesh"
email = "mihirv1@gmail.com"
tel = "2065356661" 
zipcode = "98133"
street = "314 N 158th Pl"
city = "Shoreline"
state = "WA"
cType = "visa"
cNumberTest = "1234123412341234"
cNumberReal = "4701320309169239"
cMonth = "01"
cYear = "2019"
cvv = "955" 


url = "http://www.supremenewyork.com/shop/all/"
checkoutUrl = "https://www.supremenewyork.com/checkout"
cartUrl = "http://www.supremenewyork.com/shop/cart"
hostUrl = "http://www.supremenewyork.com"

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



def userInput():
	prompt = '> '
	print "Enter item name:  "
	keyword = raw_input(prompt)
	print "Enter item size: "
	size = raw_input(prompt)
	print "Enter item color: "
	color = raw_input(prompt)
	print "Enter item category (tops_sweaters), all are plural except skate: "
	category = raw_input(prompt)
	ui = [keyword, size, category, color]
	return ui; 

start_time = time.time()

#ui = userInput(); 
keywords = "tagless tees".split() #ui[0].lower().split()
size = "large"#ui[1]
category = "accessories" #ui[2]
color = "black"#ui[3]

categoryUrl = url + category


# Initialize mechanize headless browser
br = mechanize.Browser(factory=mechanize.RobustFactory())
br.set_handle_robots(False)
br.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'), 
				 ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
]


# Let's get mechanize to the web address 
br.open(categoryUrl)

count = 0

for link in br.links(): 
	nameArray = link.text.lower().split()
	for key in keywords: 
		for name in nameArray: 
			if key == name: 
				count += 1
				if count > 1: 
					itemAddress = link.url
					itemValues = itemAddress.split('/')
					for itemValue in itemValues:
						if itemValue == color: 
							finalItemAddress = itemAddress
							break

itemUrl = hostUrl + finalItemAddress

print "\n"
print itemUrl
print "\n"




br.open(itemUrl)
soup = BeautifulSoup(br.response().read(), "html.parser")




options = soup.findAll('option')
for option in options: 
	print option
	sizeName = option.getText()
	sizeVal = option['value']
	sizeArray = [sizeName, sizeVal] 
	if sizeArray[0].lower() == size: 
		tempSizeVal = sizeArray[1]
		break 

finalSizeVal = tempSizeVal

print finalSizeVal

	


br.select_form(nr=0)
br.form.set_all_readonly(False) 
form = br.form 
form['size'] = [finalSizeVal]
print br.form
print "\n"
atc = br.submit() 




br.open(cartUrl) 
soup = BeautifulSoup(br.response().read(), "html.parser")
tr = soup.findAll('td')
for t in tr:
	print t
	break 

print "\n"

br.open(checkoutUrl)
soup = BeautifulSoup(br.response().read(), "html.parser")
strong = soup.findAll('strong')
for s in strong:
	print s

print "\n"

soupify_form(soup=None,form_id="checkout_form")
br.select_form(nr=0)
print br.form
print "\n"
br.form.set_all_readonly(False)
form = br.form
formName = [f for f in br.forms()]

#form['order[billing_name]'] = REALNAME
#form['order[email]'] = email 
#form['order[tel]'] = tel 
#form['order[billing_address]'] = street
#form['order[billing_zip]'] = zipcode
#form['order[billing_city]'] = city 
#form['order[billing_state]'] = [state]
#form['credit_card[type]'] = [cType]
#form['credit_card[cnb]'] = cNumberTest #<-- fake number for testing cNumberReal is real number 
#form['credit_card[month]'] = [cMonth]
#form['credit_card[year]'] = [cYear]
#form['credit_card[vval]'] = cvv
#br.form.find_control(id='order_terms').__setattr__("value", ['1'])

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

print form 
print "good shit"
purchase = br.submit() 
print("--- %s seconds ---" % (time.time() - start_time))










