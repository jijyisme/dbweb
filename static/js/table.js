
var sel_tab = "tab_student";
var tname = "student";
var filter_detail = [];
var temp = [];

//for testing drawTable()


function drawTable(data){
  $('#table_data tr').remove();
        temp = filter_detail;
        var header = '<thead><tr class="w3-blue">';
        for(var i=0; i<temp.length; i++){
            header += '<th>'+temp[i].toUpperCase()+'</th>';
        }
        header += '</tr></thead>';
        $('#table_data').append(header);
// create rows
        var rows,begin_index=1;
        if(sel_tab=='tab_student'&&temp[0]!='id'){
          begin_index = 2;
        }
        for(var i=begin_index; i<data[1].length; i++) {

            rows = $("<tr>",{id:data[1][i]});
            rows.click(function(){

              if(sel_tab == 'tab_student'){
                getStudentData(this.id);
              }

            });
            rows.mouseover(function(){
              $(this).toggleClass("w3-grey w3-text-white");
            });
            rows.mouseout(function(){
              $(this).toggleClass("w3-grey w3-text-white");
            });
            for(var j=1; j<=data[0].length; j++){
            rows.append('<td>' + data[j][i] + '</td>');
            }
            $('#table_data').append(rows);
        }

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

function drawPersonalData(data){
  //clear previous panel
  $('#student_profile_table').hide();
  $('#student_profile_table p').remove();
  $('#student_profile_table h2').remove();
  $('#student_profile_table h5').remove();
  //add student's info
  $("#pd_year").append(data['name']);
  $("#pd_department").append(data['name']);
  $("#pd_faculty").append(data['name']);
  $("#pd_tel_no").append(data['name']);
  $("#pd_email").append(data['name']);
  $("#pd_gpax").append(data['name']);
  $("#pd_proj_name").append(data['name']);
  $("#pd_proj_field").append(data['name']);
  $("#pd_proj_advisor").append(data['name']);
  $("#pd_proj_type").append(data['name']);
  $("#pd_scholar").append(data['name']);
  $("#pd_scholar_period").append(data['name']);
  $("#pd_comp").append(data['name']);
  $("#pd_intern_period").append(data['name']);
  $("#pd_student_status").append(data['name']);
  $("#pd_drop_status").append(data['name']);
  $("#student_profile").show();
  //add enrollment table
  var enroll = data['enrollment'];
  // create header
          temp = ['course id', 'course name', 'grade', 'credit','term/year'];
          var header = '<thead><tr class="w3-blue">';
          for(var i=0; i<temp.length; i++){
              header += '<th>'+temp[i][0].toUpperCase()+'</th>';
          }
          header += '</tr></thead>';
          $('#student_profile_table').append(header);
  // create rows
          var rows;
          for(var i=0; i<data.length; i++) {
              rows = $("<tr>",{id:enroll[i]['id']});
              rows.mouseover(function(){
                $(this).toggleClass("w3-grey w3-text-white");
              });
              rows.mouseout(function(){
                $(this).toggleClass("w3-grey w3-text-white");
              });
              for(var j=0; j<temp.length; j++){
              rows.append('<td>' + enroll[i][temp[j][0]] + '</td>');
              }
              $('#student_profile_table').append(rows);
          }
          $('#student_profile_table').show();
  }

function drawUserData(data){
  $("#user_name").append("<h2>"+data['title']+data['name']+"</h2>");
  $("#user_info").append("<p>"+data['department']+"</p>");
  $("#user_info").append("<p>"+data['faculty']+"</p>");
//  $("#user_info").append("<p>"+data['name']+"</p>");
}
function getStudentData(s_id){
  $("#")
  $.ajax({
    type: "POST",
    url: "/home/student_info",
    data: {id: s_id},
    success: function(response) {
     console.log(response)
     drawPersonalData(response);
     }
  });
}
function getUserData(id){
  $.ajax({
    type: "POST",
    url: "/home/user_info",
    success: function(response) {
     drawUserData(response);
     }
  });
}
$(":checkbox").click(function(){
    console.log("check");
    filter_detail = [];
   $('input:checked').map(function() {
      filter_detail.push([this.value,'none','']);
   });
   console.log(filter_detail);
   drawFilterTab();

});


$("#apply_btn").click(function(){
// get filter value
  for(var i=0;i<filter_detail.length;i++){
    filter_detail[i][2] = $("#textbox"+i).val();
  }
  $("#student_profile").hide();
//send request to view.py
    $.ajax({
      type: "POST",
      url: "/home/query",
      dataType : "json",
      data: JSON.stringify({ 'tab' : sel_tab ,'filter' : filter_detail }),
      success: function(response) {
          console.log(response);
          var arr = [];
            $.each(response,function(key,value){
            arr.push(value);
            });
          console.log(arr);

          drawTable(arr);
          $("#table").show();
//        column = response["column"]
//        console.log(column)
//        for(var i=0;i<response.id.length;i++){
//            for(var j=0;j<column.length;i++){
//                console.log()
//            }
//        }
//        column = ['a', 'b', 'c']
//        for x in column:
//            if (x =='a')
//             response['a']
//             elif
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
    $("#student_profile").hide();
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
