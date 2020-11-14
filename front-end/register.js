document.getElementById('form').addEventListener('submit', submitForm);
var db = firebase.firestore();
var uid;


function submitForm(e) {
  e.preventDefault();

  //get getElement
  const emailField = getid('txtEmail');
  const passwordField = getid('txtPassword');
  const birthday = getid('txtBirthday');
  const identity = getid('txtIdentity');
  const name = getid('txtName');

  // const signUpBtn = getid('btnSignup')







  var auth = firebase.auth();

  const promise = auth.createUserWithEmailAndPassword(emailField, passwordField).then(cred => {
    uid = cred.user.uid;
    console.log("uid", cred.user.uid);
    saveMessage(emailField, birthday, identity, name, uid);
    document.location.href = 'login.html';


  }).catch(function(error) {
    var errorCode = error.code;
    var errorMessage = error.message;

  })


}


function saveMessage(emailField, birthday, identity, name, uid) {
  // Add a new document in collection uid
  db.collection("User").doc(emailField).set({
      name: name,
      email: emailField,
      birthday: birthday,
      identity: identity,
      uid: uid,
      eye_temp:"eye_1"
    })
    .then(function() {
      console.log("Document successfully written!");

    })
    .catch(function(error) {
      console.error("Error writing document: ", error);
    });

    db.collection("User").doc(emailField).collection("eyesight").doc("eye_1").set({
      blind :"null",
      date :"null",
      eye_flash_left :"null",
      eye_flash_right :"null",
      eye_left :"null",
      eye_right :"null",
      mostiquto :"null",
      yellow :"null"
    });

    db.collection("User").doc(emailField).collection("eyesight").doc("eye_2").set({
      blind :"null",
      date :"null",
      eye_flash_left :"null",
      eye_flash_right :"null",
      eye_left :"null",
      eye_right :"null",
      mostiquto :"null",
      yellow :"null"
    });

    db.collection("User").doc(emailField).collection("eyesight").doc("eye_3").set({
      blind :"null",
      date :"null",
      eye_flash_left :"null",
      eye_flash_right :"null",
      eye_left :"null",
      eye_right :"null",
      mostiquto :"null",
      yellow :"null"
    });

}


function getid(id) {
  return document.getElementById(id).value;
}
