document.addEventListener('DOMContentLoaded', () => {
    const categorySelect = document.getElementById('category');
    const subCategoryDiv = document.getElementById('subCategoryDiv');
    const subCategorySelect = document.getElementById('sub_category');
    const form = document.getElementById('quizForm');

    // Show/hide subcategory dropdown
    categorySelect.addEventListener('change', () => {
        if (categorySelect.value === 'Programming') {
            subCategoryDiv.classList.remove('hidden');
            subCategorySelect.setAttribute('required', '');
        } else {
            subCategoryDiv.classList.add('hidden');
            subCategorySelect.removeAttribute('required');
            subCategorySelect.value = '';
        }
    });

    // Handle form submission
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const category = categorySelect.value;
        const subCategory = subCategorySelect.value || category;
        console.log('Submitting:', { category, subCategory });

        fetch('/start_quiz', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({
                'category': category,
                'sub_category': subCategory
            })
        })
        .then(response => {
            if (!response.ok) throw new Error(`Request failed with status ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log('Response:', data);
            if (data.redirect) {
                window.location.href = data.redirect;
            } else {
                alert('Error: ' + (data.error || 'Failed to start quiz'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error starting quiz: ' + error.message);
        });
    });
});