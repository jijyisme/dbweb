
var sel_tab = "";
var filter_detail = [['id','0','0'],['name','0','0'],['age','0','0']];
function drawTable(data){
// create header
        var header = '<thead><tr class="w3-blue">';
        for(var i=0; i<filter_detail.length; i++){
            header += '<th>'+filter_detail[i][0]+'</th>';
        }
        header += '</tr></thead>';

// create rows
        var rows = '';
        for(var i=0; i<data.length; i++) {
            rows += '<tr>';
            for(var j=0; j<filter_detail.length; j++){
            rows += '<td>' + data[i][j] + '</td>';
            }
            rows += '</tr>';
        }

        $('#table_data').html(header+rows);
}

$("input").click(){
    $('input:checked').map(function() {
       filter_detail.push([$(this).val,0,0]);
    });
}
$("#table").hide();
$("#apply_btn").click(function(){

    $.ajax({
      type: "GET",
      url: "/home/teacher",
      data: {tab : sel_tab, filter : filter_detail },
      success: function(response) {
       drawTable(response);
       $("#table").show();
       }
    });

});

//assign selected tab
$("class_of_tab").click(function(){
    sel_tab = "";
    $("#addcolumn_pane"+"_"+sel_tab).hide();
    $("#filter_pane").hide();
    $("#table").hide();
});
$("#addcolumn_btn").click(function(){

    $("#addcolumn_pane"+sel_tab).toggle();

});
$("#filter_btn").click(function(){

    $("#filter_pane"+sel_tab).toggle();

});
$(function () {
  $('#target').click(function () {
    var checkValues = $('input[name=checkboxlist]:checked').map(function() {
        return $(this).parent().text();
    }).get();
      alert(checkValues);
  });

});
