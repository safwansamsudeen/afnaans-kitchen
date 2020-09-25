$(function () {
    const date = new Date();
    document.querySelector('.year').innerHTML = date.getFullYear();
    $('.nav-item.active').css('box-shadow', 'inset 0 -3px 0 0 #000');
    $('.form-control').on('keyup', e => {
        const $unavailable = $(".unavailable")
        const $rows = $('.row')
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
                $node = $(node)
                if ($node.children(':visible').length === 1) $node.hide()
            })
        }
    })
})

