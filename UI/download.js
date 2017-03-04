var test='';
var host='http://localhost:8000/api/meta/v2/down/?'

function download  (url) {

                 $.ajax({
                     url: host+'yt_url='+url+'&format=jsonp',
                     type: 'GET',
                     dataType: 'jsonp',
                     success: function (data) {

                         var d_url = data['objects'][0]['d_url'];
                         var id = url.split("?v=")[1];
                         var button=`<button>
  <p>Download</p>
</button>`;
                             var current = '<h3><a  download='+d_url+' href='+d_url+'>'+button+'</a></h3>';





$(".download-buttom").html(current);

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