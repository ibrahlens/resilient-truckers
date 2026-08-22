// =====================================
// Donation Form
// =====================================

document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("donationForm");

    if (!form) return;

    const button = form.querySelector(".donate-btn");
    const phoneInput = document.getElementById("phone");
    const amountInput = document.getElementById("amount");

    // =====================================
    // Clean Phone Number
    // =====================================

    phoneInput.addEventListener("input", function () {

        this.value = this.value.replace(/[^\d]/g, "");

    });

    // =====================================
    // Form Submission
    // =====================================

    form.addEventListener("submit", function (e) {

        const amount = Number(amountInput.value);

        if (amount < 1) {

            e.preventDefault();

            alert("Please enter a valid donation amount.");

            amountInput.focus();

            return;

        }

        button.disabled = true;

        button.innerHTML = `
            <span class="spinner"></span>
            Processing...
        `;

    });

});