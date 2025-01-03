const rootUrl = 'http://localhost:8000';
function updateCart() {
    const cart = JSON.parse(localStorage.getItem('cart')) || {};
    const items_count = Object.keys(cart).length;
    const cartHeader = document.getElementById('header-cart');
    const icon = cartHeader.querySelector('ion-icon');

    const existingBadge = cartHeader.querySelector('.cart-badge');
    if (existingBadge) {
        existingBadge.remove();
        icon.attributes['name'].value = 'cart-outline';
        icon.classList.remove('text-pink-500');
    }

    if (items_count !== 0) {
        icon.attributes['name'].value = 'cart';
        icon.classList.add('text-pink-500');
        cartHeader.innerHTML += `<div id="cart-badge" class="cart-badge h-4 w-4 bg-pink-500 rounded-full absolute top-0 left-1/2 transform -translate-x-6 -translate-y-0.5 text-xs text-white flex items-center justify-center">${items_count}</div>`;
    }

    const hoverBox = document.getElementById('cart-hover-ul');
    if (Object.keys(cart).length > 0) {
        hoverBox.innerHTML = '';
        for (const [key, value] of Object.entries(cart)) {
            hoverBox.innerHTML += `
                        <li id="cart-hover-${key}" class='flex items-center justify-between py-1 hover:bg-gray-50'>
                                <div class="flex text-sm w-1/2 items-center gap-1">
                                    <div class="w-[40px] h-[40px]">
                                        <img src="${rootUrl}/${value.image}" alt="x" class="w-full h-full object-cover rounded-md">
                                    </div>
                                    <a class="hover:text-pink-500 duration-500" href="${rootUrl}/product/${key}">${value.short_name}</a>
                                </div>

                                <div class='border-[1px] border-gray-300 flex w-fit justify-center items-center px-0.5 rounded-md py-0.5'>
                                    <button
                                            data-id="${key}"
                                            data-stock="${value.stock}"
                                            data-parent="#cart-hover-${key}"
                                            onclick="handleIncreaseDecreaseCartPage(this, 'decrease' , 'cart-hover')"
                                            class="decrease cursor-pointer select-none w-6 hover:bg-gray-100 duration-500">-</button>
                                    <label>
                                        <input id="cart-hover-input-${key}"
                                               type='number'
                                               class='appearance-none custom-number-input outline-none w-6 text-center'
                                               value="${value.quantity}" />
                                    </label>
                                    <button
                                            data-id="${key}"
                                            data-stock="${value.stock}"
                                            data-parent="#cart-hover-${key}"
                                            onclick="handleIncreaseDecreaseCartPage(this, 'increase' , 'cart-hover')"
                                            class="increase cursor-pointer w-6 select-none hover:bg-gray-100 duration-500">+</button>
                                </div>
                                <p class="w-1/4 text-sm" id="cart-hover-price-${key}">Rs. ${value.price * value.quantity}</p>
                            </li>
                    `;
        }
    } else {
        hoverBox.innerHTML = '';
        hoverBox.innerHTML += `
                        <li class='flex items-center justify-between py-1 hover:bg-gray-50'>
                            <p class="text-sm text-center w-full">Your cart is empty</p>
                        </li>
                    `;
    }

}

function toggleCart(button) {
    const id = button.getAttribute('data-id');
    const short_name = button.getAttribute('data-short_name');
    const full_name = button.getAttribute('data-full_name');
    const price = parseFloat(button.getAttribute('data-price'));
    const description = button.getAttribute('data-description');
    const image = button.getAttribute('data-image');
    const stock = parseInt(button.getAttribute('data-stock'));
    const category = button.getAttribute('data-category');

    let cart = JSON.parse(localStorage.getItem('cart')) || {};

    if (cart[id]) {
        removeFromCart(id);
        button.textContent = 'Add to Cart';
        button.classList.remove('bg-pink-800');
        button.classList.add('bg-pink-500');
    } else {
        cart[id] = {
            short_name,
            full_name,
            price,
            description,
            image,
            stock,
            category,
            quantity: 1
        };
        localStorage.setItem('cart', JSON.stringify(cart));
        button.textContent = 'Undo Cart';
        button.classList.remove('bg-pink-500');
        button.classList.add('bg-pink-800');
    }
    updateCart();
}


function removeFromCart(id) {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};

    if (cart[id]) {
        delete cart[id];
        localStorage.setItem('cart', JSON.stringify(cart));
    }
    updateCart();
}

function initialCartHandler() {
    let cart = JSON.parse(localStorage.getItem('cart')) || null
    if (cart) {
        for (let key in cart) {
            let button = $(`#${key}`);
            if (button) {
                button.text('Undo Cart');
                button.removeClass('bg-pink-500');
                button.addClass('bg-pink-800');
            }
        }
    }

}

function handleCartAddRemove(button, action) {

    const id = button.getAttribute('data-id');
    const short_name = button.getAttribute('data-short_name');
    const full_name = button.getAttribute('data-full_name');
    const price = parseFloat(button.getAttribute('data-price'));
    const description = button.getAttribute('data-description');
    const image = button.getAttribute('data-image');
    const stock = parseInt(button.getAttribute('data-stock'));
    const category = button.getAttribute('data-category');

    const inputElement = document.getElementById('productDetailInput');
    let quantity = parseInt(inputElement.value) || 0;

    let cart = JSON.parse(localStorage.getItem('cart')) || {};

    if (action === 'increase') {
        const stock = parseInt(button.getAttribute('data-stock'));
        if (quantity >= stock) {
            $('#productDetailCartInfo').text('Out of stock').css('color', 'red');
            return;
        }
        quantity += 1;
        inputElement.value = quantity;
        if (cart[id]) {
            cart[id].quantity += 1;
        } else {
            cart[id] = {
                short_name,
                full_name,
                price,
                description,
                image,
                stock,
                category,
                quantity: 1
            }
        }
    } else if (action === 'decrease') {
        if (quantity > 0) {
            quantity -= 1;
            inputElement.value = quantity;
            if (cart[id]) {
                if (cart[id].quantity > 1) {
                    cart[id].quantity -= 1;
                } else {
                    delete cart[id];
                }
            }
        }
    }

    if (quantity === 0) {
        $('#productDetailCartInfo').text('Add To Cart').css('color', 'black');
    } else {
        $('#productDetailCartInfo').text('In cart').css('color', 'hotpink');
    }

    localStorage.setItem('cart', JSON.stringify(cart));
    updateCart();
}


