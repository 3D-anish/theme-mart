function createListItem(image_path, product_title, product_link, price, license_name, license_pk, asset_pk) {
    const listItem = document.createElement('li');
    listItem.classList.add('cart_popover_li');

    const mediaDiv = document.createElement('div');
    mediaDiv.classList.add('media');

    const imageLink = document.createElement('a');
    imageLink.href = product_link;

    const image = document.createElement('img');
    image.classList.add('me-3');
    image.alt = 'Asset Preview Image';
    image.src = image_path; // Set image source here (if needed)

    imageLink.appendChild(image);

    const mediaBodyDiv = document.createElement('div');
    mediaBodyDiv.classList.add('media-body');

    const itemNameLink = document.createElement('a');
    itemNameLink.href = product_link;

    const itemNameHeader = document.createElement('h4');
    itemNameHeader.textContent = product_title + `(${license_name})`;

    itemNameLink.appendChild(itemNameHeader);

    const priceHeader = document.createElement('h4');
    const priceSpan = document.createElement('span');
    priceSpan.textContent = '₹ ' + price;

    priceHeader.appendChild(priceSpan);

    mediaBodyDiv.appendChild(itemNameLink);
    mediaBodyDiv.appendChild(priceHeader);

    mediaDiv.appendChild(imageLink);
    mediaDiv.appendChild(mediaBodyDiv);

    const closeDiv = document.createElement('div');
    closeDiv.classList.add('close-circle');

    const closeLink = document.createElement('a');
    closeLink.href = `javascript:delete_asset_from_cart(${asset_pk})`;

    const closeIcon = document.createElement('i');
    closeIcon.classList.add('fa', 'fa-times'); // Assuming you have Font Awesome included
    closeIcon.setAttribute('aria-hidden', 'true');

    closeLink.appendChild(closeIcon);
    closeDiv.appendChild(closeLink);

    listItem.appendChild(mediaDiv);
    listItem.appendChild(closeDiv);

    return listItem;
}

function create_view_cart_li() {
    // <li>
    //   <div class="buttons"><a href="{% url 'main:cart' %}" class="view-cart">view cart</a></div>
    // </li>
    const listItem = document.createElement('li');
    const itemNameLink = document.createElement('a');
    itemNameLink.href = '/cart/';
    itemNameLink.classList.add('view-cart');
    itemNameLink.textContent = 'view cart';
    const mediaBodyDiv = document.createElement('div');
    mediaBodyDiv.classList.add('buttons');
    mediaBodyDiv.appendChild(itemNameLink);
    listItem.appendChild(mediaBodyDiv);
    return listItem;

}

function create_subtotal_cart_li(subtotal) {
    // <li>
    //     <div class="total">
    //         <h5>subtotal : <span>$299.00</span></h5>
    //     </div>
    // </li>
    const listItem = document.createElement('li');

    const mediaBodyDiv = document.createElement('div');
    mediaBodyDiv.classList.add('total');
    const subtotal_h5 = document.createElement('h5');
    subtotal_h5.textContent = 'subtotal : '
    const subtotal_span = document.createElement('span');
    subtotal_span.textContent = `₹${subtotal}`;
    subtotal_h5.appendChild(subtotal_span);
    mediaBodyDiv.appendChild(subtotal_h5);
    listItem.appendChild(mediaBodyDiv);
    return listItem
}

function get_tbody_tr(image_path, product_title, product_link, price, license_name, license_pk, asset_pk) {
    const newRow = document.createElement('tr');

    const imageCell = document.createElement('td');
    const imageLink = document.createElement('a');
    imageLink.href = product_link;
    const image = document.createElement('img');
    image.src = image_path;
    image.alt = 'Asset Preview Image';
    imageLink.appendChild(image);
    imageCell.appendChild(imageLink);

    const nameCell = document.createElement('td');
    const nameLink = document.createElement('a');
    nameLink.href = product_link;
    nameLink.textContent = product_title;
    nameCell.appendChild(nameLink);

    const licenseCell = document.createElement('td');
    licenseCell.textContent = license_name;

    const priceCell = document.createElement('td');
    const priceHeader = document.createElement('h2');
    priceHeader.classList.add('td-color');
    priceHeader.textContent = `₹ ${price}`;
    priceCell.appendChild(priceHeader);

    const actionCell = document.createElement('td');
    const actionLink = document.createElement('a');
    actionLink.href = `javascript:delete_asset_from_cart(${asset_pk})`;
    actionLink.classList.add('icon');
    const closeIcon = document.createElement('i');
    closeIcon.classList.add('ti-close'); // Replace with your icon class
    actionLink.appendChild(closeIcon);
    actionCell.appendChild(actionLink);

    newRow.appendChild(imageCell);
    newRow.appendChild(nameCell);
    newRow.appendChild(licenseCell);
    newRow.appendChild(priceCell);
    newRow.appendChild(actionCell);

    return newRow
}

