// ----- custom js ----- //
var imagePath = 'static/images/';

$(document).ready(function() {

  console.log("ready");
  modalControl();
  getAllImages();

});

// request for all images in database to display in modal
var getAllImages = function(){

     $.ajax({
      url: "/list",
      cache: false,
      contentType: false,
      processData: false,                        
      type: 'POST',
      success: function(data){
        displayModalImages(data.imgList);
      },
      error: function(error){
        console.log(error.toString()); 
      }
   });
}

// Detects objects on an image
function detectObjects(image){
    $.ajax({
      url: "/detectObjects",
      type: 'POST',
      data: { 'image': image },
      beforeSend: function(){
        _html_ = '<img style="height:100%; width:100%;" src="static/loading.gif" />';
        document.getElementById('i'+image.split('/').reverse()[0]).innerHTML = _html_;
      },
      success: function(response){
        _html_ = "<img class=responsive src='"+response['image']+"' />";
        document.getElementById('i'+image.split('/').reverse()[0]).innerHTML = _html_;
      },
      error: function(error){
        alert('May be Nothing Detected in this IMAGE !');
        _html_ = '<img class=responsive src="'+image+'" />';
        document.getElementById('i'+image.split('/').reverse()[0]).innerHTML = _html_;
      }
   });
}

// displays images in modal
var displayModalImages = function(imgList){

   for(var i = 0; i < imgList.length; i++){
      $(".modal-images-list").append("<img src="+imagePath+imgList[i]+" class=modal-image onclick=imageSelectSearch(this) />");

   }

}

// handles click of modal image
var imageSelectSearch = function(_this) {
  var src = $(_this).attr("src");

  $("#modal").css("display", "none");
  $(".img-preview").attr("src", src);
  $("#results").html("");
  $("#results").append("<div id=searching>  <img src='static/loading.gif' />  </div>");

  var image = src.split('/')[2];
  var imageName = image.split('.')[0];

  $("#preview-name").text('IMAGE: '+imageName);

  $.ajax({
    url: "/search",
    data: {img: image},
    cache: false,
    type: 'POST',
    success: function(data){
      displayResults(data.results);
    },
    error: function(error){
      console.log(error.toString()); 
    }
   });

}

//display results
var displayResults = function(data){

  $("#results").html("");

  for(var i = 0; i < data.length; i++){
    var image = data[i].image;
    var score = data[i].score;
    var element = "<div class=img-result> <button style='height:100%; width:100%;' id='"+imagePath+image+"' onclick='detectObjects(this.id)' > <div id='i"+image+"'> <img class=responsive src="+imagePath+image+"/> </div>  <div class=img-info>"+"<span style='color:blue;' class=image-name>IMAGE: "+image+"</span><span style='color:blue;' class=img-score>SCORE: "+score+"</span> </span><span style='color:red;' class=img-name>Click on this image to Detect Objects!</span> </div> </button> </div>"
    $("#results").append(element);
  }
}

//Controls the opening and closing of the modal
var modalControl = function(){

  // Get the modal
  var modal = document.getElementById("modal");

  // Get the button that opens the modal
  var btn = document.getElementById("select");
  console.log(modal);
  
  // Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];
  
  // When the user clicks the button, open the modal 
  btn.onclick = function() {
    modal.style.display = "block";
  }
  
  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    modal.style.display = "none";
  }
  
  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
}