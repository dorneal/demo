function ajaxRequest(n, t) {
    var i = null, e, f, l, o, s, r, c, u, h;
    if (typeof XMLHttpRequest != "undefined")
        i = new XMLHttpRequest;
    else if (typeof ActiveXObject != "undefined") {
        if (typeof arguments.callee.aciveXString != "string")
            for (e = ["MSXML2.XMLHttp.6.0", "MSXML2.XMLHttp.3.0", "MSXML2.XMLHttp"], f = 0, l = e.length; f < l; f++)
                try {
                    i = new ActiveXObject(e[f]);
                    arguments.callee.activeXString = e[f];
                    break
                } catch (a) {
                }
        i == null && (i = new ActiveXObject(arguments.callee.activeXString))
    }
    i.onreadystatechange = function () {
        try {
            if (i.readyState == 4)
                if (i.status >= 200 && i.status < 300 || i.status == 304) {
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
    /*=====================rk值======================*/
    h = r.indexOf("rk=") >= 0 || r.indexOf("rt=") >= 0 ? u.splice(u.length - 2, 1)[0] : u.pop();
    /* ==================CK值======================*/
    u.push("CK=");
    h = h.split("=")[1];
    var fn = (function (u, r, k, t) {
        var p46 = 1, Z46p = 1;
        p46 = p46 -= parseInt(Math.cos(4) * 0xa);
        p46 = p46 *= parseInt(Math.cos(4) * 0xa);
        p46 = p46 -= parseInt(Math.tan(4) * 0xa);
        if (p46 < 0) p46 = -p46;
        while (p46 > 30) p46 = p46 % 10;
        Z46p = Z46p -= parseInt(Math.cos(4) * 0xa);
        Z46p = Z46p *= parseInt(Math.sqrt(4) * 0xa);
        Z46p = Z46p *= parseInt(Math.cos(4) * 0xa);
        if (Z46p < 0) Z46p = -Z46p;
        while (Z46p > 30) Z46p = Z46p % 10;
        (function (r, u, x, y, t, k) {
            if (!window.location.href) {
                return;
            }
            var l = r.split('');
            var c = l.splice(y, 1);
            l.splice(x, 0, c);
            t.open('GET', u.join('&') + l.join('') + '&r=' + k, !0);
            t.send(null);
        })(r, u, p46, Z46p, t, k)
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