Array.from(document.getElementsByTagName("code")).forEach(function (container) {
  let btn = new Image();
  btn.src = "https://cdn.iconscout.com/icon/free/png-32/copy-data-667851.png";
  btn.style.float = "right";
  btn.style.color = "white";
  btn.onclick = () => {
    navigator.clipboard.writeText(document.getElementsByTagName("code")[7].innerText).then(
      () => {
        alert("ok");
        return false;
      },
      () => {
        alert("erro");
        return false;
      }
    );
  };
  container.insertBefore(btn, container.firstChild);
});
