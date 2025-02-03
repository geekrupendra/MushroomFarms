// Handle quantity changes in cart
function updateQuantity(productId, change) {
    const quantityInput = document.querySelector(`#quantity-${productId}`);
    let newQuantity = parseInt(quantityInput.value) + change;
    
    if (newQuantity < 1) newQuantity = 1;
    if (newQuantity > 99) newQuantity = 99;
    
    quantityInput.value = newQuantity;
    updateCartTotal();
}

// Update cart total
function updateCartTotal() {
    const items = document.querySelectorAll('.cart-item');
    let total = 0;
    
    items.forEach(item => {
        const price = parseFloat(item.querySelector('.price').dataset.price);
        const quantity = parseInt(item.querySelector('.quantity-input').value);
        total += price * quantity;
    });
    
    document.querySelector('#cart-total').textContent = total.toFixed(2);
}

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});

// Product image gallery
function changeImage(element) {
    document.querySelector('#main-product-image').src = element.src;
}

// Form validation
function validateForm(formId) {
    const form = document.querySelector(`#${formId}`);
    if (!form) return true;

    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// Add to cart animation
function addToCartAnimation(button) {
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-check"></i> Added';
    
    setTimeout(() => {
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-shopping-cart"></i> Add to Cart';
    }, 2000);
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
