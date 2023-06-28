//start with defining some constants


function printAlert(newMessage) {
    let myAlert = "<h2>" + newMessage + "</h2><hr>"
    console.log(myAlert)
    document.getElementById('alert-id').innerHTML = myAlert;
    mdb.Alert.getInstance(document.getElementById('alert-id')).show();
}



const datepickerDisablePast = document.querySelector('.datepicker-disable-past');
new mdb.Datepicker(datepickerDisablePast, {
    disablePast: true
});