function handleIncreaseDecreaseCartPage(button, action, view) {
    const id = button.getAttribute('data-id');
    const stock = parseInt(button.getAttribute('data-stock'));
    let element = $(`#cart-view-input-${id}`);
    if (view === 'cart-hover') {
        element = $(`#cart-hover-input-${id}`);
    }

    const cart = JSON.parse(localStorage.getItem('cart')) || {};

    let quantity = parseInt(element.val()) || 0;

    if (action === 'increase') {
        if (quantity >= stock) {
            element.addClass('text-red-500');
            return 0;
        }

        quantity += 1;
        element.val(quantity);

        if (cart[id]) {
            cart[id].quantity = quantity;
        }


    } else if (action === 'decrease') {
        element.removeClass('text-red-500');
        if (quantity > 0) {
            quantity -= 1;
            element.val(quantity);

            if (cart[id]) {
                cart[id].quantity = quantity;
                if (quantity === 0) {
                    delete cart[id];

                    const parent = $(button).attr('data-parent');
                    $(parent).remove();
                    if (view === 'cart-hover') {
                        $(`#cart-view-${id}`).remove();
                        cleanupUI(id, quantity);
                    }
                }
            }
        }
    }

    if (view === 'cart-hover') {
        try {
            $(`#cart-view-input-${id}`).val(quantity);
        } catch (e) {
            console.log(e);
        }

        try {
            $(`#productDetailInput`).val(quantity);
            if (quantity === 0) {
                $('#productDetailCartInfo').text('Add To Cart').css('color', 'black');
            }
            if (stock === quantity) {
                $('#productDetailCartInfo').text('Out of stock').css('color', 'red');
            } else if (quantity > 0) {
                $('#productDetailCartInfo').text('In cart').css('color', 'hotpink');
            }
        } catch (e) {
            console.log(e);
        }
    }

    localStorage.setItem('cart', JSON.stringify(cart));
    updateCart();
    cartTotalCalculation(id);

}


function cartTotalCalculation(id=null) {
    updateCartItemCount();
    const cart = JSON.parse(localStorage.getItem('cart')) || {};
    const prices = Object.keys(cart).map(key => cart[key].price * cart[key].quantity);
    const shipping_cost_list = {
        'Kathmandu': 100,
        'Pokhara': 150,
        'Chitwan': 200,
        'Lalitpur': 120,
        'Bhaktapur': 130,
    }
    const location = localStorage.getItem('selectedCity') || null
    if (location === null) {
        $('#cart-shipping-cost').text('Please select a location');
        $('#cart-grand-total').text('Please select a location');
        return;
    } else {
        $('#cart-sub-total').text(`Rs. 0.00`);
        $('#cart-shipping-cost').text(`Rs. 0.00`);
        $('#cart-grand-total').text(`Rs. 0.00`);
    }
    if (Object.keys(cart).length === 0) {
        return;
    }
    const sub_total = prices.reduce((acc, curr) => acc + curr, 0);
    const shipping_cost = location ? shipping_cost_list[location] : 0;
    const grand_total = sub_total + shipping_cost;

    $('#cart-sub-total').text(`Rs. ${sub_total}`);
    $('#cart-shipping-cost').text(`Rs. ${shipping_cost}`);
    $('#cart-grand-total').text(`Rs. ${grand_total}`);
    $('#checkout_price').prop('value', grand_total);
    $('#cart-data').prop('value', JSON.stringify(cart));
    console.log('cart-data', JSON.stringify(cart));
    if (id) {
        $(`#total-price-${id}`).text(`Rs. ${cart[id].price * cart[id].quantity}`);
    }
}


function updateCartItemCount() {
    const cart = JSON.parse(localStorage.getItem('cart')) || {};
    const items_count = Object.keys(cart).length;
    const noItemsInfo = $('#noItemsInfo');
    // This shouldn't be here but for now it's fine
    const checkoutButton = $('#checkout-button');
    console.log(checkoutButton)
    if (items_count === 0) {
        console.log('No items')
        noItemsInfo.removeClass('hidden');
        checkoutButton.prop('disabled', true).css('cursor', 'not-allowed');
    } else {
        console.log('Items')
        noItemsInfo.addClass('hidden');
        checkoutButton.prop('disabled', false);
    }

    $('#cart-item-count').text(`Your Cart (${items_count} items)`)
}


function productDetailOnLoad(id) {
    const cart = JSON.parse(localStorage.getItem('cart')) || {};
    const quantity = cart[id] ? cart[id].quantity : 0;
    if (quantity > 0) {
        $('#productDetailCartInfo').text('In cart').css('color', 'hotpink');
    }

    $('#productDetailInput').val(quantity);
}


function cleanupUI(id, quantity) {
    const element = $(`#${id}`);
    const productDetailInput = $('#productDetailInput')
    console.log('clicked')
    try {
        element.text('Add to Cart');
        element.removeClass('bg-pink-800');
        element.addClass('bg-pink-500');

    } catch (e) {
        console.log(e);
    }
}