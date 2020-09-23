$(function () {
    const date = new Date();
    document.querySelector('.year').innerHTML = date.getFullYear();
    $('.nav-item.active').css('box-shadow', 'inset 0 -3px 0 0 #000');
    $('.form-control').on('keyup', e => {
        const $unavailable = $(".unavailable")
        $unavailable.hide();
        $(".item").hide();
        console.log(e.target.value.trim().toLowerCase())
        const results = $(".item:contains(" + e.target.value.trim().toLowerCase() + ")");
        results.length === 0 ? $unavailable.show() : results.show();
    })
})

