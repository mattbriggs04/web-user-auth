// form global variables
const formContainer = document.getElementById("form-container");
// sign-up form global variables
const signupForm = document.getElementById("signup-form");
const signupOutputMessage = document.getElementById("signup-output-message");
const nameInput = document.getElementById("name-input");
const emailInput = document.getElementById("email-input");
const passwordInput = document.getElementById("password-input");
const confirmPasswordInput = document.getElementById("confirm-password-input");
const loginSwitchBtn = document.getElementById("login-switch-btn");

// login form global variables
const loginForm = document.getElementById("login-form");
const signupSwitchBtn = document.getElementById("signup-switch-btn");
const loginNameInput = document.getElementById("login-name-input");
const loginPasswordInput = document.getElementById("login-password-input");

// welcome header global variables
const welcomeContainer = document.getElementById("welcome-container");
const welcomeHeader = document.getElementById("welcome-header");

// helper function for switching to welcome page
function showWelcome(name) {
    console.log("show welcome activating...");
    signupForm.classList.add("hidden");
    loginForm.classList.add("hidden");
    welcomeContainer.classList.remove("hidden");

    welcomeHeader.innerText = `Welcome, ${name}`;
}

// signup form submit handler
signupForm.addEventListener("submit", async (e) => {
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
        const serverResponse = await res.json();

        // handle status cases
        if (serverResponse.status === "error") {
            signupOutputMessage.className = "error-msg";
            signupOutputMessage.innerText = serverResponse.errorMsg;
        }
        else if (serverResponse.status === "ok") {
            signupOutputMessage.className = "";
            signupOutputMessage.innerText = "Successfully created account.";
        }

    }
    catch (e) {
        console.log(`Signup form error: ${e}`);
    }
    
});

// login switch button handler
loginSwitchBtn.addEventListener("click", () => {
    signupForm.classList.add("hidden");
    loginForm.classList.remove("hidden");
});

// login form submit handler
loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        username: loginNameInput.value,
        password: loginPasswordInput.value
    }

    try {
        const res = await fetch("/login-user", {
            method: "POST",
            body: JSON.stringify(data)
        });
        const serverResponse = await res.json();

        if (serverResponse.status === "error") {
            signupOutputMessage.className = "error-msg";
            signupOutputMessage.innerText = serverResponse.errorMsg;
        }
        else if (serverResponse.status === "ok") {
            showWelcome(data.username);
        }
    }
    catch (e) {
        console.log(`Login form error: ${e}`);
    }
});

// signup switch button handler
signupSwitchBtn.addEventListener("click", () => {
    loginForm.classList.add("hidden");
    signupForm.classList.remove("hidden");
});