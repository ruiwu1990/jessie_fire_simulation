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
  // map center
  var center;

  // this is for mouse dragging
  var isDragging = false;
  var isMousePressing = false;
  var firstPosition;
  var secondPosition;

  var currentTime = 0;

  var backgroundMap = new Image();
  var canvasSize = [];

  // TODO this part should not be hard coded
  var veg_type_num = [];

  var setIntervalID;

  var vegColorScale = [];
  var veg2DGrid = [];
  var vegJson;


  $.get('/api/fire_data', function(data){
    inputJson = JSON.parse(data);

    // grab col and row num
    dataX = inputJson['num_cols'];
    dataY = inputJson['num_rows'];
    
    fireOrigin = inputJson["fire_data"].slice();

    var maxTime = inputJson['max_val'];
    var notsetfireVal = inputJson['notsetfire_Val'];


    // // should not use var fireCurrent = fireOrigin
    // // coz when we change fireCurrent and then fireOrigin will change too
    fireCurrent = fireOrigin.slice();

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
    // var scaleSize = 2;
    // colorScale = chroma.scale(['green','red']).colors(scaleSize);
    colorScale = ['#00FF00','#FF0000'];

    // init map
    var xllcorner = parseFloat(inputJson['let_top_lat']);
    var xurcorner = parseFloat(inputJson['right_bottom_lat']);
    var yllcorner = parseFloat(inputJson['right_bottom_long']);
    var yurcorner = parseFloat(inputJson['left_top_long']);
    center = [(xllcorner+xurcorner)/2,(yllcorner+yurcorner)/2];

    center = [39.5401289,-119.81453920000001];
    // set up background map img
    // var google_tile = "http://maps.google.com/maps/api/staticmap?sensor=false&center=" + center[0].toString() + "," +
    //                     center[1].toString() + "&zoom=14&size="+canvasSize[0].toString()+"x"+canvasSize[1].toString()+"&markers=color:blue|label:U|" +
    //                     center[0].toString() + ',' + center[1].toString();

    var google_tile = "http://maps.google.com/maps/api/staticmap?sensor=false&center=-30.397,150.644&zoom=8&size="+canvasSize[0].toString()+"x"+canvasSize[1].toString();
    var google_tile = "http://maps.google.com/maps/api/staticmap?sensor=false&center=-30.397,150.644&zoom=8&size=906x642";
    backgroundMap.src = google_tile;

    //setupBackgroundMap();
    initCanvas();
    $('#startButtonID').on('click',function(){
      setIntervalID = setInterval(updateCanvas, 10);

      $('#stopButtonID').on('click',function(){
        clearInterval(setIntervalID);
      });

      $('#getOnFireButtonID').on('click',function(){
        clearInterval(setIntervalID);
        var onFireInfo = getOnFireInfo();
        $.ajax({
              type : "POST",
              url : "/api/update_fire_info",
              data: JSON.stringify(
                {
                  fire_info_arr: onFireInfo,
                  num_cols: dataX,
                  num_rows: dataY
                }, null, '\t'),
              contentType: 'application/json',
              success: function(result) {

              }
          });

      });
    });
    


  });

  function getOnFireInfo()
  {
      var temparr = [];
      var outarr=[];
      for(var m=0 ; m<dataY ; m++)
      {
        temparr = [];
        for(var i=0 ; i<dataX ; i++)
        {
          if(currentTime >= parseInt(fireCurrent[m][i]))
          {
            temparr.push('1');
          }
          else
          {
            temparr.push('0');
          }
        }
        outarr.push(temparr);
      }
      return outarr;
  }

  function setupBackgroundMap()
  {
    backgroundMap.onload = function(){
      canvas2DContext.globalAlpha = 1.0;
      canvas2DContext.drawImage(backgroundMap, 0, 0);
    }
    
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

      canvas2DContext.globalAlpha = 0.5;

      for(var m=0 ; m<dataY ; m++)
      {
        for(var i=0 ; i<dataX ; i++)
        {
          // if(currentTime == fireCurrent[i+m*dataX])
          if(currentTime == parseInt(fireCurrent[m][i]))
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

      setupBackgroundMap();
  }
  function initCanvas()
  {
      // for current version, onfire 2D grid cell num should be >= then veg grid cell num 
      $.get('/api/veg_data',function(data){
        vegJson = JSON.parse(data);
        var vegMetaData = vegJson['meta_data'];
        var vegCode = vegJson['veg_code'];
        veg2DGrid = vegJson['veg_grid_data'];
        vegColorScale = chroma.scale(['white','green']).colors(vegCode);
        // change rock value into black
        vegColorScale[vegCode.indexOf(99)] = '#000000';

        canvas2DContext.globalAlpha = 0.5;
        for(var m=0 ; m<dataY ; m++)
        {
          for(var i=0 ; i<dataX ; i++)
          {
            // canvas2DContext.fillStyle = colorScale[0];
            canvas2DContext.fillStyle = vegColorScale[vegCode.indexOf(veg2DGrid[m][i])];
            //                          start x,     y,            width,    height
            canvas2DContext.fillRect(cellWidth*i,cellHeight*m,cellWidth,cellHeight);
            // draw lines to separate cell
            //canvas2DContext.rect(cellWidth*i,cellHeight*m,cellWidth,cellHeight);
          }
        }
        //canvas2DContext.stroke();
        setupBackgroundMap();

      });
      
  }

  Array.prototype.max = function() {
    return Math.max.apply(null, this);
  };

  Array.prototype.min = function() {
    return Math.min.apply(null, this);
  };



});
