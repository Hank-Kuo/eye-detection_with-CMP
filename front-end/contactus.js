function countdownTimeStart() {

  // var timer = document.getElementById("time").vlaue;
  // console.log(timer);

  var countDownDate = new Date().getTime() + 6000;
  console.log(countDownDate);

  // Update the count down every 1 second
  var x = setInterval(function() {

    // Get todays date and time
    var now = new Date().getTime();
    console.log(now);

    // Find the distance between now an the count down date
    var distance = countDownDate - now;
    var distance2=Math.round(distance);
    console.log(distance);
    console.log(distance2);

    // Time calculations for days, hours, minutes and seconds
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // Output the result in an element with id="demo"
    document.getElementById("demo").innerHTML = hours + "h " +
      minutes + "m " + seconds + "s ";

    // If the count down is over, write some text
    if (distance < 0) {
      clearInterval(x);
      Alert.render();
      document.getElementById("demo").innerHTML = "";
    }
  }, 1000);
}




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
}
