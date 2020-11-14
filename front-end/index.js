const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const path = require('path')
const Tray = electron.Tray
const Menu = electron.Menu
const iconPath = path.join(__dirname,'images/btn_slideR.png')
let appIcon = null;

// var user = auth.currentUser;
// var name, email, photoUrl, uid, emailVerified;
//
// if (user != null) {
//   name = user.displayName;
//   email = user.email;
//   uid = user.uid;}
//
// var docRef = db.collection("User").doc("uid");


function createWindow () {

  window = new BrowserWindow({width: 960, height: 590,resizable: false})
  window.loadFile('index.html')
  appIcon = new Tray(iconPath)
  appIcon.setToolTip('electron app')
  const contextMenu = Menu.buildFromTemplate([
    {
      label: 'Restore app',
      click: () => {
        window.show()
      }
    },
    {
      label: 'Quit app',
      click: () => {
        window.close()
      }
    }
  ])
  appIcon.setContextMenu(contextMenu)
  appIcon.on('click', () => {
    window.isVisible() ? window.hide() : window.show()
  })

//   let {PythonShell} =  require('python-shell');

// PythonShell.run('opencam.py',  function  (err, results)  {
  //  if  (err)  throw err;
    //console.log('opencam.py finished.');
    //console.log('results', results);
  // });

   window.on('close', (event) => {
       windows = null
   })

   window.on('minimize',function(event){
       event.preventDefault()
       window.hide()
   })
}

function eye_relax(){
    document.location.href='eyeinfor.html';

}

app.on('ready', createWindow)

// app.on('ready', createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
      app.quit()
    }
})
//
// app.on('window-all-closed', () => {
//     if (process.platform !== 'darwin') {
//       app.quit()
//     }
// })

app.on('activate', () => { window.show() })
