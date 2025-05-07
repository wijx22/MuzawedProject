window.onload = function () {
    const categorySelect = document.getElementById('category');
    const agriculturalContainer = document.querySelector('.agricultural');
    const processedContainer = document.querySelector('.processed');
    const industrialContainer = document.querySelector('.industrial');
    const specialContainer = document.querySelector('.special');
    const miscellaneousContainer = document.querySelector('.miscellaneous');

    // Function to show the relevant subcategory container
    function showRelevantSubcategory() {
        const containers = document.querySelectorAll('.agricultural, .processed, .industrial, .special, .miscellaneous');
        // Hide all subcategory containers first
 
        containers.forEach(container => {
            container.style.display = 'none'; // Hide all
            const select = container.querySelector('select');
            select.removeAttribute('name'); // Remove name attribute
        });
        // Show the relevant subcategory container based on selected category
        let selectedSubcategory;
        switch (categorySelect.value) {
            case 'agricultural':
                agriculturalContainer.style.display = 'block';
                selectedSubcategory = agriculturalContainer.querySelector('select');
                selectedSubcategory.setAttribute('name', 'subcategory'); 

                
                break;
            case 'processed':
                processedContainer.style.display = 'block';
                selectedSubcategory = processedContainer.querySelector('select');
                selectedSubcategory.setAttribute('name', 'subcategory'); 

                break;
            case 'industrial':
                industrialContainer.style.display = 'block';
                selectedSubcategory = industrialContainer.querySelector('select');
                selectedSubcategory.setAttribute('name', 'subcategory'); 

                break;
            case 'special':
                specialContainer.style.display = 'block';
                selectedSubcategory = specialContainer.querySelector('select');
                selectedSubcategory.setAttribute('name', 'subcategory'); 

                break;
            case 'miscellaneous':
                miscellaneousContainer.style.display = 'block';
                selectedSubcategory = miscellaneousContainer.querySelector('select');
                selectedSubcategory.setAttribute('name', 'subcategory'); 

                break;
        }
        // Set required attribute on the relevant subcategory select
        if (selectedSubcategory) {
            selectedSubcategory.setAttribute('required', 'required');

        }
        
        
    }

    // Add event listener to category dropdown
    categorySelect.addEventListener('change', function () {
        showRelevantSubcategory();
    });

    // Call the function on page load to set the initial state
    showRelevantSubcategory();
};
