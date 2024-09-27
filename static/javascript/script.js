
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

(function replaceBlinks() {
    var blinks = document.getElementsByTagName("blink");
    while (blinks.length) {
        var blink = blinks[0];
        var blinky = document.createElement("blinky");
        blinky.innerHTML = blink.innerHTML;
        blink.parentNode.insertBefore(blinky, blink);
        blink.parentNode.removeChild(blink);
    }
})();
(function blink(visible) {
    var blinkies = document.getElementsByTagName("blinky"),
        visibility = visible ? "visible" : "hidden";
    for (var i = 0; i < blinkies.length; i++) {
        blinkies[i].style.visibility = visibility;
    }
    setTimeout(function () {
        blink(!visible);
    }, 500);
})(true);