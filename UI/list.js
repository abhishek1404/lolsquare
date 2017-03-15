var test='';
var host='http://localhost:8000/api/meta/v2/down/?'
var m_url = '';


function get_download_url(c) {

       return  $.ajax({
  type: 'GET',
  dataType: 'jsonp',
  url: "https://d.yt-downloader.org/check.php?/",
  data: {
                v: c,
                f: "mp3"
            },
  success: function(data) {
    console.log(data.sid);
    console.log(servers[data.sid]);
     m_url ='http://' + servers[data.sid] + '.yt-downloader.org/download.php?id=' + data.hash;



  }
});
    }






function download  (url) {

                 $.ajax({
                     url: 'https://www.videoder.net/search?query=shape%20of%20you',
                     type: 'GET',
                     dataType: 'jsonp',
                     success: function (data) {


//                         var item_list = data['objects'];
//                         for (step = 0; step < item_list.length; step++) {
//                         var d_url = item_list[step]['d_url'];
//                         m_url = item_list[step]['m_url'];
//                         var video_id = item_list[step]['url'].split("?v=")[1];
//
//
//                            console.log("current");
//                             var current = '<li><iframe  style="width:56vw; height:40vw; auto;" src=\"https://www.youtube.com/embed/'+video_id+'\"  frameborder="0" allowfullscreen>><a><img src="https://img.youtube.com/vi/'+video_id+'/hqdefault.jpg" style="cursor:pointer"></a></iframe><div class="date"><h4><a id ='+video_id+'style= "padding-left: 36em;" download="#" href="#"><span  class="glyphicon glyphicon-download">Download</span></a></h4></div></li>';
//
//                            test=current+test;


//  }
//});
$(".download-buttom").html(data['response']);








                     },
                     error: function (data) {
                         console.log('Error in Operation');
                     }
                 });




         }


$("#nav-search-bar").click(function() {
query = document.getElementById("input").value;
console.log(query);
download(query);
});

$('#input').keypress(function(e){
        if(e.which == 13){//Enter key pressed
            $('#nav-search-bar').click();//Trigger search button click event
        }
    });



//////search

$('#input').on('keyup', function() {
     if (this.value.length > 1) {
                          $.ajax({
                     url:'https://suggestqueries.google.com/complete/search?client=youtube&ds=yt&q='+this.value+'&callback=jQuery1111025235569831411553_1488721251189&_=1488721251192',
                     type: 'GET',
                     dataType: 'jsonp',
                     success: function (data) {

                     var suggestions = [];
                     $.each(data[1], function(key, val) {
                     var temp = val[0];//'<div><a class="s" href="#" style="background-color: rgb(240, 240, 240);">'+val[0]+'</a><div>';
                    suggestions.push(temp);
                });


//
$( "#input" ).autocomplete({
  source: suggestions
});

}                 });
     }
});




