function getCookie(name) {
    const cookieArray = document.cookie.split(';');

    for (let i = 0; i < cookieArray.length; i++) {
        let cookie = cookieArray[i].trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }

    return null;
}

function create_checkout_form(cart) {
    const form = document.createElement('form');
    form.style.display = 'inline';
    form.action = "/orders/create/";
    form.method = 'post';

    // Create CSRF token input (replace with your CSRF implementation)
    const csrfToken = document.createElement('input');
    csrfToken.type = 'hidden';
    csrfToken.name = 'csrfmiddlewaretoken';
    csrfToken.value = getCookie('csrftoken');
    form.appendChild(csrfToken);

    // Create the select element
    const select = document.createElement('select');
    select.name = 'assets';
    select.id = 'assets';
    select.multiple = true;
    select.hidden = true;

    for (cartitem in cart) {
        const opt = document.createElement('option');
        opt.value = `${cartitem}_${cart[cartitem][5]}`;
        opt.text = `${cartitem}`;
        opt.selected = true; // Pre-select the option
        select.appendChild(opt);
    }

    form.appendChild(select);

    // Create the submit button
    const submitButton = document.createElement('button');
    submitButton.type = 'submit';
    submitButton.classList.add('btn', 'btn-solid');
    submitButton.textContent = 'Check Out';
    form.appendChild(submitButton);
    return form;
}

function update_Popover_cart() {
    let cart_ul = document.getElementById('cart_popover');
    let all_cart_li = document.querySelectorAll('.cart_popover_li')

    // for(let i = 0;i < all_cart_li.length; i++){
    //     if(all_cart_li[i]){
    //         all_cart_li[i].remove()
    //     }
    // }

    cart_ul.textContent = '';


    cart = JSON.parse(localStorage.getItem('cart'));
    let cart_length = 0
    let subtotal = 0
    for (cartitem in cart) {
        cart_length += 1;
        subtotal += Number(cart[cartitem][3]);
        const newItem = createListItem(cart[cartitem][0], cart[cartitem][1], cart[cartitem][2], cart[cartitem][3], cart[cartitem][4], cart[cartitem][5], cartitem);
        cart_ul.appendChild(newItem);
    }
    cart_ul.appendChild(create_subtotal_cart_li(subtotal))
    cart_ul.appendChild(create_view_cart_li())
    cart_qty_cls = document.getElementsByClassName('cart_qty_cls')[0].textContent = cart_length;
}

function update_cart_page_cart_body() {
    let cart = JSON.parse(localStorage.getItem('cart'));
    let tbody = document.getElementById('cart_page_cart_table_body');
    tbody.innerHTML = '';
    cart_page_assets_select_tag = document.getElementById('assets');
    if (cart_page_assets_select_tag){
        cart_page_assets_select_tag.innerHTML = '';
    }
    let subtotal = 0;
    let gst = 0;
    for (cartitem in cart) {
        subtotal += Number(cart[cartitem][3]);
        gst += .18 * Number(cart[cartitem][3]);
        const newItem = get_tbody_tr(cart[cartitem][0], cart[cartitem][1], cart[cartitem][2], cart[cartitem][3], cart[cartitem][4], cart[cartitem][5], cartitem);
        tbody.appendChild(newItem);
    }
    chechout_form_span_container = document.getElementById('chechout_form_span_container');
    if (chechout_form_span_container) {
        chechout_form_span_container.innerHTML = ''
        let form = create_checkout_form(cart);
        chechout_form_span_container.appendChild(form);
    }
    cart_page_subtotal = document.getElementById('cart_page_subtotal').textContent = `₹ ${subtotal.toFixed(2)}`;
    cart_page_tax = document.getElementById('cart_page_tax').textContent = `₹ ${gst.toFixed(2)}`;
    cart_page_total_price = document.getElementById('cart_page_total_price').textContent = `₹ ${(subtotal + gst).toFixed(2)}`;
}

