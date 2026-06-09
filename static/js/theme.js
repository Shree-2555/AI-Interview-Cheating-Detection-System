document.addEventListener("DOMContentLoaded", function () {

    const toggleBtn = document.getElementById("themeToggle");

    // Apply saved theme on load
    if (localStorage.getItem("theme") === "light") {
        document.body.classList.add("light-mode");
    }

    if (toggleBtn) {
        updateText();

        toggleBtn.addEventListener("click", function () {
            document.body.classList.toggle("light-mode");

            if (document.body.classList.contains("light-mode")) {
                localStorage.setItem("theme", "light");
            } else {
                localStorage.setItem("theme", "dark");
            }

            updateText();
        });
    }

    function updateText() {
        if (!toggleBtn) return;

        if (document.body.classList.contains("light-mode")) {
            toggleBtn.innerText = "🌞 Light";
        } else {
            toggleBtn.innerText = "🌙 Dark";
        }
    }
});