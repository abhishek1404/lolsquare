
var number_of_pages=1;
var host='http://localhost:8000/api/meta/v2/videos/?'

var test='';
var search_test='';
var search = false;
var query ='';
var li_element =`

`;
function display  (arg) {


                 $.ajax({
                     url: host+'format=jsonp',
                     type: 'GET',
                     dataType: 'jsonp',
                     success: function (data) {
                     number_of_pages = Math.floor(data['meta']['total_count']/data['meta']['limit']);
                     setPagination(active=arg);
                         var item_list = data['objects'];
                         for (step = 0; step < item_list.length; step++) {
                         var id = item_list[step]['video_url'].split("?v=")[1];
                             var current = '<li><div class="date"><h4>'
                             +item_list[step]['video_title']+'</div><video style="width:66vw; height:30vw; auto;" controls><source   src='+item_list[step]['download_url']+' type="video/mp4"></video></li>';




                            //console.log(test);
                             test=test+current;
}
$(".tileMe").html(test);

                     },
                     error: function (data) {
                         console.log('Error in Operation');
                     }
                 });
         }

   function setPagination(active){

            var pagination_html = '';
            for (step = 0; step < number_of_pages; step++) {
            console.log(active);

                             var current='';
                             var page=step+1;

                             if(page===active){
                             if (active===1){


                             current='<li class="page-item disabled"><span class="page-link">Previous</span></li><li class="page-item active"><a class="page-link" href="#" onclick=display(arg='+page+');>1<span class="sr-only">(current)</span></a></li>';
                             pagination_html=pagination_html+current;

                             }
                             else{

                             current='<li class="page-item disabled"></li><li class="page-item active"><a class="page-link" href="#" onclick=display(arg='+page+');>'+active+'<span class="sr-only">(current)</span></a></li>';
                             pagination_html=pagination_html+current;

                             }

                             }

                             else{

                             if (page===1)
                             {

                             current='<li class="page-item disabled"><span class="page-link">Previous</span></li><li class="page-item "><a class="page-link" href="#" onclick=display(arg='+page+');>1</a></li>';
                             pagination_html=pagination_html+current;

                            }
                             else{

                             current = '<li class="page-item"><a class="page-link" href="#" onclick=display(arg='+page+');>'+page+'</a></li>'
                             pagination_html=pagination_html+current;}
                            //console.log(test);
                        }
                        }


pagination_html=pagination_html+'<li class="page-item"> <a class="page-link" href="#">Next</a></li>'
$(".pagination").html(pagination_html);}

$( document ).ready( display(arg=1) );

            var count = 2;
            $(window).scroll(function(){
                    if(($(window).scrollTop() + $(window).height() > $(document).height() - 100)&& number_of_pages>count){
                       if (search===true ){search_api(arg=count,query);}else{display(arg=count);}
                       count++;
                    }
            });



$body = $("body");

$(document).on({
    ajaxStart: function() { $body.addClass("loading"); },

     ajaxStop: function() { $body.removeClass("loading");    }
});












