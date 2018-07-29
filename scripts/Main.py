import GraphBuilder as GB
import Exporter
import operator

# Build the Graph
G = GB.buildGraph(False) # If Set to True, generates a partial graph (by making SQL calls have LIMIT 0,30)
# Colorize the Graph based on Clusters
GC = GB.clusterGraph(G)

# TODO: Add CLI stuff for custom generation of Graphs?

# Export Parameters. Do not touch
# Sigma is what the application uses. GEXF and D3 are not supported, so don't waste your time generating them. 
# The Options are left in case someone needs them
D3 = False
Sigma = True
GEXF = False

Exporter.export(GC, D3, Sigma, GEXF, "0Graph")
Exporter.export(GB.getTop(GC,500), D3, Sigma, GEXF, "500Graph")
Exporter.export(GB.getTop(GC,1000), D3, Sigma, GEXF,"1000Graph")
Exporter.export(GB.getTop(GC,1500), D3, Sigma, GEXF,"1500Graph")
Exporter.export(GB.getTop(GC,2000), D3, Sigma, GEXF,"2000Graph")
Exporter.export(GB.getTop(GC,2500), D3, Sigma, GEXF,"2500Graph")
Exporter.export(GB.getTop(GC,3000), D3, Sigma, GEXF,"3000Graph")
Exporter.export(GB.getTop(GC,3500), D3, Sigma, GEXF,"3500Graph")
Exporter.export(GB.getTop(GC,4000), D3, Sigma, GEXF,"4000Graph")
Exporter.export(GB.getTop(GC,4500), D3, Sigma, GEXF,"4500Graph")
