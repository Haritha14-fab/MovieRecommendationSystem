document.addEventListener("DOMContentLoaded", () => {
    const passwordInput = document.getElementById("password");
    const confirmInput = document.getElementById("confirm_password");

    const togglePasswordBtn = document.getElementById("togglePasswordRegister");
    const toggleConfirmBtn = document.getElementById("toggleConfirmPassword");

    function toggleInputType(inputEl, btnEl) {
        if (!inputEl) return;
        const isHidden = inputEl.type === "password";
        inputEl.type = isHidden ? "text" : "password";
        if (btnEl) btnEl.textContent = isHidden ? "🙈" : "👁";
    }

    if (passwordInput && togglePasswordBtn) {
        togglePasswordBtn.addEventListener("click", () => {
            toggleInputType(passwordInput, togglePasswordBtn);
        });
    }

    if (confirmInput && toggleConfirmBtn) {
        toggleConfirmBtn.addEventListener("click", () => {
            toggleInputType(confirmInput, toggleConfirmBtn);
        });
    }
});

