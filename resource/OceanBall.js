var url = "//flights.ctrip.com/domesticsearch/search/SearchRoundRecommend?DCity1=AAT&ACity1=AKU&SearchType=D&DDate1=2018-04-12&ACity2=AAT&DDate2=2018-05-11&IsNearAirportRecommond=0&LogToken=0a29af5f595740a99c86b34d377c8eeb&CK=5D875D554609FCD32B31FD819B955CFD";
var _searchCount_c = 0;

function ajaxRequest(n, t) {
    var i = null, e, f, l, o, s, r, c, u, h;
    if (typeof XMLHttpRequest != "undefined") i = new XMLHttpRequest; else if (typeof ActiveXObject != "undefined") {
        if (typeof arguments.callee.aciveXString != "string") for (e = ["MSXML2.XMLHttp.6.0", "MSXML2.XMLHttp.3.0", "MSXML2.XMLHttp"], f = 0, l = e.length; f < l; f++) try {
            i = new ActiveXObject(e[f]);
            arguments.callee.activeXString = e[f];
            break
        } catch (a) {
        }
        i == null && (i = new ActiveXObject(arguments.callee.activeXString))
    }
    i.onreadystatechange = function () {
        try {
            if (i.readyState == 4) if (i.status >= 200 && i.status < 300 || i.status == 304) {
                var r = eval("(" + i.responseText + ")");
                if (_searchCount_c == 0 && r && r.Error && (r.Error.Code == 104 || r.Error.Code == 1004) && (r.Error.Message == "" || !r.Error.Message)) {
                    _searchCount_c++;
                    setTimeout(function () {
                        var i = n.split("&");
                        i.pop();
                        ajaxRequest(i.join("&") + "&rt=" + Math.random() * 1e3, t)
                    }, 1e3);
                    return
                }
                jsonCallback.done(r)
            } else i.status != 0 && jsonCallback.onError()
        } catch (u) {
            jsonCallback.onError()
        }
    };
    window.location.hash && (o = window.location.hash.match(/DDate1=\d{4}-\d{2}-\d{2}/), o && o.length > 0 && (n = n.replace(/DDate1=(\d{4}-\d{2}-\d{2})/ig, o[0])), s = window.location.hash.match(/DDate2=\d{4}-\d{2}-\d{2}/), s && s.length > 0 && (n = n.replace(/DDate2=(\d{4}-\d{2}-\d{2})/ig, s[0])));
    r = n.replace(/^[\s\xA0]+|[\s\xA0]+$/g, "");
    (r.indexOf("ClassType=CF") == -1 || r.indexOf("ClassType=&") != -1) && (r += getStorage("FD_SearchPage_onlyCf") == "CF" ? "&ClassType=CF" : "");
    _searchCount_c > 0 && (c = t.split(".")[1], t = "0." + c.substring(1, c.length - 1));
    u = r.split("&");
    h = r.indexOf("rk=") >= 0 || r.indexOf("rt=") >= 0 ? u.splice(u.length - 2, 1)[0] : u.pop();
    u.push("CK=");
    h = h.split("=")[1];
    var fn = (function (u, r, k, t) {
        var r19 = 1, p19r = 1;
        r19 = r19 *= parseInt(Math.sin(5) * 0xa);
        r19 = r19 *= parseInt(Math.cos(5) * 0xa);
        if (r19 < 0) r19 = -r19;
        while (r19 > 30) r19 = r19 % 10;
        p19r = p19r += parseInt(Math.cos(6) * 0xa);
        if (p19r < 0) p19r = -p19r;
        while (p19r > 30) p19r = p19r % 10;
        (function (r, u, x, y, t, k) {
            if (!window.location.href) {
                return;
            }
            var l = r.split('');
            var c = l.splice(y, 1);
            l.splice(x, 0, c);
            t.open('GET', u.join('&') + l.join('') + '&r=' + k, !0);
            t.send(null);
        })(r, u, r19, p19r, t, k)
    });
    fn(u, h, t, i)
}

var jsonCallback = {
    isError: !1, isReady: !1, data: {}, readyList: [], errorList: [], ready: function (n) {
        this.isReady == !1 ? this.readyList.push(n) : n(this.data)
    }, done: function (n) {
        this.isReady = !0;
        this.data = n;
        for (var t = 0; this.readyList[t];) this.readyList[t](n), t++
    }, error: function (n) {
        this.isError == !1 ? this.errorList.push(n) : n()
    }, onError: function () {
        this.isError = !0;
        for (var n = 0; this.errorList[n];) this.errorList[n](), n++
    }
}, getStorage = function (n) {
    var i, r, t;
    try {
        if (i = "{}", window.localStorage) i = localStorage.getItem("jStorage"); else if (window.globalStorage) i = window.globalStorage[window.location.hostname]; else {
            r = document.head || document.getElementsByTagName("head")[0];
            t = document.createElement("link");
            t.style.behavior = "url(#default#userData)";
            r.appendChild(t);
            try {
                t.load("jStorage")
            } catch (u) {
                t.setAttribute("jStorage", "{}");
                t.save("jStorage");
                t.load("jStorage")
            }
            i = t.getAttribute("jStorage") || "{}";
            r.removeChild(t)
        }
        return !i || i == "{}" ? "" : eval("(" + i + ")")[n]
    } catch (f) {
        return ""
    }
}


var searchRouteIndex = "0";
var isCivil = false;
var roundTripCombinationSwitch = true;
(getStorage('RoundRecomandHistoryIsOpen') !== 1 || (!isCivil && roundTripCombinationSwitch)) && url.indexOf('SearchRoundRecommend') > -1 && (url = url.replace('SearchRoundRecommend', ['SearchFirstRouteFlights', 'SearchSecondRouteFlights'][searchRouteIndex]));
ajaxRequest(url + '&rk=' + Math.random() * 10 + '162719', '0.2615385776611629926218');
