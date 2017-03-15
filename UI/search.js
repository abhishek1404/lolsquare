
function search_api(arg,query) {

                 $.ajax({
                     url: host+'video_title__icontains='+query+'&format=jsonp',//offset='+(4*arg-1)+'&limit=4
                     type: 'GET',
                     dataType: 'jsonp',
                     success: function (data) {
                     number_of_pages = Math.floor(data['meta']['total_count']/data['meta']['limit']);
                     setPagination(active=arg);
                         var item_list = data['objects'];
                         for (step = 0; step < item_list.length; step++) {
                         var id = item_list[step]['video_url'].split("?v=")[1];


                             var current = '<li><div class="date"><h4>'
                             +'Title:'+item_list[step]['video_title']+'</dic><iframe  style="width:66vw; height:40vw; auto;" src=\"https://www.youtube.com/embed/'+id+'\"  frameborder="0" allowfullscreen><a><img src="https://img.youtube.com/vi/'+id+'/hqdefault.jpg" style="cursor:pointer"></a></iframe><div class="date"><h4>Views:'+item_list[step]['views']+
                             '<a style= "padding-left: 36em;" download='+item_list[step]['download_url']+'href='+item_list[step]['download_url']+'><span  class="glyphicon glyphicon-download">Download</span></a></h4></div></li>';





                            //console.log(search_test);
                             search_test=search_test+current;
}
$(".tileMe").html(search_test);

                     },
                     error: function (data) {
                         console.log('Error in Operation');
                     }
                 });
         }


$("#nav-search-bar").click(function() {
search=true;
query = document.getElementById("input").value;
console.log(query);

search_api(arg=1,query);
});

$('#input').keypress(function(e){
        if(e.which == 13){//Enter key pressed
            $('#nav-search-bar').click();//Trigger search button click event
        }
    });


