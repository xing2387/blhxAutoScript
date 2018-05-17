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

var down = false;
var lastActionTime = new Date();

var sizeUrl = "http://127.0.0.1:53516/size"
var clickUrl = "http://127.0.0.1:53516/sendevent?type=click&clientX={x}&clientY={y}&downDelta=50"
$(function () {
    $('img').on("load", function () {
        showImg();
        $.get(sizeUrl, function (data, status) {
            data = JSON.parse(data);
            screenH = data.height;
            screenW = data.width;
            // $(".span2").html("<br>" + data.width + "," + screenH);

            // alert("Data: " + data + "\nStatus: " + status);
        });
        imgW = $('img').width();
    });
    $("img").bind("click", function (e) {
        // var sPosPage = "(" + e.pageX + "," + e.pageY + ")";
        // var sPosScreen = "(" + e.screenX + "," + e.screenY + ")";
        // var px = Math.ceil((e.pageX - bodyMargin / 2) * screenW / imgW);
        // var py = Math.ceil((e.pageY - bodyMargin / 2) * screenH / imgH);
        // $.get(clickUrl.format({ x: px, y: py }), function (data, status) {
        // });
        // $(".span1").html("<br>" + screenW + "," + bodyMargin + "<br>Page: " + sPosPage + "<br>Screen: " + sPosScreen);
    });

    $("img").mousedown(function (event) {
        if (checkInterval()) {
            down = true;
            aadragstart(event);
            lastActionTime = Date.parse(new Date());
        }
    });

    $("img").mouseup(function (event) {
        // if (checkInterval()) {
        down = false;
        aadragend(event);
        // }
    });
    $("img").mousemove(function (event) {
        if (down && checkInterval()) {
            aadrag(event);
            lastActionTime = Date.parse(new Date());
        }
    });
})

function checkInterval() {
    return Date.parse(new Date()) - 60 > lastActionTime;
}


var downUrl = "http://127.0.0.1:53516/sendevent?type=mousedown&clientX={x}&clientY={y}&downDelta=50"
function aadragstart(event) {
    // Ev= event || window.event; 
    var px = Math.ceil((window.event.pageX - bodyMargin / 2) * screenW / imgW);
    var py = Math.ceil((window.event.pageY - bodyMargin / 2) * screenH / imgH);
    $.get(downUrl.format({ x: px, y: py }), function (data, status) {
    });
    $(".span1").html("<br>" + px + "," + py);

}

var moveUrl = "http://127.0.0.1:53516/sendevent?type=mousemove&clientX={x}&clientY={y}&downDelta=50"
function aadrag(e) {
    var px = Math.ceil((e.pageX - bodyMargin / 2) * screenW / imgW);
    var py = Math.ceil((e.pageY - bodyMargin / 2) * screenH / imgH);
    $.get(moveUrl.format({ x: px, y: py }), function (data, status) {
    });
}

var upUrl = "http://127.0.0.1:53516/sendevent?type=mouseup&clientX={x}&clientY={y}&downDelta=50"
function aadragend(e) {
    var px = Math.ceil((e.pageX - bodyMargin / 2) * screenW / imgW);
    var py = Math.ceil((e.pageY - bodyMargin / 2) * screenH / imgH);
    $.get(upUrl.format({ x: px, y: py }), function (data, status) {
    });
}

// http://127.0.0.1:53516/sendevent?type=click&clientX=NaN&clientY=NaN&downDelta=50