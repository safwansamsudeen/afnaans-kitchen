
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
    validator = $("#order-form").validate({
        rules: {
            phonenumber: {
                number: true,
                minlength: 10
            },
        },
        onfocusout: function (element) {
            $(element).valid();
        },
        submitHandler: (form, e) => {
            form = $(form);
            if (!form.valid()) return
            const submitter = $(e.originalEvent.submitter)
            if (submitter.attr('id') === 'true-submit') {
                console.log('In');
                form.submit()
            }
            const part = submitter.parents('div.part');
            part.slideUp(500);
            const next_part = part.next()
            next_part.slideDown(500)
            $('#part-title').text(title(next_part.attr('id').replace('_', ' ')))
        }
    });
});
