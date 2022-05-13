$(document).ready(function (){
   $('#search-btn').on('click', function (e) {
       e.preventDefault();
       var searchText = $('#search-box').val();
       $.ajax( {
           url: '/listing/search?search_filter=' + searchText,
           type: 'GET',
           success: function(resp){
                var newHTML = resp.data.map(d => {
                    return <div class="well listing">
                        <a href="/listings"$.{d.id}>
                            <image class="listing-img" src="${d.firstImage}"></image>
                            <h4>${d.name}</h4>
                            <p>${d.description}</p>
                        </a>
                    </div>
                });

           },
           error: function (xhr, status, error){
               // TODO: Gera þetta aðeins meira sexy
               console.error(error);
           }
       })
   })
});