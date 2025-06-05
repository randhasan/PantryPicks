const MAX_INGREDIENTS = 5;
const MAX_CATEGORIES = 5;
const MAX_AREAS = 5;
let selectedIngredients = [];
let selectedCategories = [];
let selectedAreas = [];

// Load ingredients
fetch('/api/ingredients')
    .then(response => response.json())
    .then(ingredients => {
        const select = document.getElementById('ingredient-select');
        ingredients.forEach(ingredient => {
            const option = document.createElement('option');
            option.value = ingredient;
            option.textContent = ingredient;
            select.appendChild(option);
        });
    });

// Load categories
fetch('/api/categories')
    .then(response => response.json())
    .then(categories => {
        const select = document.getElementById('category-select');
        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            select.appendChild(option);
        });
    });

// Load area
fetch('/api/areas')
    .then(response => response.json())
    .then(areas => {
        const select = document.getElementById('area-select');
        areas.forEach(area => {
            const option = document.createElement('option');
            option.value = area;
            option.textContent = area;
            select.appendChild(option);
        });
    });

// Handle ingredient selection
document.getElementById('ingredient-select').addEventListener('change', function() {
    if (!this.value) return;
    if (selectedIngredients.length >= MAX_INGREDIENTS) {
        alert(`Maximum ${MAX_INGREDIENTS} ingredients allowed`);
        this.value = '';
        return;
    }
    if (selectedIngredients.includes(this.value)) {
        alert('Ingredient already selected');
        this.value = '';
        return;
    }

    selectedIngredients.push(this.value);
    updateIngredientTags();
    this.value = '';
});

// handle category selection
document.getElementById('category-select').addEventListener('change', function() {
    if (!this.value) return;
    if (selectedIngredients.length >= MAX_CATEGORIES) {
        alert(`Maximum ${MAX_CATEGORIES} categories allowed`);
        this.value = '';
        return;
    }
    if (selectedIngredients.includes(this.value)) {
        alert('Category already selected');
        this.value = '';
        return;
    }

    selectedCategories.push(this.value);
    updateCategoryTags();
    this.value = '';
});

// handle area selection
document.getElementById('area-select').addEventListener('change', function() {
    if (!this.value) return;
    if (selectedAreas.length >= MAX_AREAS) {
        alert(`Maximum ${MAX_AREAS} areas allowed`);
        this.value = '';
        return;
    }
    if (selectedAreas.includes(this.value)) {
        alert('Area already selected');
        this.value = '';
        return;
    }

    selectedAreas.push(this.value);
    updateAreaTags();
    this.value = '';
});

function updateIngredientTags() {
    const container = document.getElementById('selected-ingredients');
    container.innerHTML = '';
    selectedIngredients.forEach(ingredient => {
        const tag = document.createElement('div');
        tag.className = 'ingredient-tag';
        tag.innerHTML = `
            ${ingredient}
            <span class="remove-ingredient" onclick="removeIngredient('${ingredient}')">✕</span>
        `;
        container.appendChild(tag);
    });
}

function updateCategoryTags() {
    const container = document.getElementById('selected-categories');
    container.innerHTML = '';
    selectedCategories.forEach(category => {
        const tag = document.createElement('div');
        tag.className = 'category-tag';
        tag.innerHTML = `
            ${category}
            <span class="remove-category" onclick="removeCategory('${category}')" style="color: green;">✕</span>
        `;
        container.appendChild(tag);
    });
}

function updateAreaTags() {
    const container = document.getElementById('selected-areas');
    container.innerHTML = '';
    selectedAreas.forEach(area => {
        const tag = document.createElement('div');
        tag.className = 'area-tag';
        tag.innerHTML = `
            ${area}
            <span class="remove-area" onclick="removeArea('${area}')" style="color: red;">✕</span>
        `;
        container.appendChild(tag);
    });
}

function removeIngredient(ingredient) {
    selectedIngredients = selectedIngredients.filter(i => i !== ingredient);
    updateIngredientTags();
}

function removeCategory(category) {
    selectedCategories = selectedCategories.filter(c => c !== category);
    updateCategoryTags();
}

function removeArea(area) {
    selectedAreas = selectedAreas.filter(a => a !== area);
    updateAreaTags();
}

// Handle search
// if no recipes are returned show a warning message
document.getElementById('search-btn').addEventListener('click', function() {
    if (selectedIngredients.length === 0) {
        alert('Please select at least one ingredient');
        return;
    }

    fetch('/api/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            ingredients: selectedIngredients,
            categories: selectedCategories,
            areas: selectedAreas
        })
    })
    .then(response => response.json())
    .then(recipes => {
        const results = document.getElementById('results');
        results.innerHTML = '';
        
        if (!recipes || recipes.length === 0) {
            alert('No recipes found');
            return;
        }

        recipes.forEach(recipe => {
            results.innerHTML += `
                <div class="recipe-card">
                    <img src="${recipe.strMealThumb}" alt="${recipe.strMeal}">
                    <h3>${recipe.strMeal}</h3>
                    <a href="/view_recipe/${recipe.strMeal}"><span class="recipe-link"></span></a>
                </div>
            `;
        });
    });
});