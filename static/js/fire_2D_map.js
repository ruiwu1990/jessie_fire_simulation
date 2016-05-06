$(document).ready(function(){
  // TODO this part should be done byusing get request
  // get the color from get request from the server
  var inputJson;

  // set up the canvas size
  var cellWidth = 1;
  var cellHeight = 1;

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

  // this is for mouse dragging
  var isDragging = false;
  var isMousePressing = false;
  var firstPosition;
  var secondPosition;

  var currentTime = 0;


  $.get('/fire_data', function(data){
    inputJson = JSON.parse(data);

    // grab col and row num
    dataX = inputJson['num_cols'];
    dataY = inputJson['num_rows'];
    // convert the json file into 1d, this is because my previous functions are
    // designed for 1d only
    fireOrigin = obtainJsoninto1D(inputJson);

    var maxTime = inputJson['max_val'];
    var notsetfireVal = inputJson['notsetfire_Val'];


    // // should not use var fireCurrent = fireOrigin
    // // coz when we change fireCurrent and then fireOrigin will change too
    fireCurrent = fireOrigin.slice();

    canvasWidth = cellWidth*dataX;
    canvasHeight = cellHeight*dataY;
   
    $('.mapCanvas').attr('width',canvasWidth.toString()+'px');
    $('.mapCanvas').attr('height',canvasHeight.toString()+'px');

    // place mapArray into canvas
    canvasHandle = document.getElementById("myCanvas");
    canvas2DContext = canvasHandle.getContext("2d");

    // for current version, we only have on fire and not on fire
    // var scaleSize = 2;
    // colorScale = chroma.scale(['green','red']).colors(scaleSize);
    colorScale = ['#00FF00','#FF0000'];

    initCanvas();

    // init map
    var xllcorner = parseFloat(inputJson['let_top_lat']);
    var xurcorner = parseFloat(inputJson['right_bottom_lat']);
    var yllcorner = parseFloat(inputJson['right_bottom_long']);
    var yurcorner = parseFloat(inputJson['left_top_long']);
    overlayCanvasonGoogleMap(xllcorner,xurcorner,yllcorner,yurcorner);

    setInterval(updateCanvas, 10);
    //updateCanvas(926);



  });

  function obtainJsoninto1D(inputJson)
  {
      var outputarr = [];
      for(var m=0 ; m<dataY ; m++)
      {
        for(var i=0 ; i<dataX ; i++)
        {
          outputarr.push(inputJson["fire_data"][m][i]);
        }
      }
      return outputarr;
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
      for(var m=0 ; m<dataY ; m++)
      {
        for(var i=0 ; i<dataX ; i++)
        {
          if(currentTime == fireCurrent[i+m*dataX])
          {
            canvas2DContext.fillStyle = colorScale[1];
            //                          start x,     y,            width,    height
            canvas2DContext.fillRect(cellWidth*i,cellHeight*m,cellWidth,cellHeight);
            // draw lines to separate cell
            //canvas2DContext.rect(cellWidth*i,cellHeight*m,cellWidth,cellHeight);
          }
        }
      }
      //canvas2DContext.stroke();
      currentTime = currentTime + 1;

      // update google map overlay
      // need to set up some intervals or the refresh rate to fast and the google map cannot follow up
      if(currentTime%100 == 0)
      {
        updateMapOverlay();
      }
      //updateMapOverlay();
  }
  function initCanvas()
  {
      for(var m=0 ; m<dataY ; m++)
      {
        for(var i=0 ; i<dataX ; i++)
        {
          canvas2DContext.fillStyle = colorScale[0];
          //                          start x,     y,            width,    height
          canvas2DContext.fillRect(cellWidth*i,cellHeight*m,cellWidth,cellHeight);
          // draw lines to separate cell
          //canvas2DContext.rect(cellWidth*i,cellHeight*m,cellWidth,cellHeight);
        }
      }
      //canvas2DContext.stroke();
  }

  Array.prototype.max = function() {
    return Math.max.apply(null, this);
  };

  Array.prototype.min = function() {
    return Math.min.apply(null, this);
  };



});
