document.addEventListener('DOMContentLoaded', function() {
    // Get all add to cart buttons
    var addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    var removeFromCartButtons = document.querySelectorAll('.remove-from-cart-btn');

    // Add click event listener to each "Add to cart" button
    addToCartButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            var productId = button.dataset.productId;

            // AJAX call to add product to cart
            fetch('/addcart/' + productId, {
                method: 'GET',
            }).then(function(response) {
                // Change button text to "Remove from cart"
                // button.innerText = "Remove from cart";
                // button.className = "remove-from-cart-btn";

                location.reload();
            }).catch(function(error) {
                console.error('Error:', error);
            });
        });
    });

    // Add click event listener to each "Remove from cart" button
    removeFromCartButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            var productId = button.dataset.productId;

            // AJAX call to remove product from cart
            fetch('/removecart/' + productId, {
                method: 'GET',
            }).then(function(response) {
                // Change button text to "Add to cart"
                // button.innerText = "Add to cart";
                // button.className = "add-to-cart-btn";

                location.reload();
            }).catch(function(error) {
                console.error('Error:', error);
            });
        });
    });
});


// Function to submit form and retain page position
function submitForm(event, productId) {
    event.preventDefault();
    
    // Save current scroll position
    var scrollPosition = window.scrollY;

    // Submit the form
    var form = document.getElementById('form_' + productId);
    var formData = new FormData(form);
    fetch(form.action, {
        method: form.method,
        body: formData
    }).then(function(response) {
        // Scroll back to the saved position after the action completes
        window.scrollTo(0, scrollPosition);
        // Reload the page after successful form submission
        location.reload();
    }).catch(function(error) {
        console.error('Error:', error);
    });
}


function toggleSearch() {
    var searchIcon = document.getElementById("searchIcon");
    var searchInput = document.getElementById("searchInput");
    
    if (searchIcon.style.display === "inline") {
        searchIcon.style.display = "none";
        searchInput.style.display = "inline";
    } else {
        searchIcon.style.display = "inline";
        searchInput.style.display = "none";
    }
}