//start with defining some constants

const welcomePhrase = "Another visitor!\nStay a while, stay forever!";
console.log(welcomePhrase)

const datepickerDisablePast = document.querySelector('.datepicker-disable-past');
new mdb.Datepicker(datepickerDisablePast, {
    disablePast: true
});

