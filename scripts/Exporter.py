import json
from networkx.readwrite import json_graph

def export(G, D3, Sigma, GEXF, name='Graph'):  
  if D3 == True:
    print("Starting D3 Export for", name)
    # D3
    # Print JSON
    f = open(name + 'D3.json', 'w')
    f.write(json_graph.dumps(G))
    print("D3 Exported")

  if Sigma == True:
    print("Starting Sigma Export for", name)
    # Sigma      
    graphThing = json.loads(json_graph.dumps(G))
    for link in graphThing["links"]:
      link["source"] = link["sources"]
      del link["sources"]
      link["target"] = link["targets"]
      del link["targets"]
    graphThing["edges"] = graphThing["links"]
    del graphThing["links"] 
    # Print JSON
    f = open(name + 'Sigma.json', 'w')
    f.write(json.dumps(graphThing,indent=2))
    print("Exporting for Sigma")

  if GEXF == True:
    print("Starting GEXF export for", name)
    # Print GEXF
    nx.write_gexf(G, name + ".gexf", prettyprint=True)
    print("Exporting GEXF")

  if not D3 and not Sigma and not GEXF:
    print("Not doin' nuthin'")