function add_to_cart(e) {
    if (localStorage.getItem('cart') == null) {
        var cart = {};
    }
    else {
        cart = JSON.parse(localStorage.getItem('cart'));
    }
    let id = e.id;
    let asset_details = String(id).split('@_@')
    let asset_pk = asset_details[0]
    let product_title = asset_details[1]
    let product_link = asset_details[2]
    let image_path = asset_details[3]
    let price = asset_details[4]
    let license_name = asset_details[5]
    let license_pk = asset_details[6]
    if (cart[asset_pk] == undefined) {
        cart[asset_pk] = [image_path, product_title, product_link, price, license_name, license_pk];
        localStorage.setItem('cart', JSON.stringify(cart));
        update_Popover_cart();
        $.notify({
            icon: '',
            title: '',
            message: 'Asset added to the cart'
        }, {
            element: 'body',
            position: null,
            type: "text-white bg-success",
            allow_dismiss: true,
            newest_on_top: true,
            showProgressbar: true,
            placement: {
                from: "top",
                align: "right"
            },
            offset: 20,
            spacing: 10,
            z_index: 1031,
            delay: 5000,
            animate: {
                enter: 'animated fadeInDown',
                exit: 'animated fadeOutUp'
            },
            icon_type: 'class',
            template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                '<button type="button" aria-hidden="true" class="btn-close" data-notify="dismiss"></button>' +
                '<span data-notify="icon"></span> ' +
                '<span data-notify="title"> {1} </span> ' +
                '<span data-notify="message"> {2}</span>' +
                '<div class="progress" data-notify="progressbar">' +
                '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                '</div>' +
                '<a href="{3}" target="{4}" data-notify="url"></a>' +
                '</div>'
        });
    } else {
        $.notify({
            icon: '',
            title: '',
            message: 'Asset already in the cart'
        }, {
            element: 'body',
            position: null,
            type: "text-dark bg-warning",
            allow_dismiss: true,
            newest_on_top: true,
            showProgressbar: true,
            placement: {
                from: "top",
                align: "right"
            },
            offset: 20,
            spacing: 10,
            z_index: 1031,
            delay: 5000,
            animate: {
                enter: 'animated fadeInDown',
                exit: 'animated fadeOutUp'
            },
            icon_type: 'class',
            template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                '<button type="button" aria-hidden="true" class="btn-close" data-notify="dismiss"></button>' +
                '<span data-notify="icon"></span> ' +
                '<span data-notify="title"> {1} </span> ' +
                '<span data-notify="message"> {2}</span>' +
                '<div class="progress" data-notify="progressbar">' +
                '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                '</div>' +
                '<a href="{3}" target="{4}" data-notify="url"></a>' +
                '</div>'
        });
    }
}

function delete_asset_from_cart(id) {
    if (localStorage.getItem('cart') == null) {
        var cart = {};
    }
    else {
        cart = JSON.parse(localStorage.getItem('cart'));
    }
    if (cart[id] != undefined) {
        delete cart[id];
        localStorage.setItem('cart', JSON.stringify(cart));
        update_Popover_cart();
        if(window.location.pathname == '/cart/'){
            update_cart_page_cart_body();
        }
        $.notify({
            icon: '',
            title: '',
            message: 'Asset removed from the cart'
        }, {
            element: 'body',
            position: null,
            type: "text-dark bg-warning",
            allow_dismiss: true,
            newest_on_top: true,
            showProgressbar: true,
            placement: {
                from: "top",
                align: "right"
            },
            offset: 20,
            spacing: 10,
            z_index: 1031,
            delay: 5000,
            animate: {
                enter: 'animated fadeInDown',
                exit: 'animated fadeOutUp'
            },
            icon_type: 'class',
            template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                '<button type="button" aria-hidden="true" class="btn-close" data-notify="dismiss"></button>' +
                '<span data-notify="icon"></span> ' +
                '<span data-notify="title"> {1} </span> ' +
                '<span data-notify="message"> {2}</span>' +
                '<div class="progress" data-notify="progressbar">' +
                '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                '</div>' +
                '<a href="{3}" target="{4}" data-notify="url"></a>' +
                '</div>'
        });
    }
}

function empty_cart() {
    if (localStorage.getItem('cart') == null) {
        var cart = {};
    }
    else {
        var cart = {};
    }
    localStorage.setItem('cart', JSON.stringify(cart));
    update_cart_page_cart_body();
    update_Popover_cart();
}