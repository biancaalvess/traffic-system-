document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");

    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch("http://127.0.0.1:8000/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                alert("Login realizado com sucesso!");
                localStorage.setItem("token", data.access_token);
                window.location.href = "dashboard.html";
            } else {
                const errorData = await response.json();
                alert(`Erro: ${errorData.detail}`);
            }
        } catch (error) {
            console.error("Erro ao fazer login:", error);
            alert("Erro no servidor. Tente novamente mais tarde.");
        }
    });
});
