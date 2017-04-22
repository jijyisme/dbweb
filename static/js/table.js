

$("#table").hide();
$("#apply_btn").click(function(){
    $.ajax({
      type: "POST",
      url: "/home/teacher",
      data: { name: text}
    }).done(function() {
       $("#table").show();
    });

});