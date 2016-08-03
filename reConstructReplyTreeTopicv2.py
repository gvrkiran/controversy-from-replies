#!/usr/bin/env python
# script to process the scraped reply html and reconstruct the reply tree for an entire topic, instead of just a single hashtag

import sys,glob,pprint,re,random;
from collections import defaultdict;
from copy import deepcopy;
import networkx as nx
import matplotlib.pyplot as plt

def createGraph(all_files):
	G = nx.DiGraph();
	G1 = nx.DiGraph();
	root = all_files[1][0][0];
	G.add_node(root);
	for val in range(2,total_depth+1):
		nodes = all_files[val];
		for node in nodes:
			node = node[-2:];
			G.add_node(node[0]);
			G1.add_node(node[0]);
			G.add_node(node[1]);
			G1.add_node(node[1]);
			if(node[1]!=root):
#			if(node[0]!=root):
				G.add_edge(node[0],node[1]);

	# to arbitrarily break inconsistencies
	for node in G.nodes():
		if(len(G.predecessors(node))>0):
#			print "node", node, "predecessors", G.predecessors(node)[random.randint(0,len(G.predecessors(node))-1)];
			random_node = G.predecessors(node)[random.randint(0,len(G.predecessors(node))-1)];
			if(random_node!=root):
				G1.add_edge(node,random_node);
#	return G1;
	return G;
	
def visualizeGraph(G1,tweetid):
	pos=nx.graphviz_layout(G1,prog='dot')
	nx.draw(G1,pos,with_labels=False,arrows=False)
	plt.savefig('plots/' + tweetid + '.png')
#		for node in nodes:

def visualizeUserGraph(G):
	nx.draw(G, pos=nx.spring_layout(G), node_size=30, with_labels=False, arrows=False);
	plt.savefig('plots/' + tweetid + '_user.png');

def visualizeGraph1(G,tweetid):
	pos=nx.graphviz_layout(G,prog="twopi",root=0);
	# draw nodes, coloring by rtt ping time
	nx.draw(G,pos,
		with_labels=False,
		arrows=False,
		alpha=0.5,
		node_size=15);
	plt.savefig('plots/' + tweetid + '.png')

def saveGraph(G,topic_name,tweetid):
	filename = "graphs/" + topic_name + "/" + tweetid + "_replies_graph.csv";
	nx.write_weighted_edgelist(G,filename,delimiter=",");

def saveUserGraph(G,topic_name,tweetid):
	filename = "graphs/" + topic_name + "/" + tweetid + "_users_replies_graph.csv";
	nx.write_weighted_edgelist(G,filename,delimiter=",");

def saveTimestamps(dict_timestamp,topic_name,tweetid):
	out = open("graphs/" + topic_name + "/" + tweetid + "_timestamp.csv","w");
	for keys in dict_timestamp.keys():
		out.write(keys + "," + str(dict_timestamp[keys]) + "\n");
	out.close();

mention_re = re.compile("data-mentions=\"[\w ]+\"");
tweetid_re = re.compile("data-tweet-id=\"\d+\"");
screenname_re = re.compile("data-screen-name=\"\w+\"");
href_re = re.compile("href=\"[\w/]+\"");
timestamp_re = re.compile("data-time=\"\d+\"");

def processHTML(filename):
	dict_screenname = {};
	dict_timestamp = {};
	f = open(filename);
	lines = f.readlines();
	for line in lines:
		line = line.strip();
		if(line.find("data-component-context=\"replies\"")!=-1):
#			print line;
			try:
				#mentions = re.findall(mention_re,line)[0].replace("\"","").replace("data-mentions=","").lower();
				tweetid = re.findall(tweetid_re,line)[0].replace("\"","").replace("data-tweet-id=","");
				screenname = re.findall(screenname_re,line)[0].replace("\"","").replace("data-screen-name=","").lower();
				dict_screenname[tweetid] = screenname;
#				print mentions,tweetid,screenname;
			except:
				pass;
		if(line.find("tweet-timestamp")!=-1):
			try:
				tweetid1 = re.findall(href_re,line)[0].replace("\"","").replace("href=","").lower().split("/")[-1];
				timestamp = re.findall(timestamp_re,line)[0].replace("data-time=","").replace("\"","");
				dict_timestamp[tweetid1] = timestamp;
			except:
				pass;

	return dict_screenname, dict_timestamp;

def tree(): return defaultdict(tree)
def dicts(t): return {k: dicts(t[k]) for k in t}

def add(t, path):
	for node in path:
		t = t[node];
	return t;

def get(tree, path):
	path1 = path.strip("_").split("_");
	for node in path1:
		tree = tree[node];
	return dicts(tree);

def add_at_same_level(tree, head, nodes): # add 'nodes' at the level 'head'. For example if the tree is {1}{2}{3} and the head is {1}{2} and nodes is [5,6] the new tree is {1}{2:[5,6]}{3}
	path1 = head.strip("_").split("_")[-1];
#	for node in path1:
	tree1 = get(tree,head);
	for node1 in nodes:
		tree1[node1];
	return tree1;

