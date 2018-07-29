<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>FAU Degrees Of Separation</title>

    <!-- Bootstrap -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <style type="text/css">
      html{
        min-height: 100%;/* make sure it is at least as tall as the viewport */
        position: relative
      }
      body{
        height: 100%; /* force the BODY element to match the height of the HTML element */
      }

      .container{
        margin-top: 150px;
      }

      .row{
        min-height: 100%;
      }
      #graph {
        position: fixed;
        top: 0;
        bottom: 0;
        overflow: hidden;
      }
      #panel {
        height: 1200px;
        overflow: auto;
      }
    </style>  

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <?php $rangeValues = [0,500,1000,1500,2000,2500,3000,3500,4000, 4500] ?>
    <?php if(!isset($_GET['range']) || !in_array($_GET['range'], $rangeValues)): ?>
      <div class="container">
          <form role="form" name="input" action="index.php" method="get">
            <div class="form-group" >
              <p>How many nodes would you like to view? (Put 0 if you want to view the entire graph.)</p>
              <select name="range">
                <option value="0">0</option>
                <option value="500">500</option>
                <option value="1000">1000</option>
                <option value="1500">1500</option>
                <option value="2000">2000</option>
                <option value="2500">2500</option>
                <option value="3000">3000</option>
                <option value="3500">3500</option>
                <option value="4000">4000</option>
                <option value="4500">4500</option>
              </select>
            </div>
            <div class="form-group">
              <button class="btn btn-lg btn-primary" type="submit">Submit</button>
            </div>
          </form>
      </div>
    <?php else: ?>
    <div class="row">
      <div id="graph" class="col-md-9"></div>
      <div id="panel" class="col-md-3 pull-right">
        <div class="well">
          <div class="form-group">
            <label class="col-md-6 control-label">Force Atlas 2</label>
            <button class="btn btn-lg btn-primary" data-bind="click: forceAtlasButton" ><span data-bind="text: forceAtlasState"></span></button>
          </div>
          <div data-bind="visible: currentProfessor" class="panel panel-primary">
            <div class="panel-heading">
              <h1><span data-bind="text: currentProfessor"></span></h1>
            </div>
            <ul class="nav nav-tabs">
              <li class="disabled"><a href="" data-toggle="tab">Neighbors</a></li>
              <li class="active"><a href="#publications" data-toggle="tab">Publications</a></li>
              <li class="disabled"><a href="" data-toggle="tab">References</a></li>
            </ul>

            <!-- Tab panes -->
            <div class="tab-content">
              <div class="tab-pane" id="authors" >
                <ul data-bind="foreach: professorNeighbors" class="list-unstyled">
                  <li>
                    <span data-bind="">Not Actually working...</span>
                  </li>
                </ul>
              </div>
              <div class="tab-pane active" id="publications">
                <ul data-bind="foreach: professorEdges" class="list-unstyled">
                  <li>
                    Publication EID: <span data-bind="text: $data"></span>
                  </li>
                </ul>
              </div>
              <div class="tab-pane" id="references">...</div>
            </div>
          </div>

        </div>
      </div>
    </div>
    <script src="lib/sigma-v1.0.2/sigma.min.js"></script>
    <script src="lib/sigma-v1.0.2/plugins/sigma.parsers.json.min.js"></script>
    <script src="lib/sigma-v1.0.2/plugins/sigma.layout.forceAtlas2.min.js"></script>
    <script>

      // Add a method to the graph model that returns an
      // object with every neighbors of a node inside:
      sigma.classes.graph.addMethod('neighbors', function(nodeId) {
        var k,
            neighbors = {},
            index = this.allNeighborsIndex[nodeId] || {};

        for (k in index)
          neighbors[k] = this.nodesIndex[k];

        return neighbors;
      });

      sigma.parsers.json(
        '<?php echo $_GET['range'] ?>GraphSigma.json', 
        {
          container: 'graph',
          settings: {
            defaultNodeColor: '#666',
            defaultEdgeColor: '#666',
            edgeColor: 'default',
            labelThreshold: 30,
            maxNodeSize: 4
          }
        },
        function(s) {
          // We first need to save the original colors of our
          // nodes and edges, like this:
          s.graph.nodes().forEach(function(n) {
            n.originalColor = n.color;
          });
          s.graph.edges().forEach(function(e) {
            e.originalColor = e.color;
          });

          // When a node is clicked, we check for each node
          // if it is a neighbor of the clicked one. If not,
          // we set its color as grey, and else, it takes its
          // original color.
          // We do the same for the edges, and we only keep
          // edges that have both extremities colored.
          s.bind('clickNode', function(e) {
            var nodeId = e.data.node.id,
                toKeep = s.graph.neighbors(nodeId);
            toKeep[nodeId] = e.data.node;
            var publications = [];

            s.graph.nodes().forEach(function(n) {
              if (toKeep[n.id])
                n.color = n.originalColor;
              else
                n.color = '#ddd';
            });

            s.graph.edges().forEach(function(e) {
              if (toKeep[e.source] && toKeep[e.target])
                {
                  e.color = e.originalColor;
                  eid = e.eid;
                  if (typeof(eid) != "undefined") eid = eid.substring(2,eid.length-2);
                  if (publications.indexOf(eid) == -1) publications.push(eid);
                }
              else
                e.color = '#eee';
            });

            // Side Panel Data
            visibleNode = e.data.node;
            viewModel.currentProfessor(visibleNode.label);
            viewModel.professorNeighbors(toKeep);
            delete viewModel.professorNeighbors()[nodeId]
            viewModel.professorEdges(publications);
            console.log(viewModel.professorNeighbors());
            console.log(viewModel.professorEdges());

            // Since the data has been modified, we need to
            // call the refresh method to make the colors
            // update effective.
            s.refresh();
          });

          // When the stage is clicked, we just color each
          // node and edge with its original color.
          s.bind('clickStage', function(e) {
            s.graph.nodes().forEach(function(n) {
              n.color = n.originalColor;
            });

            s.graph.edges().forEach(function(e) {
              e.color = e.originalColor;
            });

            // Sets Current Professr to Null
            viewModel.currentProfessor("");

            // Same as in the previous event:
            s.refresh();
          });       
        }
      );


    </script>
    <?php endif; ?>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>
    <script type='text/javascript' src='lib/knockout-3.1.0.js'></script>
    <script>
      var viewModel = {
        forceAtlasState : ko.observable("Start"),
        forceAtlasButton : function() {
          if(this.forceAtlasState() == "Start"){
            sigma.instances()[0].startForceAtlas2();
            this.forceAtlasState("Stop");
          } else if (this.forceAtlasState() == "Stop"){
            sigma.instances()[0].stopForceAtlas2();
            this.forceAtlasState("Start");
          }
        },
        currentProfessor : ko.observable(""),
        professorNeighbors : ko.observable(),
        professorEdges : ko.observable()
      };
      ko.applyBindings(viewModel);
    </script>
  </body>
</html>
