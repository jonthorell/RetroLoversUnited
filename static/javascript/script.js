
const triggers = [
    'primary',
    'secondary',
    'success',
    'danger',
    'warning',
    'info',
    'light',
    'dark',
];
const basicInstances = [
    'alert-primary',
    'alert-secondary',
    'alert-success',
    'alert-danger',
    'alert-warning',
    'alert-info',
    'alert-light',
    'alert-dark',
];

triggers.forEach((trigger, index) => {
    let basicInstance = mdb.Alert.getInstance(document.getElementById(basicInstances[index]));
    document.getElementById(trigger).addEventListener('click', () => {
        basicInstance.show();
    });
});