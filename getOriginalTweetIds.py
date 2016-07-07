import sys,re,os,glob;

filename = sys.argv[1];

f = open("US_politicians_tweetid_username.txt");
lines = f.readlines();
dict_username = {};

for line in lines:
	line = line.strip().lower();
	line_split = line.split("\t");
	dict_username[line_split[1]] = line_split[0];

for infile in glob.glob(filename + "_replies/*.html"):
	if(infile.split("/")[-1].find("_")==-1):
		tweetid = infile.split("/")[-1].replace(".html","");
		command = "grep '<link href=\"https://twitter.com/' " + infile + " | grep " + tweetid + " > 1";
		os.system(command);
		f = open("1");
		line = f.read().strip();
		username = line.split(".com/")[-1].split("/status")[0];
#		directory = dict_username[tweetid] + "_replies";
#		if not os.path.exists(directory):
#			os.makedirs(directory);
		if(username!=""):
			try:
				print "python reConstructReplyTreeTopic.py " + dict_username[tweetid] + " " + tweetid + " " + username;
			except:
				print >> sys.stderr, "aa";
