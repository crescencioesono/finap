// Menu configuration object (can be moved to a separate config file if needed)
const menuConfig = {
    items: [
        {
            label: 'Funcionarios',
            submenuId: 'funcionarios-submenu',
            subItems: [
                { label: 'Ver Funcionarios', url: '/official/' } // Hardcoded URL for now
            ]
        },
        {
            label: 'Cursos',
            submenuId: 'cursos-submenu',
            subItems: [
                { label: 'Ver Cursos', url: '/training/' } // Hardcoded URL for now
            ]
        },
        {
            label: 'Códigos de cursos',
            submenuId: 'codigos-submenu',
            subItems: [
                { label: 'Ver Códigos', url: '/batch/' } // Hardcoded URL for now
            ]
        },
        {
            label: 'Usuarios',
            submenuId: 'usuarios-submenu',
            subItems: [
                { label: 'Ver Usuarios', url: '/user/' } // Hardcoded URL for now
            ]
        }
    ],
    logoutUrl: '/logout', // Hardcoded URL for now
    logoutLabel: 'Cerrar Sesión'
};

// Function to generate sidebar HTML
function generateSidebar() {
    const sidebar = document.createElement('aside');
    sidebar.className = 'sidebar';
    sidebar.id = 'sidebar';

    // App Branding
    const branding = document.createElement('div');
    branding.className = 'app-branding';
    const logo = document.createElement('img');
    logo.src = '/static/images/logo.png'; // Hardcoded path for now
    logo.alt = 'App Logo';
    logo.className = 'app-logo';
    branding.appendChild(logo);
    sidebar.appendChild(branding);

    // Navigation
    const nav = document.createElement('nav');
    nav.className = 'sidebar-nav';
    const menuList = document.createElement('ul');
    menuList.className = 'menu-list';

    menuConfig.items.forEach(item => {
        const menuItem = document.createElement('li');
        menuItem.className = 'menu-item';
        const menuButton = document.createElement('button');
        menuButton.className = 'menu-button';
        menuButton.setAttribute('data-submenu', item.submenuId);
        menuButton.textContent = item.label;
        const submenu = document.createElement('ul');
        submenu.className = 'submenu';
        submenu.id = item.submenuId;
        item.subItems.forEach(subItem => {
            const subLi = document.createElement('li');
            const subLink = document.createElement('a');
            subLink.href = subItem.url;
            subLink.textContent = subItem.label;
            subLi.appendChild(subLink);
            submenu.appendChild(subLi);
        });
        menuItem.appendChild(menuButton);
        menuItem.appendChild(submenu);
        menuList.appendChild(menuItem);
    });

    nav.appendChild(menuList);

    // Logout
    const logoutDiv = document.createElement('div');
    logoutDiv.className = 'logout';
    const logoutLink = document.createElement('a');
    logoutLink.href = menuConfig.logoutUrl;
    logoutLink.className = 'logout-link';
    logoutLink.textContent = menuConfig.logoutLabel;
    logoutDiv.appendChild(logoutLink);
    nav.appendChild(logoutDiv);

    sidebar.appendChild(nav);
    return sidebar;
}

// IIFE to initialize sidebar and handle interactivity
(function () {
    // Generate and append sidebar to document
    const sidebar = generateSidebar();
    document.body.insertBefore(sidebar, document.body.firstChild);

    // Hamburger toggle
    const hamburger = document.querySelector('.hamburger');
    if (hamburger) {
        hamburger.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });

        // Close sidebar when clicking outside
        document.addEventListener('click', (e) => {
            if (!sidebar.contains(e.target) && !hamburger.contains(e.target)) {
                sidebar.classList.remove('active');
            }
        });
    }

    // Toggle submenu visibility
    const menuButtons = document.querySelectorAll('.menu-button');
    menuButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault(); // Prevent default button behavior
            const submenuId = button.getAttribute('data-submenu');
            const submenu = document.getElementById(submenuId);
            const isActive = submenu.classList.contains('active');

            // Close all submenus
            document.querySelectorAll('.submenu').forEach(sub => {
                sub.classList.remove('active');
            });
            document.querySelectorAll('.menu-button').forEach(btn => {
                btn.classList.remove('active');
            });

            // Toggle current submenu
            if (!isActive) {
                submenu.classList.add('active');
                button.classList.add('active');
            }
        });
    });
})();