var test='';
var host='http://localhost:8000/api/meta/v2/down/?'
var m_url = '';
var servers = {
            1: "fzaqn",
            2: "agobe",
            3: "topsa",
            4: "hcqwb",
            5: "gdasz",
            6: "iooab",
            7: "idvmg",
            8: "bjtpp",
            9: "sbist",
            10: "gxgkr",
            11: "njmvd",
            12: "trciw",
            13: "sjjec",
            14: "puust",
            15: "ocnuq",
            16: "qxqnh",
            17: "jureo",
            18: "obdzo",
            19: "wavgy",
            20: "qlmqh",
            21: "avatv",
            22: "upajk",
            23: "tvqmt",
            24: "xqqqh",
            25: "xrmrw",
            26: "fjhlv",
            27: "ejtbn",
            28: "urynq",
            29: "tjljs",
            30: "ywjkg"
        }

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
                     url: host+'yt_url='+url+'&format=jsonp',
                     type: 'GET',
                     dataType: 'jsonp',
                     success: function (data) {


                         var item_list = data['objects'];
                         for (step = 0; step < item_list.length; step++) {
                         var d_url = item_list[step]['d_url'];
                         m_url = item_list[step]['m_url'];
                         var video_id = item_list[step]['url'].split("?v=")[1];

//                         $.ajax({
//  type: 'GET',
//  dataType: 'jsonp',
//  url: "https://d.yt-downloader.org/check.php?/",
//  data: {
//                v: video_id,
//                f: "mp3"
//            },
//  success: function(data1) {
//    console.log(data1.sid);
//    console.log(servers[data1.sid]);
//     m_url ='http://' + servers[data1.sid] + '.yt-downloader.org/download.php?id=' + data1.hash;

                            console.log("current");
                             var current = '<video  style="width:50vw; margin-bottom: 30px; height:30vw; auto;" controls poster="https://img.youtube.com/vi/'+video_id+'/sddefault.jpg"><source src='+d_url+' type="video/mp4"></video><a  href='+m_url+' ><font color="white">Download MP3</font></a>';

                            test=current+test;
$(".download-buttom").html(test);

//  }
//});





}



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




















