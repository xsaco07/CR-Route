$(document).ready(function() {
  $("a.btn").click(function() {
    console.log("click");
    var currentClass = $(this).find("i").attr('class');
    console.log(currentClass);
    if (currentClass == "fas fa-angle-up") {
      $(this).find("i").attr('class', "fas fa-angle-down");
    }
    else {
      $(this).find("i").attr('class', "fas fa-angle-up");
    }
  });
});
