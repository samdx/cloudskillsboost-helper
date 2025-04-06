// Add event listeners to all collapsible headings
document.querySelectorAll('.collapsible-heading').forEach(heading => {
    heading.addEventListener('click', () => {
        // Toggle the 'collapsed' class
        heading.classList.toggle('collapsed');

        // Find the next sibling element (the collapsible content)
        const content = heading.nextElementSibling;
        if (content) {
            // Toggle the display property
            content.style.display = content.style.display === 'none' ? 'block' : 'none';
        }
    });
});

// Initialize collapsible sections as collapsed
document.querySelectorAll('.collapsible-content').forEach(content => {
    content.style.display = 'none';
});
