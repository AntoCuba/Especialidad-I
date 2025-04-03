document.addEventListener('DOMContentLoaded', function() {
    const toggleButtons = document.querySelectorAll('.toggle');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const parentLi = this.parentElement;
            
            document.querySelectorAll('li').forEach(item => {
                if (item !== parentLi) {
                    item.classList.remove('submenu-visible');
                    const otherSubmenu = item.querySelector('.submenu');
                    if (otherSubmenu) otherSubmenu.style.maxHeight = null;
                }
            });
            
            parentLi.classList.toggle('submenu-visible');
            const submenu = this.nextElementSibling;
            
            if (parentLi.classList.contains('submenu-visible')) {
                submenu.style.maxHeight = submenu.scrollHeight + 'px';
            } else {
                submenu.style.maxHeight = null;
            }
        });
    });
});