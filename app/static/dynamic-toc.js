// Dynamic Table of Contents for base.html
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems);

    // Generate TOC dynamically based on h2 headings in contents.html
    const tocContainer = document.querySelector('.toc-table .toc-dynamic'); // Updated selector
    const headings = document.querySelectorAll('.container h2');
    headings.forEach(heading => {
        const id = heading.id || heading.textContent.trim().replace(/\s+/g, '-').toLowerCase();
        heading.id = id; // Ensure the heading has an ID
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = `#${id}`;
        a.className = 'toc-link'; // Add class for styling
        a.textContent = heading.textContent;
        li.appendChild(a);
        tocContainer.appendChild(li);
    });
});
