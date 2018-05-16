
var bodyMargin;
var imgT;
var imgL;
var imgH;
var imgW;

var screenH;
var screenW;

var c = 0;
function showImg() {
    $("img").attr("src", "http://127.0.0.1:53516/screenshot.jpg?c=" + c++)
}
function setImgSize() {
    var h = $(window).height() - bodyMargin;
    $('img').height(h);
    imgH = $('img').height();
}

$(window).resize(function () {
    setImgSize()
});

$(document).ready(function () {
    bodyMargin = $(document.body).outerHeight(true) - $(document.body).outerHeight();
    imgT = bodyMargin;
    imgL = bodyMargin;
    setImgSize()
    showImg()
})

$(function () {
    var sizeUrl = "http://127.0.0.1:53516/size"
    $('img').on("load", function () {
        showImg();
        $.get(sizeUrl, function(data,status){
            screenH = data.height;
            screenW = data.width;
            // alert("Data: " + data + "\nStatus: " + status);
        });
        imgW = $('img').width();
    });
    var clickUrl = "http://127.0.0.1:53516/sendevent?type=click&clientX={x}&clientY={y}&downDelta=50"
    $("img").bind("click", function (e) {    
        var sPosPage = "(" + e.pageX + "," + e.pageY + ")";
        var sPosScreen = "(" + e.screenX + "," + e.screenY + ")";
        $.get(sizeUrl, function(data,status){
        });
        // $("span").html("<br>" + imgW + "," + imgH + "<br>Page: " + sPosPage + "<br>Screen: " + sPosScreen);
    });
})