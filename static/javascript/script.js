//start with defining some constants

function printAlert(newMessage) {
    let myAlert = '<h2><img src="https://res.cloudinary.com/retroloversunited/raw/upload/v1686394021/static/images/Boing_Ball.5037f34b676b.svg" height="40" width="40" alt="BoingBall logo" loading="lazy">'
    myAlert += "    " + newMessage + "</h2><hr>"
    console.log(myAlert)
    document.getElementById('alert-id').innerHTML = myAlert;
    mdb.Alert.getInstance(document.getElementById('alert-id')).show();
}
