function initVue(data) {
    const App = new Vue({
        el: '#menu',
        delimiters: ['[{', '}]'],
        data() {
            return {
                data: data.data
            }
        }
    })
}
// axios.get(`${window.location.origin}/cart_details`).then(data => initVue(data))

$('.form-control').on('keyup', e => {
    const $unavailable = $(".unavailable")
    const $rows = $('.row.item-row')
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