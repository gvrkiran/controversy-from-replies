# script to get the tweet text from the raw html dumps

from bs4 import BeautifulSoup;
import sys,re,glob;

filename = sys.argv[1];

for infile in glob.glob("US_politicians_replies/" + filename + "*"):
#f = open("US_politicians_replies/726035099125346305.html");
	f = open(infile);
	if(len(infile.split("/")[-1].split("_"))==1):
		out = open("tweet_text/" + infile.split("/")[-1],"w");
	lines = f.readlines();

	flag_id = 0;
	flag_text = 0;
	tmp_id = "";
	tmp_text = "";
	visited_id = 0;

	for line in lines:
		line = line.strip();
		if(line.find("stream-item-header")!=-1 and line.find("div")!=-1):
			flag_id = 1;
		if(flag_id==1 and line.find("/div")==-1):
			tmp_id += line;
		if(flag_id==1 and line.find("/div")!=-1):
			tmp_id = tmp_id + line;
	#		print tmp_id;
			soup1 = BeautifulSoup(tmp_id);
			texts = soup1.find_all("a",class_="tweet-timestamp");
			tweetids = re.findall(r"\D(\d{18})\D", tmp_id);
			tmp_id = "";
			flag_id = 0;
			visited_id = 1;
	
		if(line.find("js-tweet-text-container")!=-1 and line.find("div")!=-1):
			flag_text = 1;
		if(flag_text==1 and line.find("/div")==-1):
			tmp_text += line;
		if(flag_text==1 and line.find("/div")!=-1):
			tmp_text = tmp_text + line;
	#		print tmp_text;
			soup2 = BeautifulSoup(tmp_text);
	#		texts = soup2.find_all("p");
			texts = soup2.get_text();
			if(visited_id==1):
				out.write(str(tweetids[-1]) + "\t" + texts.encode('utf-8') + "\n");
			tmp_text2 = "";
			tmp_text = "";
			flag_text = 0;
			visited_id = 0;

out.close();
