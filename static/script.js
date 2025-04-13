// Add event listeners to all collapsible headings
document.querySelectorAll('.collapsible-heading').forEach(heading => {
    heading.addEventListener('click', () => {
        // Find the next sibling element (the collapsible content)
        const content = heading.nextElementSibling;

        if (content) {
            if (content.classList.contains('expanded')) {
                // Collapse the content
                content.style.maxHeight = null; // Reset height
                content.classList.remove('expanded');
            } else {
                // Expand the content
                content.style.maxHeight = content.scrollHeight + 'px'; // Set height to content's scroll height
                content.classList.add('expanded');
            }
        }
    });
});

// Initialize collapsible sections as collapsed
document.querySelectorAll('.collapsible-content').forEach(content => {
    content.style.maxHeight = null; // Reset height
    content.classList.remove('expanded');
});
