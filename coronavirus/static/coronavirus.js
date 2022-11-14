$(document).ready(function () {
    $("#filter").click(function () {
        const city = $("#city").val();
/*                    if (city==null || city==undefined || city==""){
            window.location.href = "http://" + window.location.host + "/coronavirus";
        }else{
        window.location.href = "http://" + window.location.host + "/coronavirus?city=" + city;
        }*/
        city==null || city==undefined || city=="" ? window.location.href = "http://" + window.location.host + "/coronavirus" : window.location.href = "http://" + window.location.host + "/coronavirus?city=" + city;
    });
    $("#sync").click(function () {
        $.get("{{ sync_data_url }}", function (result) {
            alert("Message: " + result.message);
        });
    });
});