const prizes = ["🚀 1 день VIP", "🎁 Стикер", "🎉 Купон", "😎 Бонус"];

function spin() {
  const rand = Math.floor(Math.random() * prizes.length);
  const deg = 360 * 3 + rand * 90;

  document.getElementById("wheel").style.transform = `rotate(${deg}deg)`;

  setTimeout(() => {
    const prize = prizes[rand];
    if (window.Telegram && Telegram.WebApp) {
      Telegram.WebApp.sendData(prize);
      Telegram.WebApp.close();
    }
  }, 4000);
}
