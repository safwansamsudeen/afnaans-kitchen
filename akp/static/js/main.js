$(function () {
    const date = new Date();
    document.querySelector('.year').innerHTML = date.getFullYear();

    setTimeout(() => $("#message").fadeOut("slow"), 3000)

    $('.nav-item.active').css('box-shadow', 'inset 0 -3px 0 0 #000');

    document.onkeydown = e => {
        if (e.metaKey && e.ctrlKey && e.key === 'k') {
            window.open('admin')
        }
    }
})