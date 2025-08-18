const createAccountForm = document.getElementById("create-account-form");

createAccountForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        name: document.getElementById("name-input").value,
        email: document.getElementById("email-input").value,
        password: document.getElementById("password-input").value,
        confirmPassword: document.getElementById("confirm-password-input").value
    }

    try {
        const res = await fetch("/register-user", 
            {
                method: "POST",
                body: JSON.stringify(data)
            });
        const serverResponse = await res.json()
        console.log("Server responded with:")
        console.log(serverResponse)
    }
    catch (e) {
        console.log(`Error: ${e}`)
    }
})