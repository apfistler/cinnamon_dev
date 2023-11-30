function init() {
    var menuVisibility = document.getElementById("menu_visibility");
    var menu = document.getElementById("menu");
    var content = document.getElementById("content");
    var menuDisplayed = false;

    menu.addEventListener("click", function (event) {
        var target = event.target;
        if (target.classList.contains("parent")) {
            var childMenu = target.nextElementSibling;
            if (childMenu && childMenu.classList.contains("child-menu")) {
                childMenu.classList.toggle("hidden");
                target.classList.toggle("active");
            }
        }
    });

    // Flag to track whether the page has been loaded
    var pageLoaded = false;

    // Function to hide the menu only on page load
    function hideMenuOnLoad() {
	if ( menuDisplayed == false ) {
            if (!pageLoaded && window.innerWidth < 1280) {
                hideMenu();
            } else {
                showMenu();
            }
            menuDisplayed = true;
        }

        pageLoaded = true; // Set the flag to true after the first load
    }

    // Check screen width on page load
    hideMenuOnLoad();

    // Check screen width when the window is resized
    window.addEventListener("resize", function () {
        hideMenuOnLoad(); // Call hideMenuOnLoad on window resize
    });

    function hideMenu() {
        menu.style.display = "none";
        menuVisibility.querySelector(".hamburger-icon").style.display = "inline";
        menuVisibility.querySelector(".close-icon").style.display = "none";
        content.classList.add("hidden-menu");
        content.style.marginRight = "0";
        document.body.classList.remove("visible");
    }

    function showMenu() {
        menu.style.display = "block";
        menuVisibility.querySelector(".hamburger-icon").style.display = "none";
        menuVisibility.querySelector(".close-icon").style.display = "inline";
        content.classList.remove("hidden-menu");
        content.style.marginRight = menu.offsetWidth + "px";
        document.body.classList.add("visible");
    }

    menuVisibility.addEventListener("click", function (event) {
        event.preventDefault();
        if (menu.style.display === "none" || menu.style.display === "") {
            showMenu();
        } else {
            hideMenu();
        }
    });

    const messageBox = document.querySelector('.message-box');
    const closeButton = document.querySelector('.close-btn');

    messageBox.style.display = "flex";

    closeButton.addEventListener('click', function () {
        messageBox.style.display = "none";
    });
}

document.addEventListener("DOMContentLoaded", init);

