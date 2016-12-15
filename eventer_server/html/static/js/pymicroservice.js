var counter = 1;

var pymicroserviceMethodCall = function (opts) {
    var url = opts.url;
    var method = opts.method;
    var params = opts.params;
    var onSuccess = opts.onSuccess;
    var onError = opts.onError;

    $.ajax({
        url: url,
        method: "post",
        contentTyoe: "application/json",
        data: {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": counter
        },
        success: onSuccess,
        error: onError
    });
    counter++;

};