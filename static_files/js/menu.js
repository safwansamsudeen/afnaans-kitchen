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
            if ($node.children(':visible').length === 1) $node.hide();
        })
    }
    hideEmptyRows()
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
            hideEmptyRows()
        }
    })
})