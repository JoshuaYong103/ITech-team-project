$(document).ready(function() {
    $('#like_btn').click(function() {
        var categoryLiked;
        categoryLiked = $(this).attr('data-liked');
        console.log(categoryLiked);
        console.log("Testing");
        $.get('/rango/like_category/',
        {'category_liked':categoryLiked},
        function(data) {
            $('#like_count').html(data);
            $('#like_btn').hide();
        })
    });

    $('#search-input').keyup(function() {
        var query;
        query = $(this).val();

        $.get('/rango/suggest',
                {'suggestion': query},
                function(data) {
                    $('#categories-listing').html(data);
                })
    });

    $('.rango-page-add').click(function() {
        var categoryid = $(this).attr('data-categoryid');
        var title = $(this).attr('data-title');
        var url = $(this).attr('data-url');
        var clickedButton = $(this);

        $.get('/rango/search_add_page/',
                {'category_id': categoryid, 'title':title, 'url': url},
                function(data) {
                    $('#page-listing').html(data);
                    clickedButton.hide();
                })
    });
});