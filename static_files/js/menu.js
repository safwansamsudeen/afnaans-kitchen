$(function () {
    $('.btn.add').on('click', e => update_cart(e, num => num + 1))
    $('.btn.subtract').on('click', e => update_cart(e, num => {
        if (num - 1 >= -1) return num - 1
        return 0
    }))
    function hideEmptyRows() {
        const $rows = $('.row.item-row');
        $rows.each((i, node) => {
            const $node = $(node);
            if ($node.children(':visible').length === 1) $node.remove();
        })
    }
    hideEmptyRows()
    $('.form-control').on('keyup', e => {
        const $unavailable = $(".unavailable");
        const $rows = $('.row.item-row');
        const $items = $(".item");
        let $results = [];
        const query = e.target.value.toLowerCase().trim()
        $rows.show();
        $unavailable.hide();
        $items.hide();
        $items.each((i, node) => node.textContent.toLowerCase().includes(query) ? $results.push(node) : null)
        $results = $($results);
        if ($results.length === 0) {
            $rows.hide();
            $unavailable.show();
        } else {
            $results.show();
            hideEmptyRows()
        }
    })
    if (!$('.search-group').find('.item')[0]) {
        $('.search-group').append('<div class="my-4">Sorry! There are no available items.</div>')
    }
})