def createUserGraph(G,dict_screenname):
	G_user = nx.DiGraph();
	tmp = {};
	for edge in G.edges():
		try:
			node1 = dict_screenname[edge[0]];
			node2 = dict_screenname[edge[1]];
			
			
			if(tmp.has_key(node1 + "," + node2)):
				tmp[node1 + "," + node2] += 1;
			else:
				tmp[node1 + "," + node2] = 1;
			
			
		except:
			continue;


	for keys in tmp.keys():
		edge = keys.split(",");
		node1 = edge[0];
		node2 = edge[1];
		try:
			G_user.add_edge(node1,node2);
			G_user[node1][node2]['weight'] = tmp[node1 + "," + node2];
		except:
			print >> sys.stderr, "missed";
			pass;
	return G_user;

# SCRIPT STARTS HERE

topic_name = sys.argv[1];
#topic_name = "test";
folder_name = "US_politicians_replies/";
#folder_name = "html_files/";
tweetid = sys.argv[2]; #"714855025055514624";
screen_name = sys.argv[3];
#screen_name = "test";

# get the order in which we process the files. Go depth first. first the root and then all children till the leaf.

all_files = {};
already_in_tree = {}; # to avoid duplicate addition of reply ids

#for infile in glob.glob("beefban_replies/572625482593644544*"):
#for infile in glob.glob(folder_name + "*"):
for infile in glob.glob(folder_name + tweetid + "*"):
	filename = infile.replace(".html","").split("/")[-1].split("_");
	for file1 in filename:
		already_in_tree[file1] = 1;

	depth = len(filename);
	if(all_files.has_key(depth)):
		tmp = all_files[depth];
		tmp.append(filename);
		all_files[depth] = tmp;
	else:
		tmp = [];
		tmp.append(filename);
		all_files[depth] = tmp;
	
total_depth = len(all_files.keys());

reply_tree = tree();
reply_tree1 = tree();

nodes_1 = all_files[1];

reply_tree[nodes_1[0][0]];

for val in range(2,total_depth+1):
	nodes = all_files[val];
	for node in nodes:
		add(reply_tree,node);
		add(reply_tree1,node);

#pprint.pprint(dicts(reply_tree));

#add(reply_tree1,['573518578739060736','573519233642020864','573521420527013888','3']);
#add(reply_tree1,['573518578739060736','573519233642020864','573521420527013888','4']);

#pprint.pprint(dicts(reply_tree1));
#queue = [];

root = reply_tree.keys()[0];
#queue.append(root); # push the root node
filename = "";
tmp = [];
count = 0;

#print get(reply_tree1,'573518578739060736_573519233642020864_573521420527013888');

G = createGraph(all_files); # create initial graph backbone based on the crawled structure

root = all_files[1][0][0];
filename = root + ".html";
dict_screenname, dict_timestamp = processHTML(folder_name + filename);
count = len(dict_screenname.keys());
for keys in dict_screenname.keys():
	if(not already_in_tree.has_key(keys)): # this tweetid doesnt already exist
#	if(1==1):
		G.add_node(keys);
		G.add_edge(root,keys); # for the root, add replies as children
		already_in_tree[keys] = 1;

#for keys in dict_screenname.keys():
#	print keys + "\t" + dict_screenname[keys];

#sys.exit();

dict_final_screenname_mapping = {tweetid:screen_name};
dict_final_screenname_mapping.update(dict_screenname);

dict_final_timestamp_mapping = {}; # mapping from reply edges to timestamps
dict_final_timestamp_mapping.update(dict_timestamp);

# add other reply ids
for val in range(2,total_depth+1):
	nodes = all_files[val];
	for node in nodes:
#		root = node[-2];
		root = node[-1];
		filename = ("_").join(node) + ".html";
		dict_screenname, dict_timestamp = processHTML(folder_name + filename);
		dict_final_screenname_mapping.update(dict_screenname);
		dict_final_timestamp_mapping.update(dict_timestamp);
		child_tweetids = dict_screenname.keys();
#		print  node, child_tweetids;
		"""
		for i in range(len(child_tweetids)-1):
			child_tweetid = child_tweetids[i];
			child_tweetid1 = child_tweetids[i+1];
			if(i==0):
				if(not already_in_tree.has_key(child_tweetid)):
#				if(1==1):
					G.add_node(child_tweetid);
					G.add_edge(root,child_tweetid);
					already_in_tree[child_tweetid] = 1;
			if(not already_in_tree.has_key(child_tweetid1)):
#			if(1==1):
				G.add_node(child_tweetid1);
				G.add_edge(child_tweetid,child_tweetid1);
				already_in_tree[child_tweetid1] = 1;
		"""
		for i in range(len(child_tweetids)):
			child_tweetid = child_tweetids[i];
			if(not already_in_tree.has_key(child_tweetid)):
				G.add_node(child_tweetid);
				G.add_edge(root,child_tweetid);
				already_in_tree[child_tweetid] = 1;

		print >> sys.stderr, filename, len(dict_screenname.keys());
		count += len(dict_screenname.keys());

#print len(G.nodes()), len(G.edges()), len(dict_final_screenname_mapping.keys());
#visualizeGraph1(G,tweetid);
G_user = createUserGraph(G,dict_final_screenname_mapping);
#visualizeUserGraph(G_user);
saveGraph(G,topic_name,tweetid);
saveUserGraph(G_user,topic_name,tweetid);
saveTimestamps(dict_final_timestamp_mapping,topic_name,tweetid);
