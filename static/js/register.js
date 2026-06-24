document.addEventListener("DOMContentLoaded", () => {
    const passwordInput = document.getElementById("password");
    const confirmInput = document.getElementById("confirmPassword");
    const showButton = document.getElementById("showPassword");
    const strengthBar = document.getElementById("strengthBar");
    const strengthText = document.getElementById("strengthText");
    const matchMessage = document.getElementById("matchMessage");

    if (showButton && passwordInput) {
        showButton.addEventListener("click", () => {
            const isHidden = passwordInput.type === "password";
            passwordInput.type = isHidden ? "text" : "password";
            showButton.textContent = isHidden ? "Hide" : "Show";
        });
    }

    function scorePassword(value) {
        let score = 0;
        if (value.length >= 8) score += 1;
        if (/[A-Z]/.test(value)) score += 1;
        if (/[0-9]/.test(value)) score += 1;
        if (/[^A-Za-z0-9]/.test(value)) score += 1;
        return score;
    }

    if (passwordInput && strengthBar && strengthText) {
        passwordInput.addEventListener("input", () => {
            const score = scorePassword(passwordInput.value);
            const labels = ["Too weak", "Weak", "Fair", "Good", "Strong"];
            strengthBar.style.width = `${score * 25}%`;
            strengthBar.className = `progress-bar bg-${score < 2 ? "danger" : score < 3 ? "warning" : "success"}`;
            strengthText.textContent = passwordInput.value ? labels[score] : "";
        });
    }

    if (passwordInput && confirmInput && matchMessage) {
        confirmInput.addEventListener("input", () => {
            if (!confirmInput.value) {
                matchMessage.textContent = "";
                return;
            }
            const matches = passwordInput.value === confirmInput.value;
            matchMessage.textContent = matches ? "Passwords match" : "Passwords do not match";
            matchMessage.className = matches ? "text-success" : "text-danger";
        });
    }
});
