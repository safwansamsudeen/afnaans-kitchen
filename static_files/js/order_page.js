
$(function () {
    function title(str) {
        return str.toLowerCase().split(' ').map(function (word) {
            return (word.charAt(0).toUpperCase() + word.slice(1));
        }).join(' ');
    }
    $('#order-form').areYouSure(
        {
            message: 'It looks like you have been editing something. '
                + 'If you leave before saving, your changes will be lost.'
        }
    );
    $('.next-part').on('click', e => {
        const part = $(e.target).parents('div[class$="-part"]');
        part.slideUp(500);
        const next_part = part.next()
        next_part.slideDown(500)
        $('#part-title').text(title(next_part[0].id.replace('_', ' ')))
    })

});
