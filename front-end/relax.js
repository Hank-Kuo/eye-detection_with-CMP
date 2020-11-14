function test(){
let {PythonShell} =  require('python-shell');
let options = {
  mode: 'text',
  pythonPath: 'C:\\Users\\User\\AppData\\Local\\Continuum\\anaconda3\\envs\\tensorflow-gpu\\python',

  pythonOptions: ['-u'], // get print results in real-time
};
 var a=PythonShell.run('code/relax.py', options, function (err, results) {
 if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results);
});

  var b=PythonShell.run('code/relax_sound.py', options, function (err, results) {
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results);  
});
 

}

