function getCsrfToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === 'csrftoken=') {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    const metaToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    const inputToken = document.querySelector('[name="csrfmiddlewaretoken"]')?.value;
    return cookieValue || metaToken || inputToken || '';
}

function addToCart(productId, quantity = 1, size = '', color = '') {
    const formData = new URLSearchParams();
    formData.append('quantity', quantity);
    if (size) formData.append('size', size);
    if (color) formData.append('color', color);

    return fetch(`/pedidos/agregar/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData.toString()
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Producto añadido al carrito');
        }
        return data;
    });
}

function addToCartDetail(productId) {
    const qtyInput = document.getElementById('product-quantity') || document.querySelector('input[type="number"]');
    const qty = qtyInput ? qtyInput.value : 1;
    const sizeSelect = document.getElementById('product-size');
    const colorSelect = document.getElementById('product-color');
    const size = sizeSelect ? sizeSelect.value : '';
    const color = colorSelect ? colorSelect.value : '';

    return addToCart(productId, qty, size, color);
}

function comprarWhatsApp(productName, productPath = '', phone = '573144871445') {
    const qtyInput = document.getElementById('product-quantity') || document.querySelector('input[type="number"]');
    const qty = qtyInput ? qtyInput.value : 1;
    const sizeSelect = document.getElementById('product-size');
    const colorSelect = document.getElementById('product-color');
    const size = sizeSelect ? sizeSelect.value : 'No especificada';
    const color = colorSelect ? colorSelect.value : 'No especificado';
    const name = productName || document.querySelector('.product-title')?.textContent?.trim() || 'Producto';
    const productUrl = productPath ? (window.location.origin + productPath) : window.location.href;
    const message = `Hola KUROVOID, me interesa comprar este producto:\n\n*${name}*\n- Cantidad: ${qty}\n- Talla: ${size}\n- Color: ${color}\n\nEnlace: ${productUrl}`;
    const waUrl = `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;
    window.open(waUrl, '_blank');
}

function updateCartQuantity(productId, quantity) {
    return fetch(`/pedidos/update/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'quantity=' + encodeURIComponent(quantity)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
        return data;
    });
}

function removeFromCart(productId) {
    return fetch(`/pedidos/quitar/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
        return data;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.cart-qty-input').forEach(input => {
        input.addEventListener('change', function() {
            const productId = this.getAttribute('data-id');
            const quantity = this.value;
            if (productId && quantity) {
                updateCartQuantity(productId, quantity);
            }
        });
    });

    document.querySelectorAll('.cart-remove-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.getAttribute('data-id');
            if (productId) {
                removeFromCart(productId);
            }
        });
    });
});
