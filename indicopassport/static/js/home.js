function readerdata(controlId) {
    if (controlId == "ocr") {
        var passportId = MyApplet.GetDocumentNumber();
        var passportExpire = MyApplet.GetDateOfExpiry();
        var passportOrigin = MyApplet.GetIssuer();
        var data = {
            "Passport Origin": passportOrigin,
            "Passport ID": passportId,
            "Passport Expire": passportExpire
        };
        jsonRpc(Indico.Urls.JsonRpcService,'passport.redirect',data,function handler(response,error){
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
    }
}

$(function(){
    var jarsBase = "static/assets/plugins/indicopassport/jars/";
    var fragment = "<applet name=\"MyApplet\" code=swipeapplet.SwipeApplet.class " +
                        "codebase=\""+jarsBase+"\" archive=\"swipeapplet.jar,mmmreader.jar\"  style=\"width: 400px; height: 50px\">" +
                        "Browser Does not support Java </applet>";
    var isSecurity = $('#toggleShowQRCode').length>0;
    if (isSecurity) {
        $(document.body).append(fragment);
    }
});