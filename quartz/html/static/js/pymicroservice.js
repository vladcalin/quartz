var counter = 1;

var pymicroserviceMethodCall = function (opts) {
    var url = opts.url;
    if (url == undefined) {
        url = "/api";
    }
    var method = opts.method;
    var params = opts.params;
    var onSuccess = opts.onSuccess;
    var onError = opts.onError;

    $.ajax({
        url: url,
        method: "post",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": Math.random().toString(36).substring(7)
        }),
        success: function (data) {
            if (data.error == null) {
                onSuccess(data.result);
            }
            else {
                onError(data.error);
            }
        }
    });
    counter++;

};

var pymicroserviceBatchCall = function (opts) {
    var url = opts.url;
    if (url == undefined) {
        url = "/api";
    }
    var onSuccess = opts.onSuccess;
    var onError = opts.onError;

    var body = [];
    for (var i = 0; i < opts.calls.length; i++) {
        body.push({
            "jsonrpc": "2.0",
            "method": opts.calls[i].method,
            "params": opts.calls[i].params,
            "id": Math.random().toString(36).substring(7)
        })
    }
    $.ajax({
        url: url,
        method: "post",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(body),
        success: function (data) {
            if (data.error == null) {
                onSuccess(data.result);
            }
            else {
                onError(data.error);
            }
        }
    });
};


function bootstrapNotify(type, message) {
    $.notify({
        message: message
    }, {
        type: type
    })
}