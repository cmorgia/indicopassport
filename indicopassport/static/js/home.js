$(function(){
    window.webSocket = new WebSocket("wss://127.0.0.1");
    window.webSocket.onmessage = function(event) {
        var payload = $.parseJSON(event.data);
        jsonRpc(Indico.Urls.JsonRpcService,'passport.redirect',payload,function handler(response,error){
            if (error) {
                var popup = new ErrorPopup("Connection error", ["Unable to contact the server"], "");
                popup.open();
            } else {
                if (response.error) {
                    var popup = new ErrorPopup("Passport lookup returned an error", [response.error], "");
                    popup.open();
                } else {
                    window.location=response.location;
                }
            }
        });
    };
    $( window ).unload(function() {
        window.webSocket.close();
    });
});