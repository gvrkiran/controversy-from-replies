import glob;

dict_tweetids = {};
for infile in glob.glob("tweet_text/*.html"):
	f = open(infile);
	lines = f.readlines();
	for line in lines:
		line = line.strip();
		line_split = line.split("\t");
		dict_tweetids[line_split[0]] = 1;

for infile in glob.glob("graphs/*/*_replies_graph.csv"):
	if(infile.find("users")!=-1):
		continue;
	f = open(infile);
	lines = f.readlines();
	for line in lines:
		line = line.strip();
		line_split = line.split(",");
		if(not dict_tweetids.has_key(line_split[0])):
			print line_split[0];
		if(not dict_tweetids.has_key(line_split[1])):
			print line_split[1];

