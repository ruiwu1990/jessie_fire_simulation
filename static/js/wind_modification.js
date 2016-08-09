$(document).ready(function(){
  // TODO this part should be done byusing get request
  // get the color from get request from the server
  var inputJson;

  // set up the canvas size
  var cellWidth = 10;
  var cellHeight = 10;

  // canvas col and row num
  var dataX;
  var dataY;
  // original fire code
  var fireOrigin;
  // current fire code
  var fireCurrent;
  // elevation information for all HRU cells
  var elevationInfo;

  var canvasWidth;
  var canvasHeight;
  var canvasHandle;
  var canvas2DContext;

  // this is for define color for the cells
  var colorScale;

  // define google map with map
  var map;
  // this is for image overlay
  var imgOverlay;
  var imageBounds;
  // url for overlay image
  var imgURL;
  // map center
  var center;

  // this is for mouse dragging
  var isDragging = false;
      //chosenHRU.push(p1.x+p2.y*vegColNum);
  var isMousePressing = false;
  var firstPosition;
  var secondPosition;
  var clickTime;
  // record the chosen area rec top left
  var firstPoint = {x:-1,y:-1};
  // record the chosen area rec bot right
  var secondPoint = {x:-1,y:-1};
  // record mouse click time
  // this var record all the chosen HRU num
  var chosenHRU = [];

  var currentTime = 0;

  var backgroundMap = new Image();
  var canvasSize = [];

  // TODO this part should not be hard coded
  var veg_type_num = [];


  // these for veg type modification
  var vegColorScale = [];
  var veg2DGrid = [];
  var vegJson;

  var vegColNum;
  var vegRowNum;
  var chosenAreaInfo=[];
  var vegCode;
  var vegMetaData;

  var onFireCell = [];

  var windX;
  var windY;
  var colorScaleX;
  var colorScaleY;
  var uniqueX;
  var uniqueY;
  // this is for the line arrow drawing
  var arrow = [
    [ 1, 0 ],
    [ -5, -2],
    [ -5, 2]
  ];

  $.get('/api/wind_data', function(data){

    inputJson = JSON.parse(data);

    // grab col and row num
    dataX = parseInt(inputJson['num_cols']);
    dataY = parseInt(inputJson['num_rows']);

    windX = inputJson["wind_data_x"].slice();
    windY = inputJson["wind_data_y"].slice();

    uniqueX = inputJson["unique_x"].slice();
    uniqueY = inputJson["unique_y"].slice();


    canvasWidth = cellWidth*dataX;
    canvasHeight = cellHeight*dataY;

    canvasSize.push(canvasWidth);
    canvasSize.push(canvasHeight);
   
    $('.mapCanvas').attr('width',canvasWidth.toString()+'px');
    $('.mapCanvas').attr('height',canvasHeight.toString()+'px');

    // place mapArray into canvas
    canvasHandle = document.getElementById("myCanvas");
    canvas2DContext = canvasHandle.getContext("2d");

    // for current version, we only have on fire and not on fire
    var scaleSizeX = uniqueX.length;
    if(scaleSizeX == 1)
    {
      colorScaleX = ['blue'];
    }
    else
    {
      colorScaleX = chroma.scale(['blue','red']).colors(scaleSizeX);
    }

    var scaleSizeY = uniqueY.length;
    if(scaleSizeX == 1)
    {
      colorScaleY = ['blue'];
    }
    else
    {
      colorScaleY = chroma.scale(['blue','red']).colors(scaleSizeY);
    }
    

    //colorScale = ['#00FF00','#FF0000'];

    initCanvas();

  });

  // dynamically create array
  // function is from http://stackoverflow.com/questions/966225/how-can-i-create-a-two-dimensional-array-in-javascript/966938#966938
  function createArray(length) {
    var arr = new Array(length || 0),
        i = length;

    if (arguments.length > 1) {
        var args = Array.prototype.slice.call(arguments, 1);
        while(i--) arr[length-1 - i] = createArray.apply(this, args);
    }

    return arr;
  }

  
  // TODO, cannot use url to get google map image based on the two corners
  function setupBackgroundMap()
  {
    // backgroundMap.onload = function(){
    //   canvas2DContext.globalAlpha = 0.5;
    //   canvas2DContext.drawImage(backgroundMap, 0, 0);
    // }
    
  }

  // this is from http://www.html5canvastutorials.com/advanced/html5-canvas-mouse-coordinates/
  // get the mouse position, based on px
  function getMousePos(canvas, evt)
  {
    var rect = canvas.getBoundingClientRect();
    return {
      x: evt.clientX - rect.left,
      y: evt.clientY - rect.top
    };
  }


  // this function is used to update canvas (fire cell) with the current fire code
  function updateCanvas()
  {
      // var tempIndexX;
      // var tempIndexY;
      // var tempColorX;
      // var tempColorY;

      var tempLocationArr;
      for(var m=0 ; m<dataY ; m++)
      {
        for(var i=0 ; i<dataX ; i++)
        {
          // tempIndexX = uniqueX.indexOf(windX[m][i]);
          // tempColorX = colorScaleX[tempIndexX];
          // tempIndexY = uniqueY.indexOf(windY[m][i]);
          // tempColorY = colorScaleY[tempIndexY];
          // // use the toolkit to merge two color
          // canvas2DContext.fillStyle = $.xcolor.average(tempColorX, tempColorY);;
          // //                          start x,     y,            width,    height
          // canvas2DContext.fillRect(cellWidth*i,cellHeight*m,cellWidth,cellHeight);
          tempLocationArr = getStartEndPositions(windX[m][i],windY[m][i],i,m);
          drawLineArrow(tempLocationArr[0],tempLocationArr[1],tempLocationArr[2],tempLocationArr[3]);
        }
      }
      //canvas2DContext.stroke();
      currentTime = currentTime + 1;

      setupBackgroundMap();
  }
  function initCanvas()
  {
      updateCanvas();
  }

  // componentToHex, rgbToHex, and hexToRgb from http://stackoverflow.com/questions/5623838/rgb-to-hex-and-hex-to-rgb
  function componentToHex(c) {
      var hex = c.toString(16);
      return hex.length == 1 ? "0" + hex : hex;
  }

  function rgbToHex(r, g, b) {
      return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
  }  
  function hexToRgb(hex) {
      var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
      return result ? {
          r: parseInt(result[1], 16),
          g: parseInt(result[2], 16),
          b: parseInt(result[3], 16)
      } : null;
  }
  

  $("#myCanvas")
    .mousedown(function(evt){
      isMousePressing = true;
    })
    .mousemove(function(evt){
      // record the first mouse position
      if(isDragging==false && isMousePressing==true)
      {
        // start point
        clickTime = 1;
        firstPosition = getMousePos(canvasHandle, evt);
        isDragging = true;
        changeCanvasCellColor(firstPosition,"#FFFF00");
      }
      else if(isDragging == true && isMousePressing==true)
      {
        clickTime = 2;
        secondPosition = getMousePos(canvasHandle, evt);
        changeCanvasCellColor(secondPosition,"#FFFF00");
      }
    })
    .mouseup(function(evt){
      isMousePressing = false;
      // choose single cell
      if(isDragging==false)
      {
        clickTime = 1;
        firstPosition = getMousePos(canvasHandle, evt);
        changeCanvasCellColor(firstPosition,"#FF00FF");
        secondPosition = firstPosition;
        clickTime = 2;
        changeCanvasCellColor(secondPosition,"#FF00FF");
      }
      // choose an area
      else if(isDragging==true)
      {
        isDragging = false;
      }
       // push the final chosen area into chosenAreaInfo
      // get the current chosen color number
      var tempWindX = $('#wind_x').val();
      var tempWindY = $('#wind_y').val();
      //parseInt($('input[name="vegcode-select"]:checked').val());
      chosenAreaInfo.push({updateWindX:tempWindX, updateWindY:tempWindY, chosenArea:chosenHRU});
      chosenHRU=[];
  });

  $('#global-wind-modification-label').click(function(){
    alert('1');
  });

  $('#area-wind-modification-label').click(function(){
    alert('2');
  });

  $("#save-wind-update").click(function(){

    $.each(chosenAreaInfo, function(index1, value1) {
      //var tempColor = value1.colorNum;
      $.each(value1.chosenArea,function(index2,value2){
        // value2[0] is x, value2[1] is y
        windX[value2[1]][value2[0]] = parseInt(value1.updateWindX);
        // TODO, change color based on input values
        var tempColor = hexToRgb('#832510');
        var tempColorString = 'rgba('+tempColor.r.toString()+','+tempColor.g.toString()+','+tempColor.b.toString()+',0.5)';

        // canvas2DContext.fillStyle = colorScale[0];
        canvas2DContext.fillStyle = tempColorString;
        //                          start x,     y,            width,    height
        canvas2DContext.fillRect(cellWidth*value2[0],cellHeight*value2[1],cellWidth,cellHeight);

      });
    });

    $.each(chosenAreaInfo, function(index1, value1) {
      //var tempColor = value1.colorNum;
      $.each(value1.chosenArea,function(index2,value2){
        windY[value2[1]][value2[0]] = parseInt(value1.updateWindY);

      });
    });


  // TODO need to merge fire update and veg post
  $("#post-wind-update").click(function(){
    // var wind_x = $('#wind_x').val().toString();
    // var wind_y = $('#wind_y').val().toString();
    // post the update info back to server
    $.ajax({
        type : "POST",
        url : "/api/update_wind",
        data: JSON.stringify(
          {
            wind_x_data: windX,
            wind_y_data: windY
          }, null, '\t'),
        contentType: 'application/json',
        success: function(result) {

          window.location.replace('/fire_vis_modified');

        }
    });

  });


    // TODO send changes back to server

    // update map overlay
    // updateMapOverlay();
  });

  // this is from http://www.html5canvastutorials.com/advanced/html5-canvas-mouse-coordinates/
  // get the mouse position, based on px
  function getMousePos(canvas, evt)
  {
    var rect = canvas.getBoundingClientRect();
    return {
      x: evt.clientX - rect.left,
      y: evt.clientY - rect.top
    };
  }

  function getStartEndPositions(tempWindX,tempWindY,col,row)
  {
    var tempStartX;
    var tempStartY;
    var tempEndX;
    var tempEndY;
    var tanAngle = Math.atan(tempWindY/tempWindX);
    // this is kind of cheated, coz cellWidth == cellHeight
    var tempYLen = cellWidth*Math.tan(tanAngle);
    if(tempWindX>=0 && tempWindY>=0)
    {
      tempStartX = cellWidth*col;
      tempEndX = cellWidth*col+cellWidth;
      tempStartY = cellHeight*row+tempYLen;
      tempEndY = cellHeight*row;
    }
    else if(tempWindX>=0 && tempWindY<0)
    {
      tempStartX = cellWidth*col;
      tempEndX = cellWidth*col+cellWidth;
      tempStartY = cellHeight*row;
      tempEndY = cellHeight*row+tempYLen;
    }
    else if(tempWindX<0 && tempWindY>=0)
    {
      tempStartX = cellWidth*col+cellWidth; 
      tempEndX = cellWidth*col;
      tempStartY = cellHeight*row+tempYLen;
      tempEndY = cellHeight*row;
    }
    else if(tempWindX<0 && tempWindY<0)
    {
      tempStartX = cellWidth*col+cellWidth; 
      tempEndX = cellWidth*col;
      tempStartY = cellHeight*row;
      tempEndY = cellHeight*row+tempYLen;
    }

    return [tempStartX,tempStartY,tempEndX,tempEndY];
  }

  function changeCanvasCellColor(mousePosition,color)
  {
    var startX = Math.floor(mousePosition.x/cellWidth);
    var startY = Math.floor(mousePosition.y/cellHeight);
    canvas2DContext.fillStyle = color;
    canvas2DContext.fillRect(startX*cellWidth, startY*cellHeight, cellWidth, cellHeight);

    if(clickTime == 1)
    {
      firstPoint.x = startX;
      firstPoint.y = startY;
    }
    else if(clickTime == 2)
    {
      secondPoint.x = startX;
      secondPoint.y = startY;

      showChosenRecArea(firstPoint,secondPoint);

    }

  }

  // this function requires top left and bot right points for the chosen area
  function showChosenRecArea(input1,input2)
  {
    var p1 = {x:input1.x,y:input1.y};
    var p2 = {x:input2.x,y:input2.y};
    var temp;
    canvas2DContext.fillStyle = "#FFFF00";
    // not the same point
    if(p2.x!=p1.x&&p2.y!=p1.y)
    {
      if(p2.x < p1.x)
      {
        temp = p2.x;
        p2.x = p1.x;
        p1.x = temp;
      }
      if(p2.y < p1.y)
      {
        temp = p2.y;
        p2.y = p1.y;
        p1.y = temp;
      }
      // Here +1 coz need to count the bottom line too
      canvas2DContext.fillRect(p1.x*cellWidth, p1.y*cellHeight, cellWidth*(p2.x-p1.x+1), cellHeight*(p2.y-p1.y+1));
    }
    // two points in the same column
    else if(p2.x==p1.x&&p2.y!=p1.y)
    {
      if(p2.y < p1.y)
      {
        temp = p2.y;
        p2.y = p1.y;
        p1.y = temp;
      }
      // Here +1 coz need to count the bottom line too
      canvas2DContext.fillRect(p1.x*cellWidth, p1.y*cellHeight, cellWidth, cellHeight*(p2.y-p1.y+1));
    }
    // two points in the same row
    else if(p2.x!=p1.x&&p2.y==p1.y)
    {
      if(p2.x < p1.x)
      {
        temp = p2.x;
        p2.x = p1.x;
        p1.x = temp;
      }
      // Here +1 coz need to count the bottom line too
      canvas2DContext.fillRect(p1.x*cellWidth, p1.y*cellHeight, cellWidth*(p2.x-p1.x+1), cellHeight);
    }
    // choose the single cell
    else if(p2.x==p1.x&&p2.y==p1.y)
    {
      canvas2DContext.fillRect(p1.x*cellWidth, p1.y*cellHeight, cellWidth, cellHeight);
    }
    // push chosen HRU cell num
    recordChosenAreaInfo(p1,p2);

  }


  // this function is used to add the chosen cell number into chosenHRU
  // for this function p1.x and p1.y should be =< p2.x and p2.y
  // after this function chosenHRU may have some duplicated elements
  function recordChosenAreaInfo(p1,p2)
  {
    // get the current chosen color number
    // var colorOptNum =
    //       parseInt($('input[name="vegcode-select"]:checked').val());

    // single point
    if(p1.x==p2.x && p1.y==p2.y)
    {
      //chosenHRU.push(p1.x+p2.y*vegColNum);
      chosenHRU.push([p1.x,p2.y]);
    }
    else
    {
      for(var m=p1.y; m<=p2.y; m++)
      {
        for(var i=p1.x; i<=p2.x; i++)
        {
          // chosenHRU.push(i+m*vegColNum);
          chosenHRU.push([i,m]);
        }
      }
    }
  
  }

  Array.prototype.max = function() {
    return Math.max.apply(null, this);
  };

  Array.prototype.min = function() {
    return Math.min.apply(null, this);
  };

  
  // the following five functions are for line arrow drawing on canvas
  // these five functions are from http://deepliquid.com/blog/archives/98
  function drawFilledPolygon(shape) {
      canvas2DContext.beginPath();
      canvas2DContext.moveTo(shape[0][0],shape[0][1]);

      for(p in shape)
          if (p > 0) canvas2DContext.lineTo(shape[p][0],shape[p][1]);

      canvas2DContext.lineTo(shape[0][0],shape[0][1]);
      canvas2DContext.fill();
  }

  function translateShape(shape,x,y) {
      var rv = [];
      for(p in shape)
          rv.push([ shape[p][0] + x, shape[p][1] + y ]);
      return rv;
  }

  function rotateShape(shape,ang) {
      var rv = [];
      for(p in shape)
          rv.push(rotatePoint(ang,shape[p][0],shape[p][1]));
      return rv;
  }
  function rotatePoint(ang,x,y) {
      return [
          (x * Math.cos(ang)) - (y * Math.sin(ang)),
          (x * Math.sin(ang)) + (y * Math.cos(ang))
      ];
  }

  function drawLineArrow(x1,y1,x2,y2) {
      canvas2DContext.beginPath();
      canvas2DContext.moveTo(x1,y1);
      canvas2DContext.lineTo(x2,y2);
      canvas2DContext.stroke();
      var ang = Math.atan2(y2-y1,x2-x1);
      drawFilledPolygon(translateShape(rotateShape(arrow,ang),x2,y2));
  }


});
