function openModal(imageUrl) {
    var modal = document.getElementById("cardModal");
    var modalImage = document.getElementById("modalImage");

    modal.style.display = "block";  // Show the modal
    modalImage.src = imageUrl;  // Set the clicked image in the modal
}

function closeModal() {
    var modal = document.getElementById("cardModal");
    modal.style.display = "none";  // Hide the modal
}

document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        closeModal();
    }
});

function fetchCards(url) {
    // Ensure the URL starts with a slash
    if (!url.startsWith('/')) {
        url = '/' + url;
    }

    // Fetch the cards and pagination using AJAX
    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.cards_html && data.pagination_html) {
            document.getElementById('card-container').innerHTML = data.cards_html;
            document.querySelector('.pagination').innerHTML = data.pagination_html;
        } else {
            console.error("Unexpected data format:", data);
        }
    })
    .catch(error => {
        console.error('Error fetching cards:', error);
    });
}

function applySortAndFilters() {
    var sortBy = document.getElementById('sort_by').value;
    var rarityFilter = document.getElementById('rarity_filter').value;
    var inkableFilter = document.getElementById('inkable_filter').value;
    var cardTypeFilter = document.getElementById('card_type_filter').value;
    var colorFilter = document.getElementById('color_filter').value;
    
    var queryString = `?sort_by=${sortBy}&rarity=${rarityFilter}&inkable=${inkableFilter}&card_type=${cardTypeFilter}&color=${colorFilter}`;
    fetchCards(queryString);
}

// Event listeners for sorting and filtering
document.getElementById('sort_by').addEventListener('change', applySortAndFilters);
document.getElementById('rarity_filter').addEventListener('change', applySortAndFilters);
document.getElementById('inkable_filter').addEventListener('change', applySortAndFilters);
document.getElementById('card_type_filter').addEventListener('change', applySortAndFilters);
document.getElementById('color_filter').addEventListener('change', applySortAndFilters);

// Event listener for pagination links (delegated event handling)
document.addEventListener('click', function(event) {
    if (event.target.matches('.pagination a')) {
        event.preventDefault();
        var url = event.target.getAttribute('href');
        fetchCards(url);
    }
});

// Call applySortAndFilters on page load to initialize the view
document.addEventListener('DOMContentLoaded', applySortAndFilters);
