
var sel_tab = "tab_student";
var tname = "student";
var filter_detail = [];
var temp = [];

// for testing drawTable()
// data = [
//   {id: '1', name: 'a'},
//   {id: '2', name: 'b'},
//   {id: '3', name: 'c'}
// ];
// temp = ['id','name'];

function drawTable(data){
// create header
        temp = filter_detail;
        var header = '<thead><tr class="w3-blue">';
        for(var i=0; i<temp.length; i++){
            header += '<th>'+temp[i].toUpperCase()+'</th>';
        }
        header += '</tr></thead>';

// create rows
        var rows = '';
        for(var i=0; i<data.length; i++) {
            rows += '<tr>';
            for(var j=0; j<temp.length; j++){
            rows += '<td>' + data[i][temp[j]] + '</td>';
            }
            rows += '</tr>';
        }

        $('#table_data').html(header+rows);
}
function drawFilterTab(){
$("#filtertab_detail").empty();
if(filter_detail.length==0){
  $('#filtertab_detail').append("<p> Please select column before filter</p>");
  return;
}
//create Operation and Value
var dropdown,textbox;
for(var i=0; i<filter_detail.length; i++){
  dropdown = $("<select>",{class:'test', id:i});
  dropdown.append("<option value='none'> None </option><option value='>'> Greater </option><option value='<'> Less </option><option value='='> Equal </option><option value='>='> Greater or Equal</option><option value='<='>Less or Equal</option>");
  (dropdown).change(function(){
    filter_detail[parseInt(this.id)][1] = $(this).find(":selected").val();
  });
  textbox = $("<input>",{type:'text', id:'textbox'+i});

  $("#filtertab_detail").append("<p>Column : "+filter_detail[i][0]);
  $('#filtertab_detail').append("Operation : ");
  $('#filtertab_detail').append(dropdown);
  $('#filtertab_detail').append(" Value : ");
  $('#filtertab_detail').append(textbox);
  $('#filtertab_detail').append("<p>");

  }

}


$(":checkbox").click(function(){
    filter_detail = [];
   $('input:checked').map(function() {
      filter_detail.push([this.value,'none','none']);
   });
   drawFilterTab();

});


$("#apply_btn").click(function(){
// get filter value
  for(var i=0;i<filter_detail.length;i++){
    filter_detail[i][2] = $("#textbox"+i).val();
  }
//send request to view.py
    $.ajax({
      type: "GET",
      url: "/home/teacher",
      data: {tab : sel_tab, filter : filter_detail },
      success: function(response) {
       drawTable(response);
       $("#table").show();
       }
    });
//just print sent data
    console.log(sel_tab);
    for(var i=0;i<filter_detail.length;i++){
      console.log(filter_detail[i]);
    }

});

//assign selected tab & reset selected filter
$(".btn-warning").click(function(){
    $("#filtertab_detail").empty();
    $(":checkbox").prop('checked', false);
    filter_detail = [];
    $("#addtab"+tname).hide();
    $("#filtertab").hide();
    $("#table").hide();
    sel_tab = this.id;
    tname = sel_tab.substring(4);

});


$("#addcolumn_btn").click(function(){
    $("#addtab"+tname).toggle();

});


$("#filter_btn").click(function(){
    drawFilterTab();
    $("#filtertab").toggle();

});

$("#signout_btn").click(function(){
    window.location = "/home"
});
