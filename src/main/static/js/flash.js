

var success = function (type,msg) {
    console.debug("testing success");
    var message = SnackBar({
        message: msg,
        status: type,
        timeout: 5000
    });
};

var def = function () {
    let def = SnackBar({
        message: "Hello World!"
    })
};




function demoCustom() {
    let timeout = document.getElementById("demo_timeout").value;

    if (document.getElementById("demo_notimeout").checked) {
        timeout = false;
    }

    SnackBar({
        message: document.getElementById("demo_text").value,
        dismissible: document.getElementById("demo_dismiss").checked,
        status: document.getElementById("demo_status").value,
        timeout: timeout
    });

    return false;
}
