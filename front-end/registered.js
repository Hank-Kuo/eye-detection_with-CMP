document.getElementById('btn_relaxureye').addEventListener('click', getidentify);

function getidentify() {
  const identify = document.getElementById("identify").value;
  sessionStorage.setItem('identify', identify);
}
