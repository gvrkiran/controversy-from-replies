import glob,sys,os;

f = open("y");
lines = f.readlines();

for line in lines:
	line = line.strip();
	print >> sys.stderr, line;
	for infile in glob.glob("US_politicians_replies/*"):
		f1 = open(infile);
		line1 = f1.read().strip();
		if(line1.find(line)!=-1):
#			print line + "\t" + line1;
			command = "grep " + line + " " + infile + " > 1";
#			print command;
			os.system(command);
			f2 = open("1");
			line2 = f2.read().strip();
			print line + "\t" + line2.split("/status/")[0].split("=&quot;/")[-1].split("=\"/")[-1].lower();
			break;
#	break;

