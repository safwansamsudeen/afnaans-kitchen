function updateSepPrices(node) {
    const price = parseInt(node.parents('td').siblings().children('.sep-price').text().replace(/,/g, ''));
    const totalPriceCell = node.parents('td').siblings().children('.total-price');
    const qty = parseInt(node.siblings('.qty').text().replace(/,/g, ''))
    totalPriceCell.text(isNaN(price * qty) ? location.reload() : (price * qty).toLocaleString());
}

function updateQty() {
    const qtys = $('.qty');
    let totalQty = 0;
    qtys.each((i, node) => {
        node = $(node);
        const qty = parseInt(node.text().replace(/,/g, ''));
        totalQty += isNaN(qty) ? location.reload() : qty
    })
    $('#total-qty').text(totalQty.toLocaleString());
}

function updateTotalPrice() {
    const prices = $('.total-price');
    let totalPrice = 0;
    prices.each((i, node) => {
        node = $(node);
        const price = parseInt(node.text().replace(/,/g, ''));
        totalPrice += isNaN(price) ? location.reload() : price
    })
    $('#total-price').text(totalPrice.toLocaleString());
}

$('.btn.add').on('click', e => {
    update_cart(e, num => num + 1);
    updateQty()
    updateSepPrices($(e.target))
    updateTotalPrice()
})

$('.btn.subtract').on('click', e => {
    update_cart(e, num => {
        if (num - 1 >= -1) return num - 1
        return 0
    })
    updateQty()
    updateSepPrices($(e.target))
    updateTotalPrice()
})