$(document).ready(function() {
    $('#like_btn').click(function() {
        var cateaboutIdVar;
        cateaboutIdVar = $(this).attr('data-aboutid');

        $.get('/rango/like_about/',
        {'about_id': cateaboutIdVar},
        function(data) {
            $('#like_count').html(data);
            $('#like_btn').hide();
        })
    });
});