const createAccountForm = document.getElementById("create-account-form");
const outputMessage = document.getElementById("output-message");
const nameInput = document.getElementById("name-input");
const emailInput = document.getElementById("email-input");
const passwordInput = document.getElementById("password-input");
const confirmPasswordInput = document.getElementById("confirm-password-input");

createAccountForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        username: nameInput.value,
        email: emailInput.value,
        password: passwordInput.value,
        confirmPassword: confirmPasswordInput.value
    }

    try {
        const res = await fetch("/register-user", 
            {
                method: "POST",
                body: JSON.stringify(data)
            });
        const serverResponse = await res.json()

        // handle status cases
        if (serverResponse.status === "error") {
            outputMessage.className = "error-msg";
            outputMessage.innerText = serverResponse.errorMsg;
        }

        if (serverResponse.status === "ok") {
            outputMessage.className = "";
            outputMessage.innerText = "Successfully created account."
        }

    }
    catch (e) {
        console.log(`Error: ${e}`)
    }
    
})