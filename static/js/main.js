$(function () {
    const date = new Date();
    document.querySelector('.year').innerHTML = date.getFullYear();
    $('.nav-item.active').css('box-shadow', 'inset 0 -3px 0 0 #000')
})

