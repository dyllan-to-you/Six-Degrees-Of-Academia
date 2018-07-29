import config
import mysql.connector
import networkx as nx
import operator
import random
import colorsys

random.seed()

def buildGraph(LIMIT=False):
  # Connect to the Database
  print("Connecting to DB {} at {} as {}".format(config.DATABASE, config.HOST, config.USER))
  try:
    cnx = mysql.connector.connect(user=config.USER, 
                                password=config.PASS,
                                host=config.HOST,
                                database=config.DATABASE,
                                buffered=True)
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exists")
    else:
      print(err)
  cur1 = cnx.cursor()

  # Initialize the Graph
  print("Graph Initialized")
  G = nx.Graph()

  # Random Coordinate Generator
  counter = 0
  coordinateX = 1
  coordinateY = 1

  # Generates the nodes
  print("Querying Authors\n")
  cur1.execute("SELECT  `author_ScopusID`, `author_ori_name` FROM  `authors` WHERE 1 LIMIT 0 , 30") if LIMIT else cur1.execute("SELECT  `author_ScopusID`, `author_ori_name` FROM  `authors` WHERE 1")
  for(author_ScopusID, author_ori_name) in cur1:
    print("Adding node {} with ID={} and name={}".format(str(author_ScopusID), str(author_ScopusID), str(author_ori_name)))  
    G.add_node(str(author_ScopusID), label = str(author_ori_name), x = coordinateX, y = coordinateY, size = 1)
    print("Coordinate: ", coordinateX, coordinateY)
    # Arranges the nodes in an X. 
    if counter == 0 or counter == 2:
      coordinateX *= -1
    elif counter == 1 or counter == 3:
      coordinateY *= -1
    counter += 1
    if counter == 4:
      coordinateX +=1
      coordinateY +=1
      counter = 0   

  print("~~~~~~~~~~~~~~~")

  # Makes a Dict which will be referenced on edge generation
  edges = {}

  # Makes Edges based on Co-Authorship
  cur1.execute("SELECT `eid` FROM `publications` WHERE 1 LIMIT 0,30") if LIMIT else cur1.execute("SELECT `eid` FROM `publications` WHERE 1") 
  listOfEids = cur1.fetchall()
  for (eid,) in listOfEids:
    print("\nAssociating Authors from publications with eid = {}".format(eid))
    cur1.execute("SELECT `author_ScopusID` FROM `authors_publications` WHERE `eid` = %s",(eid,))
    listOfAuthors = cur1.fetchall()
    for (author,) in listOfAuthors:
      for (connected,) in listOfAuthors:
        if author != connected:
          edgeID = getEdgeID(author,connected) if getEdgeID(connected,author) not in edges else getEdgeID(connected,author)
          # # If an edge already exists between authors, add another reason for that edge. 
          # if edgeID in edges and eid not in edges[edgeID]["eid"]:
          #     print("Adding eid between {} and {}. ID={}, eid={}".format(str(author), str(connected), edgeID, str(eid)))
          #     edges[edgeID]["eid"].append(eid)
          # else:
          # Else just add the edge
          if edgeID not in edges:
            print("Adding edge between {} and {}. id={}, eid={}".format(str(author), str(connected), edgeID, str(eid)))
            edges[edgeID] = {"id":str(edgeID), "sources":str(author), "targets":str(connected), "eid":[str(eid)]}

  # Make Edges based on publication references
  cur1.execute("SELECT `ref_eid` FROM `references` WHERE 1 LIMIT 0,30") if LIMIT else cur1.execute("SELECT `ref_eid` FROM `references` WHERE 1")
  listOfReferences = cur1.fetchall()
  for(ref_eid,) in listOfReferences:
    cur1.execute("SELECT `eid` FROM `publications_references` WHERE `ref_eid` = %s", (ref_eid,))
    listOfPublications = cur1.fetchall()
    listOfAuthors = list()
    print("\nAssociating Authors from publications that have a reference = {}".format(ref_eid))
    for(eid,) in listOfPublications:
      cur1.execute("SELECT `author_ScopusID`, `eid` FROM `authors_publications` WHERE `eid` = %s",(eid,))
      listOfAuthors.extend(cur1.fetchall())
    for (author,pub1) in listOfAuthors:
      for (connected,pub2) in listOfAuthors:
        if author != connected and pub1 != pub2:
          edgeID = getEdgeID(author,connected) if getEdgeID(connected,author) not in edges else getEdgeID(connected,author)
          # # If an edge already exists between authors, add another reason for that edge. 
          # if edgeID in edges and ref_eid not in edges[edgeID]["ref_eid"] and pub1 not in edges[edgeID]["pub_eid"] and pub2 not in edges[edgeID]["pub_eid"]:
          #   print("Adding references between {} and {}. ID={}, ref_eid={}, pub_eid={}&{}".format(str(author), str(connected), edgeID, str(ref_eid), str(pub1), str(pub2)))
          #   edges[edgeID]["ref_eid"].append(ref_eid)
          #   edges[edgeID]["pub_eid"].extend([pub1,pub2])
          # # Else just add the edge
          # else:     
          if edgeID not in edges:
            print("Adding edge between {} and {}. ID={}, ref_eid={}, pub_eid={}&{}".format(str(author), str(connected), edgeID, str(ref_eid), str(pub1), str(pub2)))
            edges[edgeID] = {"id":str(edgeID), "sources":str(author), "targets":str(connected), "ref_eid":[str(ref_eid)], "pub_eid":[str(pub1),str(pub2)]}

  # # Make edges based on an author's publication referencing another publication
  # cur1.execute("SELECT pr.`eid`, pr.`ref_eid` FROM `publications_references` pr INNER JOIN `publications` p ON pr.ref_eid = p.eid")
  # listOfReferences = cur1.fetchall()
  # for(ref_eid,) in listOfReferences:
  #   cur1.execute("SELECT `author_ScopusID` FROM `authors_publications` WHERE `eid` = %s", (ref_eid,))
  #   referenceAuthors = cur1.fetchall()
  #   cur1.execute("SELECT `eid` FROM `publications_references` WHERE `ref_eid` = %s", (ref_eid,))
  #   pubAuthors = cur1.fetchall()
  #   for (eid,) in pubAuthors
  #     cur1.execute("SELECT `eid`, `author_ScopusID` FROM `authors_publications` ")

  # Add Edges
  for edgeK,edgeV in edges.items():
    G.add_edge(str(edgeV.get("sources")), str(edgeV.get("targets")))
    for k,v in edgeV.items():
      G.edge[edgeV.get("sources")][edgeV.get("targets")][k] = str(v)

  # Adds Neighbor Count
  for nodeIndex in G.nodes():
    neighbors = len(G.neighbors(nodeIndex))
    G.node[nodeIndex]["neighborCount"] = neighbors
    print(nodeIndex, "has ", neighbors, "neighbors")

  return G

