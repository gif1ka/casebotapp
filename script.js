// telegram-wheel/script.js
const prizes = ["🎁 Секретный файл", "🎟 Бонус-код", "🚀 VIP на 1 день", "😎 Мем"];
const wheel = document.getElementById("wheel");
const spinBtn = document.getElementById("spinBtn");
const resultDiv = document.getElementById("result");

spinBtn.addEventListener("click", () => {
  spinBtn.disabled = true;
  const rand = Math.floor(Math.random() * prizes.length);
  const deg = 360 * 5 + (rand * 90); // 4 сек вращения + сектор

  wheel.style.transform = `rotate(${deg}deg)`;

  setTimeout(() => {
    const prize = prizes[rand];
    resultDiv.textContent = `Ты выиграл: ${prize}`;

    if (window.Telegram.WebApp) {
      Telegram.WebApp.sendData(prize);
      Telegram.WebApp.close();
    }
  }, 4000);
});

if (window.Telegram.WebApp) {
  Telegram.WebApp.expand();
}
