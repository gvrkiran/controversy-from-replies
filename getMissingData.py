# script to get the data present in graphs/*/*_users_replies_graph.csv and not in graphs1/*/*_users*

import sys,glob,json;

f = open("mutual_following_data_all_US_politicians.txt");
lines = f.readlines();
dict_follow = {};

for line in lines:
	line = line.strip();
	try:
#	for i in range(1,2):
		line = line.replace("'","\"");
		line = line.replace("u\"","\"");
		line = line.replace("None","\"None\"");
		line = line.replace("False,","\"False\",");
		line = line.replace("True,","\"True\",");
		json_data = json.loads(line);
		source = json_data["relationship"]["source"]["screen_name"].lower();
		target = json_data["relationship"]["target"]["screen_name"].lower();
		followed_by = json_data["relationship"]["source"]["followed_by"]; # source followed by target
		following = json_data["relationship"]["source"]["following"]; # source following the target
		dict_follow[source + "," + target] = followed_by + "," + following;
	except:
		print >> sys.stderr, "fu";
		pass;
#
for infile in glob.glob("graphs/*/*_users_replies_graph.csv"):
	filename1 = infile.replace("graphs","graphs1");
	filename2 = infile.replace("graphs","graphs2");
	out = open(filename2, "w");
	f1 = open(filename1);
	lines1 = f1.readlines();
	dict1 = {};
	
	for line in lines1:
		line = line.strip();
		line_split = line.split(",");
		dict1[line_split[0] + "," + line_split[1]] = line;
	
	f2 = open(infile);
	lines2 = f2.readlines();

	for line in lines2:
		line = line.strip();
		line_split = line.split(",");
		if(not dict1.has_key(line_split[0] + "," + line_split[1])):
			if(dict_follow.has_key(line_split[1] + "," + line_split[0])):
				tmp_str = dict_follow[line_split[1] + "," + line_split[0]].split(",");
				out.write(line_split[0] + "," + line_split[1] + "," + line_split[2] + "," + tmp_str[1] + "," + tmp_str[0] + "\n");
			else:
				out.write(line_split[0] + "," + line_split[1] + "," + line_split[2] + ",False,False\n");
#			out.write(line_split[0] + "," + line_split[1] + "\n");# + "," + line_split[2] + ",False,False\n");
		else:
			out.write(dict1[line_split[0] + "," + line_split[1]] + "\n");
	out.close();

