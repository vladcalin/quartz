var counter = 1;

var pymicroserviceMethodCall = function (opts) {
    var url = opts.url;
    if (url == undefined) {
        url = "/api";
    }
    var method = opts.method;
    var params = opts.params;
    var onSuccess = opts.onSuccess;

    $.ajax({
        url: url,
        method: "post",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": counter
        }),
        success: onSuccess
    });
    counter++;

};