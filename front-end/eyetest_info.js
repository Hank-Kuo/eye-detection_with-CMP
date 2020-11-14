var db = firebase.firestore();
var email;
email = window.sessionStorage.getItem("email");
console.log(email);
var eye_temp;

var docRef1 = db.collection("User").doc(email);

docRef1.get().then(function(doc1) {
  eye_temp = doc1.data().eye_temp;
  get_eyesight(eye_temp, email);

}).catch(function(error) {
  console.log("Error getting document:", error);
});

function get_eyesight(eye_temp, email) {
    db.collection("User").doc(email).collection("eyesight").doc(eye_temp).get().then(function(doc) {
      document.getElementById("eye_left1").innerHTML = doc.data().eye_left;
      document.getElementById("eye_right1").innerHTML = doc.data().eye_right;
      document.getElementById("eye_flash_left1").innerHTML = doc.data().eye_flash_left;
      document.getElementById("eye_flash_right1").innerHTML = doc.data().eye_flash_right;
      document.getElementById("eye_yello_left1").innerHTML = doc.data().yellow;
      document.getElementById("eye_fly_left1").innerHTML = doc.data().mostiquto;
      document.getElementById("eye_blind_left1").innerHTML = doc.data().blind;
});
}
