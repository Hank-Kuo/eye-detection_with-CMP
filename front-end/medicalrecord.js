var identify2 = sessionStorage.getItem('identify');
var date2 = sessionStorage.getItem('date');
document.getElementById('date1').value = date2;

var db = firebase.firestore();

var docRef = db.collection("medic").doc(identify2);

docRef.get().then(function(doc) {
    if (doc.exists) {
      document.getElementById('fname').value = doc.data().name;
      document.getElementById('phonename').value = doc.data().phone;
      document.getElementById('medical').value = doc.data().medical;
      document.getElementById('allergic').value = doc.data().allergic;
      document.getElementById('lbox').value = doc.data().medbox;
      document.getElementById('subject').value = doc.data().txtbox;
    } else {
        // doc.data() will be undefined in this case
        console.log("No such document!");
    }
}).catch(function(error) {
    console.log("Error getting document:", error);
});




function validate(){
  alert('請於  '+date2+'  14:00看診 您的號碼為12號');
  
}

function savedata() {

  const txtName = getid('fname');
  const phone = getid('phonename');
  const medic = getid('medical');
  const allergic = getid('allergic');
  const medbox = getid('lbox');
  const txtbox = getid('subject');
  console.log(medbox);
  console.log(allergic);
  console.log(medic);

  saveMessage(identify2, date2, txtName, allergic, phone, medic, medbox, txtbox);

  document.location.href = 'index.html';
}


function saveMessage(identify2, date2, txtName, allergic, phone, medic, medbox, txtbox) {
  db.collection('medic').doc(identify2).set({
    // date: date,
    identify: identify2,
    name: txtName,
    date: date2,
    phone: phone,
    medical: medic,
    allergic: allergic,
    medbox: medbox,
    txtbox: txtbox
  }).then(function() {
    console.log("Document successfully written!");
  }).catch(function(error) {
    console.error("Error writing document: ", error);
  });

}


function getid(id) {
  return document.getElementById(id).value;
}
