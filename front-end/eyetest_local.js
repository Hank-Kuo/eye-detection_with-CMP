var email = window.sessionStorage.getItem("email");
function test(){
let {PythonShell} =  require('python-shell');
let options = {
  mode: 'text',
  pythonPath:  'C:\\Users\\User\\AppData\\Local\\Continuum\\anaconda3\\envs\\tensorflow-gpu\\python',
  pythonOptions: ['-u'], // get print results in real-time
};
 var a=PythonShell.run('code/exam_local.py', options, function (err, results) {
 if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results);
});

  var b=PythonShell.run('code/distance.py', options, function (err, results) {
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results);
});
 var a=PythonShell.run('code/model/run_demo_hand_with_tracker.py', options, function (err, results) {
 if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results);
});

}
var fs = require('fs');
fs.writeFile('email.txt', email, function (err) {
    if (err)
        console.log(err);
    else
        console.log('Write operation complete.');
});
