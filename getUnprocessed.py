# script to get unprocessed files

import sys,glob,os;

f = open("back_tweetids.txt");
lines = f.readlines();
dict_tweetids = {};

for line in lines:
	line = line.strip();
	dict_tweetids[line] = 1;

dict_processed = {};
for infile in glob.glob("US_politicians_replies/*"):
	if(len(infile.split("_"))==3):
		filename = infile.split("/")[-1].replace(".html","");
		dict_processed[filename] = 1;

for infile in glob.glob("x*"):
	out = open("tmp/" + infile,"w");
	f1 = open(infile);
	lines1 = f1.readlines();
	for line in lines1:
		line = line.strip();
		if(not dict_processed.has_key(line)):
			out.write(line + "\n");
	out.close();
	command = "cp tmp/" + infile + " " + infile;
	print command;