def getEdgeID(id1, id2):
  return str(id1) + "|" + str(id2)

def getTop(G, x):
  TopGraph = nx.Graph();
  sortedNodeData = sorted(G.nodes(data=True), key=lambda x: x[1].get('neighborCount'), reverse=True)
  TopGraph.add_nodes_from(sortedNodeData[0:x])
  sortedNodes = [item[0] for item in sortedNodeData]
  topSortedNodes = sortedNodes[0:x]
  for u,v,d in G.edges_iter(data=True):
    if u in topSortedNodes and v in topSortedNodes:
      TopGraph.add_edge(u,v,d)
  return TopGraph

def clusterGraph(G):
  print("Clustering and Colorizing Graph")
  c = list(nx.k_clique_communities(G, COMMUNITY_SIZE = 10))
  usedColors = list()
  for cluster in c:
    goldenRatio = 0.618033988749895
    h = random.random()
    color = "0"
    while color in usedColors or color == "0":
      h += goldenRatio
      h %= 1
      rgb = colorsys.hsv_to_rgb(h,0.5,0.95)
      color = "#{0:02x}{1:02x}{2:02x}".format(int(rgb[0]*255),int(rgb[1]*255),int(rgb[2]*255))
    usedColors.append(color)
    for nodeID in cluster:
      print("Giving", nodeID, "Color", color)
      G.node[nodeID]['color'] = color
  print("Used Colors:", usedColors)
  return G
