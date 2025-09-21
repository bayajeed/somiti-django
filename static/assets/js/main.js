// ================================
        // TOPBAR FUNCTIONALITY
        // ================================
        const topbar = document.querySelector('.topbar');
        const navbar = document.querySelector('.navbar-custom');
        const topbarClose = document.getElementById('topbarClose');
        let topbarClosed = false; // Changed: Don't check localStorage, always start with topbar visible
        let lastScrollTop = 0;
        let isTopbarVisible = true; // Changed: Always start with topbar visible

        // Topbar close button functionality
        topbarClose.addEventListener('click', function() {
            hideTopbar();
            topbarClosed = true; // Only set for current session, don't save to localStorage
        });

        function hideTopbar() {
            topbar.classList.add('hidden');
            navbar.classList.add('topbar-hidden');
            document.body.style.paddingTop = '80px';
            isTopbarVisible = false;
        }

        function showTopbar() {
            topbar.classList.remove('hidden');
            navbar.classList.remove('topbar-hidden');
            document.body.style.paddingTop = '120px';
            isTopbarVisible = true;
        }

        // ================================
        // SCROLL FUNCTIONALITY
        // ================================
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            // Hide topbar on scroll down (if not already closed)
            if (!topbarClosed) {
                if (scrollTop > lastScrollTop && scrollTop > 100) {
                    // Scrolling down
                    if (isTopbarVisible) {
                        hideTopbar();
                    }
                } else if (scrollTop < lastScrollTop && scrollTop < 50) {
                    // Scrolling up to top
                    if (!isTopbarVisible) {
                        showTopbar();
                    }
                }
            }

            // Add blur effect to navbar after scrolling 500px
            if (scrollTop > 500) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }

            lastScrollTop = scrollTop;
        });

        // ================================
        // THEME FUNCTIONALITY
        // ================================
        const themeToggle = document.getElementById('themeToggle');
        const themeIcon = document.getElementById('themeIcon');
        const htmlElement = document.documentElement;

        // Get saved theme or default to dark
        const savedTheme = localStorage.getItem('theme') || 'dark';
        
        // Set initial theme
        htmlElement.setAttribute('data-bs-theme', savedTheme);
        updateThemeIcon(savedTheme);

        // Theme toggle event listener
        themeToggle.addEventListener('click', function() {
            const currentTheme = htmlElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            htmlElement.setAttribute('data-bs-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        });

        // Update theme icon based on current theme
        function updateThemeIcon(theme) {
            if (theme === 'dark') {
                themeIcon.className = 'bi bi-moon-stars-fill';
                themeToggle.title = 'Switch to Light Mode';
            } else {
                themeIcon.className = 'bi bi-sun-fill';
                themeToggle.title = 'Switch to Dark Mode';
            }
        }

        // ================================
        // NAVIGATION FUNCTIONALITY
        // ================================
        
        // Active nav link highlighting
        const navLinks = document.querySelectorAll('.nav-link:not(.dropdown-toggle)');
        
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                // Remove active class from all nav links
                navLinks.forEach(navLink => navLink.classList.remove('active'));
                // Add active class to clicked link
                this.classList.add('active');
            });
        });

        // Smooth scroll for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    const offset = isTopbarVisible ? 120 : 80;
                    window.scrollTo({
                        top: target.offsetTop - offset,
                        behavior: 'smooth'
                    });
                }
            });
        });

        // ================================
        // MOBILE MENU FUNCTIONALITY
        // ================================
        const navbarCollapse = document.getElementById('navbarNav');
        const navbarToggler = document.querySelector('.navbar-toggler');
        
        // Close mobile menu when clicking on a non-dropdown link
        document.querySelectorAll('.nav-link:not(.dropdown-toggle)').forEach(link => {
            link.addEventListener('click', () => {
                if (navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            });
        });

        // Handle dropdown clicks on mobile
        document.querySelectorAll('.dropdown-item').forEach(item => {
            item.addEventListener('click', (e) => {
                // Close mobile menu after dropdown item click
                setTimeout(() => {
                    if (navbarCollapse.classList.contains('show') && window.innerWidth < 992) {
                        navbarToggler.click();
                    }
                }, 100);
            });
        });

        // ================================
        // IMPROVED MOBILE DROPDOWN HANDLING
        // ================================
        function initializeMobileDropdowns() {
            const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
            
            dropdownToggles.forEach(toggle => {
                // Remove any existing listeners first
                const newToggle = toggle.cloneNode(true);
                toggle.parentNode.replaceChild(newToggle, toggle);
            });

            // Re-select after cloning
            document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
                toggle.addEventListener('click', handleDropdownClick);
            });
        }

        function handleDropdownClick(e) {
            console.log('Dropdown clicked, window width:', window.innerWidth); // Debug log
            
            if (window.innerWidth < 992) {
                e.preventDefault();
                e.stopPropagation();
                
                const dropdownMenu = this.nextElementSibling;
                const isCurrentlyOpen = dropdownMenu.classList.contains('show');
                
                console.log('Dropdown menu:', dropdownMenu); // Debug log
                console.log('Currently open:', isCurrentlyOpen); // Debug log
                
                // Close all other dropdowns first
                document.querySelectorAll('.dropdown-menu').forEach(menu => {
                    if (menu !== dropdownMenu) {
                        menu.classList.remove('show');
                        menu.previousElementSibling.setAttribute('aria-expanded', 'false');
                    }
                });
                
                // Toggle current dropdown
                if (isCurrentlyOpen) {
                    dropdownMenu.classList.remove('show');
                    this.setAttribute('aria-expanded', 'false');
                    console.log('Dropdown closed'); // Debug log
                } else {
                    dropdownMenu.classList.add('show');
                    this.setAttribute('aria-expanded', 'true');
                    console.log('Dropdown opened'); // Debug log
                }
            } else {
                // Let Bootstrap handle desktop dropdowns
                console.log('Desktop mode - letting Bootstrap handle'); // Debug log
            }
        }

        // Initialize mobile dropdowns when page loads
        document.addEventListener('DOMContentLoaded', function() {
            console.log('DOM loaded, initializing dropdowns'); // Debug log
            initializeMobileDropdowns();
        });

        // Also initialize immediately in case DOM is already loaded
        initializeMobileDropdowns();

        // Reinitialize on window resize
        window.addEventListener('resize', function() {
            console.log('Window resized to:', window.innerWidth); // Debug log
            
            if (window.innerWidth >= 992) {
                // Desktop mode - remove manual show classes and let Bootstrap handle
                document.querySelectorAll('.dropdown-menu').forEach(menu => {
                    menu.classList.remove('show');
                });
                document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
                    toggle.setAttribute('aria-expanded', 'false');
                });
                console.log('Reset to desktop mode'); // Debug log
            }
        });

        // Close dropdowns when clicking outside on mobile
        document.addEventListener('click', function(e) {
            if (window.innerWidth < 992 && !e.target.closest('.dropdown')) {
                console.log('Clicked outside dropdown, closing all'); // Debug log
                document.querySelectorAll('.dropdown-menu').forEach(menu => {
                    menu.classList.remove('show');
                });
                document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
                    toggle.setAttribute('aria-expanded', 'false');
                });
            }
        });

        // Prevent dropdown menu from closing when clicking inside
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            menu.addEventListener('click', function(e) {
                e.stopPropagation();
                console.log('Clicked inside dropdown menu'); // Debug log
            });
        });

        // Additional: Disable Bootstrap's dropdown behavior on mobile
        window.addEventListener('resize', function() {
            if (window.innerWidth < 992) {
                // Disable Bootstrap dropdowns on mobile
                document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
                    toggle.removeAttribute('data-bs-toggle');
                });
            } else {
                // Re-enable Bootstrap dropdowns on desktop
                document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
                    toggle.setAttribute('data-bs-toggle', 'dropdown');
                });
            }
        });

        // Initial setup for mobile/desktop
        if (window.innerWidth < 992) {
            document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
                toggle.removeAttribute('data-bs-toggle');
            });
        }