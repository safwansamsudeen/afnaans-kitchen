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

function notIsNanInIterable(iterable) {
    const newIterable = [];
    for (item of iterable) {
        item = parseInt(item);
        if (isNaN(item) || item < 0) location.reload();
        newIterable.push(item)
    }
    return newIterable
}

function getCookie(key) {
    var keyValue = document.cookie.match('(^|;) ?' + key + '=([^;]*)(;|$)');
    return keyValue ? keyValue[2] : null;
}

function update_cart(e, func) {
    const countButton = $(e.target).parent().children('.qty');
    let name = $(e.target).parents('.card-body').find('.item-name').text()
    if (!name) {
        name = $(e.target).parents('tr').find('.item-name').text()
    }
    let number = parseInt(countButton.text());
    notIsNanInIterable([number])
    number = func(number);
    if (number === -1) return
    countButton.html(number)
    axios.post(`${window.location.origin}/update_cart`, {
        item: name,
        qty: number,
    }, { headers: { "X-CSRFToken": getCookie('csrftoken') } })
        .then(data => console.log(data))
        .catch(err => console.log(err));
}