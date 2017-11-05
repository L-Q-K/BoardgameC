$(document).ready(function(){

  $('#room-name').focus(function(input) {
    $('#room-name').attr('type', "number");
    $('#room-name').attr('placeholder', "Number of player");
  });

});
