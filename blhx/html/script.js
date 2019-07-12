/**
 * 替换所有匹配exp的字符串为指定字符串
 * @param exp 被替换部分的正则
 * @param newStr 替换成的字符串
 */
String.prototype.replaceAll = function (exp, newStr) {
    return this.replace(new RegExp(exp, "gm"), newStr);
};

/**
 * 原型：字符串格式化
 * @param args 格式化参数值
 */
String.prototype.format = function (args) {
    var result = this;
    if (arguments.length < 1) {
        return result;
    }

    var data = arguments; // 如果模板参数是数组
    if (arguments.length == 1 && typeof (args) == "object") {
        // 如果模板参数是对象
        data = args;
    }
    for (var key in data) {
        var value = data[key];
        if (undefined != value) {
            result = result.replaceAll("\\{" + key + "\\}", value);
        }
    }
    return result;
}

var host = "127.0.0.1";
//var host = "192.168.2.1";
var screenshotPort = 50087;
var controlPort = 50088;
var screenshotBaseUrl = "http://" + host + ":" + screenshotPort + "/";
var controlBaseUrl = "http://" + host + ":" + controlPort + "/";


var bodyMargin;
var imgT;
var imgL;
var imgH;
var imgW;

var screenH;
var screenW;

var scale = 1;
var picSize = 540;

var c = 0;

function showImg() {
    $("#phone").attr("src", screenshotBaseUrl + "screenshot?format=jpg&size=540&quality=70&c=" + c++);//&size=1080
    lastShotTime = new Date().getTime();
}

var sizeUrl = screenshotBaseUrl + "size"
function initScale() {
    $.getJSON(sizeUrl, function (obj) {
        var minSize = Math.min(obj.width, obj.height);
        scale = picSize / minSize;
        // $(".span1").html("<br>" + scale);
    });
}

function setImgSize() {
    var h = $(window).height() - bodyMargin - 16;
    $("#phone").height(h);
    imgH = $("#phone").height();
}

$(window).resize(function () {
    setImgSize()
});

$(document).ready(function () {
    bodyMargin = $(document.body).outerHeight(true) - $(document.body).outerHeight();
    setImgSize();
    showImg();
    initScale();
})

var down = false;
var lastActionTime = new Date().getTime();
var lastShotTime = new Date().getTime();


var clickUrl = controlBaseUrl + "sendevent?type=click&clientX={x}&clientY={y}&downDelta=50"
$(function () {
    $("#phone").on("load", function () {
        var theImage = new Image();
        theImage.src = $("#phone").attr("src");
        screenW = theImage.width;
        screenH = theImage.height;
        imgW = $("#phone").width();
        imgT = $("#phone").offset().top;
        imgL = $("#phone").offset().left;
        $(".span2").html("<br>" + $("#phone").offset().left + "," + $("#phone").offset().top);
        var ii = 100 - (new Date().getTime()) + lastShotTime;
        if (ii > 0) {
            $(".span2").html("<br> " + ii);
            setTimeout("showImg()", ii);
        } else {
            showImg();
        }
    });
    // $("#phone").bind("click", function (e) {
    //     // var sPosPage = "(" + e.pageX + "," + e.pageY + ")";
    //     // var sPosScreen = "(" + e.screenX + "," + e.screenY + ")";
    //     var px = Math.ceil((e.pageX - bodyMargin / 2) * screenW / imgW);
    //     var py = Math.ceil((e.pageY - bodyMargin / 2) * screenH / imgH);
    //     $.get(clickUrl.format({ x: px, y: py }), function (data, status) {
    //     });
    //     // $(".span1").html("<br>" + screenW + "," + bodyMargin + "<br>Page: " + sPosPage + "<br>Screen: " + sPosScreen);
    // });

    $("#phone").mousedown(function (event) {
        if (checkInterval()) {
            down = true;
            aadragstart(event);
            lastActionTime = new Date().getTime();
        }
    });

    $("#phone").mouseout(function (event) {
        if (down) {
            down = false;
            aadragend(event);
        }
    });

    $("#phone").mouseup(function (event) {
        if (down) {
            down = false;
            aadragend(event);
        }
    });

    $("#phone").mousemove(function (event) {
        if (down && checkInterval()) {
            aadrag(event);
            lastActionTime = new Date().getTime();
        }
    });

    $("#back").bind("click", function () {
        $.get(controlBaseUrl + "sendevent?type=back", function (data, status) {
        });
    });
    $("#home").bind("click", function () {
        $.get(controlBaseUrl + "sendevent?type=home", function (data, status) {
        });
    });
    $("#recent").bind("click", function () {
        $.get(controlBaseUrl + "sendevent?type=recent", function (data, status) {
        });
    });
    $("body")
        .keydown(function (event) {
            var keycode = event.keyCode;
            if (keycode == 46) {
                $.get(controlBaseUrl + "sendevent?type=delete", function (data, status) {
                });
            } else if (keycode == 8) {
                $.get(controlBaseUrl + "sendevent?type=backspace", function (data, status) {
                });
            } else if (keycode == 192) { //`
                $.get(controlBaseUrl + "sendevent?type=back", function (data, status) {
                });
            } else if (keycode == 13) { //enter
                sendKeyCode(66);
            } else if (keycode == 32) { //space
                sendKeyCode(62);
            } else if (keycode <= 40 && keycode >= 37) { //space
                // sendKeyCode(62);
            } else if (keycode == 16 || keycode == 18) {

            } else if (event.originalEvent.key.length == 1) {
                sendKeyChar(event.originalEvent.key);
            }
            console.log(event);
        });
})

function checkInterval() {
    return new Date().getTime() - 40 > lastActionTime;
}


var downUrl = controlBaseUrl + "sendevent?type=mousedown&clientX={x}&clientY={y}&downDelta=50"
function aadragstart(e) {
    var px = Math.ceil((e.pageX - imgL) * screenW / imgW / scale);
    var py = Math.ceil((e.pageY - imgT) * screenH / imgH / scale);
    // $(".span2").html("<br>" + $("#phone").offset().left + "," + $("#phone").offset().top);
    $.get(downUrl.format({ x: px, y: py }), function (data, status) {
    });
    // $(".span1").html("<br>" + screenW + "," + py);
}

var moveUrl = controlBaseUrl + "sendevent?type=mousemove&clientX={x}&clientY={y}&downDelta=50"
function aadrag(e) {
    var px = Math.ceil((e.pageX - imgL) * screenW / imgW / scale);
    var py = Math.ceil((e.pageY - imgT) * screenH / imgH / scale);
    $.get(moveUrl.format({ x: px, y: py }), function (data, status) {
    });
}

var upUrl = controlBaseUrl + "sendevent?type=mouseup&clientX={x}&clientY={y}&downDelta=50"
function aadragend(e) {
    var px = Math.ceil((e.pageX - imgL) * screenW / imgW / scale);
    var py = Math.ceil((e.pageY - imgT) * screenH / imgH / scale);
    $.get(upUrl.format({ x: px, y: py }), function (data, status) {
    });
}

var keycodeUrl = controlBaseUrl + "sendevent?type=keycode&keycode={code}"
function sendKeyCode(keycode) {
    $.get(keycodeUrl.format({ code: keycode }), function (data, status) {
    });
}

var charUrl = controlBaseUrl + "sendevent?type=keychar&keychar={char}"
function sendKeyChar(char) {
    $.get(charUrl.format({ char: char }), function (data, status) {
    });
}
