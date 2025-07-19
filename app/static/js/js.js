document.addEventListener('DOMContentLoaded', () => {
    const menuButtons = document.querySelectorAll('.menu-button');
    menuButtons.forEach(button => {
        button.addEventListener('click', () => {
            const submenu = button.nextElementSibling;
            submenu.classList.toggle('active');
        });
    });
});