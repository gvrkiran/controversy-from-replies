# script to get the username from the tweetids

import sys,glob,os;

filename = sys.argv[1];

for infile in glob.glob(filename + "/*.html"):
#	if(len(infile.split("_"))!=2):
#		continue;
	command = 'grep "<meta content=\\"https://twitter.com/" ' + infile + ' > 1';
	os.system(command);
	f = open("1");
	line = f.readlines();
	if(len(line)!=0):
		line = line[0].strip();
		print line.split("/status")[0].split(".com/")[-1] + "\t" + infile.split("/")[-1].split("_")[-1].replace(".html","");
	f.close();
#	break;
