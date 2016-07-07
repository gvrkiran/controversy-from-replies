from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys,time;

#f = open("musicians_tweets_userid_tweetid_part.txt");
count = 1;
dict_explored = {};

def scrapeData(tweetid):
	current_tweetid = tweetid.split("_")[-1];
	if(dict_explored.has_key(current_tweetid)):
		return;
	if(tweetid.find("_")==-1):
		num_scrolls = 30;
	else:
		num_scrolls = 10;
	dict_explored[current_tweetid] = 1;
#	out = open("trump_replies/" + tweetid + ".html","w");
	out = open("US_politicians_replies/" + tweetid + ".html","w");
	url_to_get = "https://twitter.com/asda/status/" + current_tweetid + "?replies_view=true";
	driver.get(url_to_get)

	page_title = driver.title;
	if(page_title.find("/ ?")!=-1 or page_title.find("Account Suspended")!=-1): # tweet missing
		return;

	html_data = driver.page_source.encode('utf-8');
	flag = 0;
	for i in range(1,num_scrolls): # scroll down upto 60 times
#		handle = driver.current_window_handle;
		bg = driver.find_element_by_class_name('js-original-tweet');
#		bg.click();
		bg.send_keys(Keys.SPACE)
#		bg.send_keys(Keys.PAGE_DOWN)
#		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(1);
#		reached_bottom = driver.execute_script("return $(document).height() == ($(window).height() + $(window).scrollTop());");
		print >> sys.stderr, "scrolled " + str(i) + " times";
		html_data = driver.page_source.encode('utf-8');
	links = driver.find_elements_by_class_name('show-more-link');
	for link in links:
		print >> sys.stderr, "show more links", link.get_attribute("href");
		link.click();
		time.sleep(2);
	links1 = driver.find_elements_by_class_name('view-other-link');
	out.write(html_data);
	out.close();
	child_pages = {};
	for link in links1:
		link_to_click = link.get_attribute("href");
		new_tweetid = link_to_click.split("status/")[-1].split("?replies")[0];
		child_pages[link_to_click] = new_tweetid;

	for link in child_pages.keys():
		print >> sys.stderr, "Child links", link;
		scrapeData(tweetid + "_" + child_pages[link]);

filename = sys.argv[1];
f = open(filename);
lines = f.readlines();

for line in lines:
	line = line.strip();
	tweetid = line;
	print >> sys.stderr, "processing", tweetid;

	# first log in to twitter
	driver = webdriver.Firefox()
	driver.set_window_size(4080,3800);
	driver.get("https://twitter.com/login")
#	assert "Twitter" in driver.title
#	elem = driver.find_element_by_id("signin-email")
	elem = driver.find_element_by_class_name("js-username-field");
	elem.send_keys("ogk04593@uikd.com")
	elem = driver.find_element_by_class_name("js-password-field")
	elem.send_keys("chiran")
	elem.send_keys(Keys.ENTER)
	#driver.wait(10)
	time.sleep(1);

	#tweetid = "719830679765270528";
	scrapeData(tweetid);
	driver.close()

"""
#for line in lines:
for n in range(1,2):
	url_to_get = "https://twitter.com/asda/status/" + tweetid + "?replies_view=true";
	driver.get(url_to_get)
	page_title = driver.title.encode('utf-8');

	html_data = driver.page_source.encode('utf-8');
	flag = 0;
	for i in range(1,15): # scroll down upto 60 times
		bg = driver.find_element_by_css_selector('body')
		bg.send_keys(Keys.PAGE_DOWN)
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		#driver.implicitly_wait(10)
		time.sleep(1);
		reached_bottom = driver.execute_script("return $(document).height() == ($(window).height() + $(window).scrollTop());");
		print >> sys.stderr, "scrolled " + str(i) + " times";
		html_data = driver.page_source.encode('utf-8');
#		if(html_data.find("back-to-top hidden")==-1):
#			out.write(html_data);
#			print >> sys.stderr, "exited before scrolled" + str(i) + "times before getting out";
#			break;

#		if(reached_bottom):
#			html_data = driver.page_source.encode('utf-8');
#			flag = 1;
#			out.write(html_data);
#			print >> sys.stderr, "exited before scrolled" + str(i) + "times before getting out";
#			break;
#	if(flag==0):
	links = driver.find_elements_by_class_name('show-more-link');
	for link in links:
		print link.get_attribute("href");
		link.click();
	count += 1;
	links1 = driver.find_elements_by_class_name('view-other-link');
	out.write(html_data);
	child_pages = {};
	for link in links1:
		link_to_click = link.get_attribute("href");
		new_tweetid = link_to_click.split("status/")[-1].split("?replies")[0];
		child_pages[link_to_click] = new_tweetid;

	for link in child_pages.keys():
		print link;
		out1 = open("tmp/" + tweetid + "_" + child_pages[link] + "_tweets.txt","w");
		driver.get(link)
		html_data1 = driver.page_source.encode('utf-8');
		out1.write(html_data1);
		out1.close();
	out.close();
#	if(count>2):
#		break;
"""
