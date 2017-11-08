$(document).ready(function(){

  $('#Nop').focus(function(input) {
    $('#Nop').attr('type', "number");
    $('#Nop').attr('placeholder', "Number of player");
  });

  $('#room_code').focus(function(input) {
    $('#room_code').attr('type', "text");
    $('#room_code').attr('placeholder', "Room_code");
  });

});
