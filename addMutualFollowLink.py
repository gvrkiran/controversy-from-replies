# script to join the friendships data with the user reply data

import sys,glob,json;

filename = sys.argv[1];

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
#		line_split = line.split("\t");
#		dict_follow[line_split[0] + "," + line_split[1]] = line_split[2] + "," + line_split[3];

for infile in glob.glob("graphs/" + filename + "/*_users_replies_graph.csv"):
	out = open(infile.replace("graphs","graphs1"), "w");
	f = open(infile);
	lines = f.readlines();
	for line in lines:
		line = line.strip();
		line_split = line.split(",");
		if(not dict_follow.has_key(line_split[0] + "," + line_split[1])):
			print >> sys.stderr, "sssssss";
			continue;
		out.write(line + "," + dict_follow[line_split[0] + "," + line_split[1]] + "\n");
	out.close();
