$(function(){
  // $("#show-history").on('click', function(){
  //   $("#reading-list").slideToggle('fast',function(){});
  // });
  $(".show-five-list").hide();

  $(".show-five").on('click', function(){
    $("#"+ this.id + "-list").slideToggle('fast',function(){});
  });

  $(".robot-img").click(function(){
    $(".robot-img").removeClass("selected");
    $(this).addClass("selected")
  })
});

function flash_target_dom(dom_path){
  $("#" + dom_path + '-reading').addClass('dom_flash',1000);
  setTimeout(function(){
    $("#" + dom_path + '-reading').removeClass('dom_flash');},1000);
};