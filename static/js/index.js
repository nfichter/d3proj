var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
	return "<strong>Date:</strong> <span style='color:red'>" + d.day
	    + "</span><br><strong>Shape:</strong> <span style='color:red'>" + d.shape
	    + "</span><br><strong>Duration:</strong> <span style='color:red'>" + d.duration
	    + "</span><br><strong>Summary:</strong> <span style='color:red'>" + d.specs + "</span>";
    })

  var pane = d3.select("svg");
  pane.attr("width",1203);
  pane.attr("height",595);
  pane.append("svg:image").attr("href","../static/usaMap.jpg").attr("width",1203).attr("height",595);

  pane.call(tip);

  var toPx = function convertDegreesToPx(lat,lng,state){
      if (state == "HI"){
          //console.log(state);
          //console.log("lat:");
          var ycor = 548 + (20-lat)*28;//42.0 + (50.0-lat)*/9.8;
          //console.log(ycor);
          //console.log("lng:");
          var xcor = 172 + (155.0-lng)*28;
          //console.log(xcor);
          return [xcor,ycor];
      };
      if (state == "AK"){
          //console.log(state);
          //console.log("lat:");
          var ycor = 398 + (60-lat)*11.4;//42.0 + (50.0-lat)*/9.8;
          //console.log(ycor);
          //console.log("lng:");
          var xcor = 112 + (150-lng)*5;
          //console.log(xcor);
          return [xcor,ycor];
      };
//120 deg-X == 174px
  //70 deg-X  == 561px
  //ratio -50 deg-X to 387px
  // px/deg = 7.74

  //50 deg-Y == 42px
  //25 deg-Y == 287px
  //ratio -25 deg-Y == 245 px
  // px/deg = 9.8

      //console.log(state);
      //console.log("lat:");
      var ycor = 1072 + (0-lat)*19.6;//42.0 + (50.0-lat)*/9.8;
      //console.log(ycor);
      //console.log("lng:");
      var xcor = 348.0 + (120.0-lng)*15.48;
      //console.log(xcor);
      return [xcor,ycor];
  };

  //get line
  var lineFunction = d3.svg.line()
      .x(function(d) { return d.x; })
      .y(function(d) { return d.y; })
      .interpolate("linear");
  //makes line
  var makeLine = function makesLines(coors,color){ //coors list of list pairs of coordinates
      var lData = [];
      for (var i = 0;i<coors.length;i++){
          lData.push([ { "x": coors[i][0] - 20,   "y": coors[i][1]},  { "x": coors[i][0]+20,  "y  ": coors[i][1]}],[{ "x": coors[i][0],   "y": coors[i][1]-20},  { "x": coors[i][0],  "y": coors  [i][1]+20 }]);
      };
      for (var i = 0;i<lData.length;i++){
  pane.append("path")
  .attr("d", lineFunction(lData[i]))
  .attr("stroke", color)
  .attr("stroke-width", 2)
  .attr("fill", "none");
    }
  };

  //circle stuff
  //var reportPoints = {{reports}};
  //console.log(reportPoints);

  var plot = function plotDot(dotInfo){ //dot info is a list of dot info lists  with the format   [<latitude>,<longitude>,<state>,<city>,<report>]
  //circle stuff with modified code from dashingd3
      var pointList = [];
      for (var i = 0;i<dotInfo.length;i++){
          var tempDict = {};
          var tempCoor = toPx(dotInfo[i]["lat"],dotInfo[i]["lng"],dotInfo[i]["state"]);
          tempDict.xcor = tempCoor[0];
          tempDict.ycor = tempCoor[1];
          tempDict.radius = 5;
          tempDict.color = "purple";
          tempDict.state = dotInfo[i]["state"];
          tempDict.city = dotInfo[i]["city"];
          tempDict.specs = dotInfo[i]["specs"];
          tempDict.day = dotInfo[i]["date"];
	  tempDict.shape = dotInfo[i]['shape']
	  tempDict.duration = dotInfo[i]['duration']
          pointList.push(tempDict);
      };
  var points = pane.selectAll("circle")
      .data(pointList)
      .enter()
      .append("circle");
  var circleAttributes = points
      .attr("cx", function (d) { return d.xcor; })
      .attr("cy", function (d) { return d.ycor; })
      .attr("r", function (d) { return d.radius; })
      .style("fill", function(d) { return d.color; })
      .on('mouseover', tip.show)
      .on('mouseout', tip.hide);
  };
//clear dots
//points.remove();


  //plot(reportPoints);

////////TEST CASE FUNCTIONS //////////////////////////

  //test coors AK
  var testAK = function test_Alaska(){
  var coors = [toPx(60,150,"AK")];
  coors.push(toPx(70,165,"AK"));
  makeLine(coors,"red");
  };

  //test coors HI
  var testHI = function test_Hawaii(){
  var coors = [toPx(20,155,"HI")];
  coors.push(toPx(22,160,"HI"));
  makeLine(coors,"green");
  };

  //test Coors NY is arbitrary state that is not HI or AK
  var testMain = function test_regular_states(){
  var coors = [toPx(50,120,"NY")];
  coors.push(toPx(45,110,"NY"));
  coors.push(toPx(40,100,"NY"));
  coors.push(toPx(35,90,"NY"));
  coors.push(toPx(30,80,"NY"));
  coors.push(toPx(25,70,"NY"));
  makeLine(coors,"blue");
  };
  //Test Grid
  //testAK();
  //testHI();
  //testMain();
