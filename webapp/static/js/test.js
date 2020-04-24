$(function(){
  $("div").slice(0, 3).show();
  $("#loadMore").on('click', function(e){
    e.preventDefault();
    $("div:hidden").slice(0, 3).slideDown();
  })
})