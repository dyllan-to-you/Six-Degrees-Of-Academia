This application is composed of three parts: The Database, The Graph Generator, and The Renderer. 

This was my first program in Python. Can you tell? 

The Database
============
You can find an image outlining the database schema in `/data/Database Diagram.PNG`.
You can also find the original data used to populate the databse in the same `/data/` folder.


The Graph Generator
===================
The Relevant Python Scripts are found in the Scripts Folder. 
There are three files
  Main.py
    This is the main file that references the others
    it encapsulates the main function of the program
    From here, the Graph is generated and Colorized
    Then Exporter is referenced to export graphs of varying sizes. You can also set filetype with the parameters in Main
      The Application uses Sigma Graphs. 
  Exporter.py
    Handles File Exporting. 
    Note that the graph is passed in. 
    Also Note that networkx defines its own IDs, which do not work well with SigmaJS. It also names the 'edges' key 'links'. 
      This is accounted for in the Exporter, so I'd personally advise not touching it. 
  GraphBuilder.py
    This is the fun one

    buildGraph(boolean b) Generates the Graph. 
      if the boolean value is set to True, all SQL calls have LIMIT 0,30 appended
        (was used to generate test files)
      Not my cleanest bit of code, but hopefully you can puzzle it out if you want to make changes. It is reasonably well commentated

    getTop(integer i, Graph g) Generates a graph of the top i nodes
      It essentially takes a dict of the nodes, and creates a sorted dict node list thing, sorted by the number of neighbors
      It then grabs the top i nodes from the sorted dict node list thing and generates a new graph using these nodes
      It then goes through the old graph and grabs all the edges that use the top i nodes and imports them into the new graph

    clusterGraph(Graph g) Generates a graph colorized by the cluster
      uses networkx to dicover the communities
      Colorizes communities based on a minimum size defined in the config
      randomly generates colors on a palatte that provides maxiumum discernability

  config.py
    Config File for SQL Database and Community size

The Renderer
=============
  Uses Sigma JS to render the graph by importing the JSON outputted by the Graph Generator
  uses Bootstrap for basic UI


Setup Instructions
==================
Import SQL database. This is found in /data/six_degrees.sql
You can use the provided JSON files, or you can generate new ones. New generation causes new colors for the communities. 
To generate new JSON files, run /scripts/Main.py
Copy the newly generated JSON files into /www/
That's all folks
