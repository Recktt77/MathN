function generateEquation() {
    const n = document.getElementById("n").value;
    const verbose = document.getElementById("verbose").checked;

    console.log("Button clicked. Value of n:", n);
    console.log("Verbose mode:", verbose);

    if (n) {
        console.log("Calling eel.calculate_equation...");
        eel.calculate_equation(n, verbose)(function(response) {
            console.log("Received response:", response);

            // Отображаем формулы и дополнительные данные
            document.getElementById("equation").innerText = response.equation_str;

            // Отображение шагов в режиме Verbose Mode
            if (response.verbose_steps.length > 0) {
                document.getElementById("steps").innerText = response.verbose_steps.join('\n');
            } else {
                document.getElementById("steps").innerText = ""; // Очистить, если шагов нет
            }
        });
    } else {
        alert("Please enter a valid number for 'n'.");
    }
}
