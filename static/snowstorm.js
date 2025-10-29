// snowfall.js — efecto de nieve animada y aleatoria
document.addEventListener("DOMContentLoaded", () => {
  const snowContainer = document.createElement("div");
  document.body.appendChild(snowContainer);

  const snowflakes = ["❅", "❆"];
  const snowflakeCount = 10; // número total de copos en pantalla

  for (let i = 0; i < snowflakeCount; i++) {
    const snowflake = document.createElement("span");
    snowflake.classList.add("snowflake");
    snowflake.textContent = snowflakes[Math.floor(Math.random() * snowflakes.length)];

    // posición y tamaño aleatorio
    snowflake.style.left = Math.random() * 100 + "vw";
    snowflake.style.fontSize = 0.8 + Math.random() * 1 + "rem";
    snowflake.style.animationDuration = 5 + Math.random() * 10 + "s";
    snowflake.style.animationDelay = Math.random() * 5 + "s";
    snowflake.style.opacity = 0.3 + Math.random() * 0.5;

    snowContainer.appendChild(snowflake);
  }
});
