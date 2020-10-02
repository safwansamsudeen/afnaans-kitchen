$(function () {
    function getCookie(key) {
        var keyValue = document.cookie.match('(^|;) ?' + key + '=([^;]*)(;|$)');
        return keyValue ? keyValue[2] : null;
    }

    function changer(e, func) {
        const countButton = $(e.target).parent().children('.count');
        const name = $(e.target).parents('.card-body').find('h4').text()
        console.log(name)
        let number = parseInt(countButton.html());
        if (isNaN(number)) location.reload();
        number = func(number);
        countButton.html(number)
        if (number === 0) return
        axios.post(`${window.location.origin}/update_cart`, {
            item: name,
            qty: number,
        }, { headers: { "X-CSRFToken": getCookie('csrftoken') } })
            .then(data => console.log(data))
            .catch(err => console.log(err));
    }

    $('.btn.add').on('click', e => changer(e, num => num + 1))
    $('.btn.subtract').on('click', e => changer(e, num => {
        if (num - 1 >= 0) return num - 1
        return 0
    }))

    $('.form-control').on('keyup', e => {
        const $unavailable = $(".unavailable");
        const $rows = $('.row.item-row');
        const $items = $(".item");
        let $results = [];
        $rows.show();
        $unavailable.hide();
        $items.hide();
        $items.each((i, node) => node.textContent.toLowerCase().includes(e.target.value.toLowerCase()) ? $results.push(node) : null)
        $results = $($results);
        if ($results.length === 0) {
            $rows.hide();
            $unavailable.show();
        } else {
            $results.show();
            $rows.each((i, node) => {
                const $node = $(node);
                if ($node.children(':visible').length === 1) $node.hide();
            })
        }
    })
})