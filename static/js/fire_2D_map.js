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

  var setIntervalID;

  // these for veg type modification
  var vegColorScale = [];
  var veg2DGrid = [];
  var vegJson;
  var vegCellWidth;
  var vegCellHeight;
  var vegColNum;
  var vegRowNum;
  var chosenAreaInfo=[];
  var vegCode;
  var vegMetaData;

  var onFireCell = [];


  $.get('/api/fire_data', function(data){

    inputJson = JSON.parse(data);

    // grab col and row num
    dataX = inputJson['num_cols'];
    dataY = inputJson['num_rows'];
    
    fireOrigin = inputJson["fire_data"].slice();
    onFireCell = inputJson["fire_data"].slice();

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
  // TODO, cannot use url to get google map image based on the two corners
  function setupBackgroundMap()
  {veg2DGrid[tempRow][tempCol] = value1.colorNum
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

      canvas2DContext.globalAlpha = 1.0;
      var tempColor = hexToRgb(colorScale[1]);
      var tempColorString = 'rgba('+tempColor.r.toString()+','+tempColor.g.toString()+','+tempColor.b.toString()+',0.5)';
      for(var m=0 ; m<dataY ; m++)
      {
        for(var i=0 ; i<dataX ; i++)
        {
          
          if(currentTime == parseInt(fireCurrent[m][i]))
          {
            canvas2DContext.fillStyle = tempColorString;
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
        vegMetaData = vegJson['meta_data'];
        vegCode = vegJson['veg_code'];
        veg2DGrid = vegJson['grid_data'];
        vegColorScale = chroma.scale(['white','green']).colors(vegCode.length);
        // change rock value into black
        vegColorScale[vegCode.indexOf(99)] = '#000000';

        vegColNum = parseInt(vegMetaData[0][1]);
        vegRowNum = parseInt(vegMetaData[1][1]);
        vegCellWidth = canvasWidth/vegColNum;
        vegCellHeight = canvasHeight/vegRowNum;

        // generate button color
        for(var i=0; i<vegColorScale.length; i++)
        {
          $("#"+i.toString()+"square").css("color",vegColorScale[i]);
        }
        updateVeg();

      });
      
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
  function updateVeg()
  {

    canvas2DContext.globalAlpha = 0.5;
    for(var m=0 ; m<vegRowNum ; m++)
    {
      for(var i=0 ; i<vegColNum ; i++)
      {
        // canvas2DContext.fillStyle = colorScale[0];
        canvas2DContext.fillStyle = vegColorScale[vegCode.indexOf(parseInt(veg2DGrid[m][i]))];
        //                          start x,     y,            width,    height,          opacity
        canvas2DContext.fillRect(vegCellWidth*i,vegCellHeight*m,vegCellWidth,vegCellHeight);
        // draw lines to separate cell
        //canvas2DContext.rect(cellWidth*i,cellHeight*m,cellWidth,cellHeight);
      }
    }
    //canvas2DContext.stroke();
    setupBackgroundMap();
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
      var colorOptNum = parseInt($('#vegetation-type-selector label.active input').val());
            //parseInt($('input[name="vegcode-select"]:checked').val());
      chosenAreaInfo.push({colorNum:colorOptNum,chosenArea:chosenHRU});
      chosenHRU=[];
    });

  $("#save-veg-update").click(function(){

    $.each(chosenAreaInfo, function(index1, value1) {
      //var tempColor = value1.colorNum;
      $.each(value1.chosenArea,function(index2,value2){
        // convert 1D into 2D, this is coz of recordChosenAreaInfo using 1D but veg2DGrid is 2D
        var tempRow = Math.floor(value2/vegColNum);
        var tempCol = value2%vegColNum;
        veg2DGrid[tempRow][tempCol] = value1.colorNum;

        // canvas2DContext.fillStyle = colorScale[0];
        canvas2DContext.fillStyle = vegColorScale[vegCode.indexOf(parseInt(value1.colorNum))];
        //                          start x,     y,            width,    height
        canvas2DContext.fillRect(vegCellWidth*tempCol,vegCellHeight*tempRow,vegCellWidth,vegCellHeight);

      });
    });

  $("#post-veg-update").click(function(){
    // post the update info back to server
    $.ajax({
        type : "POST",
        url : "/api/update_veg_file",
        data: JSON.stringify(
          {
            veg_meta: vegMetaData,
            veg_2D_grid: veg2DGrid
          }, null, '\t'),
        contentType: 'application/json',
        success: function(result) {

          $.get('/api/update_veg_file', function(data){
              inputJson = JSON.parse(data);
              fireCurrent = inputJson["fire_data"].slice();
              $('#startButtonID').trigger("click");
          });

        }
    });

  });


    // TODO send changes back to server

    // update map overlay
    // updateMapOverlay();
  });


  $("#save-fire-update").click(function(){

    $.each(chosenAreaInfo, function(index1, value1) {
      //var tempColor = value1.colorNum;
      $.each(value1.chosenArea,function(index2,value2){
        // convert 1D into 2D, this is coz of recordChosenAreaInfo using 1D but veg2DGrid is 2D
        var tempRow = Math.floor(value2/vegColNum);
        var tempCol = value2%vegColNum;
        // 2 means on fire by users
        onFireCell[tempRow][tempCol] = 2;
        var tempColor = hexToRgb(colorScale[1]);
        var tempColorString = 'rgba('+tempColor.r.toString()+','+tempColor.g.toString()+','+tempColor.b.toString()+',0.5)';

        // canvas2DContext.fillStyle = colorScale[0];
        canvas2DContext.fillStyle = tempColorString;
        //                          start x,     y,            width,    height
        canvas2DContext.fillRect(vegCellWidth*tempCol,vegCellHeight*tempRow,vegCellWidth,vegCellHeight);

      });
    });


  // TODO need to merge fire update and veg post
  $("#post-fire-update").click(function(){
    // post the update info back to server
    $.ajax({
        type : "POST",
        url : "/api/update_fire_file",
        data: JSON.stringify(
          {
            fire_2D_grid: onFireCell
          }, null, '\t'),
        contentType: 'application/json',
        success: function(result) {

          $.get('/api/update_fire_file', function(data){
              inputJson = JSON.parse(data);
              fireCurrent = inputJson["fire_data"].slice();
              $('#startButtonID').trigger("click");
          });

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

  function changeCanvasCellColor(mousePosition,color)
  {
    var startX = Math.floor(mousePosition.x/vegCellWidth);
    var startY = Math.floor(mousePosition.y/vegCellHeight);
    canvas2DContext.fillStyle = color;
    canvas2DContext.fillRect(startX*vegCellWidth, startY*vegCellHeight, vegCellWidth, vegCellHeight);

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
      canvas2DContext.fillRect(p1.x*vegCellWidth, p1.y*vegCellHeight, vegCellWidth*(p2.x-p1.x+1), vegCellHeight*(p2.y-p1.y+1));
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
      canvas2DContext.fillRect(p1.x*vegCellWidth, p1.y*vegCellHeight, vegCellWidth, vegCellHeight*(p2.y-p1.y+1));
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
      canvas2DContext.fillRect(p1.x*vegCellWidth, p1.y*vegCellHeight, vegCellWidth*(p2.x-p1.x+1), vegCellHeight);
    }
    // choose the single cell
    else if(p2.x==p1.x&&p2.y==p1.y)
    {
      canvas2DContext.fillRect(p1.x*vegCellWidth, p1.y*vegCellHeight, vegCellWidth, vegCellHeight);
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
      chosenHRU.push(p1.x+p2.y*vegColNum);
    }
    else
    {
      for(var m=p1.y; m<=p2.y; m++)
      {
        for(var i=p1.x; i<=p2.x; i++)
        {
          chosenHRU.push(i+m*vegColNum);
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



});
