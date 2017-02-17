require.config({
    paths: {
        "jquery": "/jslib/jquery-1.11.0.min"
    },
    shim: {
        //'knockout': {
        //    deps: ['knockout-json2']
        //}
    }
});
define(["jquery"], function ($) {
    var dt = function (par) {
        par = par ? par : {};
        var _this = this;
        if (par.dom) {
            par.dom.on("click", function () {
                _this.show();
            });
        };
        if (par.v) {
            this.v = job.d(par.v);
        }
        if (par.call) {
            this.call = par.call;
        }
    };
    dt.prototype.show = function () {
        var _this = this;
        if (!this.m) {
            dt.N + 10;
            this.m = $("<div class=\"mydt\" style=\"display:none;z-index:" + (10001 + dt.N) + "\"><div class=\"tb-tit\"><a class=\"tb-left tb-dre\" href=\"javascript:void(0)\">&lt;</a><h2><a class=\"tb-tit-con\" href=\"javascript:void(0)\"><label></label><span></span></a></h2><a class=\"tb-right tb-dre\" href=\"javascript:void(0)\">&gt;</a></div><div class=\"tb-con\"><table class=\"tb-con-a\"><thead><tr><th>日</th><th>一</th><th>二</th><th>三</th><th>四</th><th>五</th><th>六</th></tr></thead><tbody></tbody></table><table class=\"tb-con-sel\"></table></div><div class=\"tb-dir\"><div></div>").appendTo($(document.body));
            this.layer = $("<div class=\"mydt-layer\" style=\"display:none;z-index:" + (10000 + dt.N) + "\"></div>").appendTo($(document.body));
            this.layer.on("click", function () {
                _this.hide();
            });
            var mode = "a";
            this.m.find(".tb-tit .tb-tit-con").on("click", function () {//sel click
                var mcon = _this.m.find(".tb-con-a");
                if (_this.mode == "a") {
                    _this.initMonth();
                    _this.mode = "b";
                    mcon.hide();
                } else if (_this.mode == "b") {
                    _this.initYear(_this.now.getFullYear() - _this.now.getFullYear() % 10);
                    _this.mode = "c";
                }
            });
            this.m.find(".tb-tit .tb-left").on("click", function () {//left click
                if (_this.mode == "a") {
                    _this.now.setMonth(_this.now.getMonth() - 1);
                    _this.init(_this.now);
                } else if (_this.mode == "b") {
                    _this.now.setFullYear(_this.now.getFullYear() - 1);
                    _this.initMonth();
                } else if (_this.mode == "c") {
                    _this.initYear(_this.m.fromYear - 10);
                }
            });
            this.m.find(".tb-tit .tb-right").on("click", function () {//right click
                if (_this.mode == "a") {
                    _this.now.setMonth(_this.now.getMonth() + 1);
                    _this.init(_this.now);
                } else if (_this.mode == "b") {
                    _this.now.setFullYear(_this.now.getFullYear() + 1);
                    _this.initMonth();
                } else if (_this.mode == "c") {
                    _this.initYear(_this.m.fromYear + 10);
                }
            });
            var tody = $("<a href=\"javascript:void(0)\">今天</a>").appendTo(this.m.find(".tb-dir"));
            tody.on("click", function () {
                _this.setV(new Date);
                var tody = _this.m.find(".tb-con-a tbody td.istody a");
                tody.className = "on";

            });
            $(window).resize(function () {
                _this.setPosition();
            });
            this.init(job.dnew(this.v) || new Date());
        } else {
            if (this.mode != "a") {
                this.m.find(".tb-con-a").show();
                this.m.find(".tb-con-sel").hide();
                this.mode = "a";
            };
            if (this.v) {
                if (this.v.getFullYear() != this.now.getFullYear() || this.v.getMonth() != this.now.getMonth()) {
                    this.init(job.dnew(this.v));
                }
            }
        }
        this.layer.show();
        this.m.show();
        this.setPosition();
    };
    dt.N = 1;
    dt.prototype.hide = function () {
        this.layer.hide();
        this.m.hide();
    };
    dt.prototype.setTit = function (y, m) {
        this.m.find(".tb-tit .tb-tit-con span").html(y || '');
        this.m.find(".tb-tit .tb-tit-con label").html(m || '');
    };
    dt.prototype.mode = "a";
    dt.prototype.initMonth = function () {
        var _this = this;
        var con = this.m.find(".tb-con-sel");
        con.html("");
        var n = 1;
        for (var i = 0; i < 3; i++) {
            var tr = $("<tr></tr>").appendTo(con);
            for (var j = 0; j < 4; j++) {
                var nclass = (this.v && this.now.getFullYear() == this.v.getFullYear() && n == this.v.getMonth() + 1) ? "on" : "cur";
                var td = $("<td><a href=\"javascript:void(0)\" class=\"" + nclass + "\" >" + n + "月</a></td>").appendTo(tr);
                (function (month) {
                    td.find("a").on("click", function () {
                        con.hide();
                        _this.init(new Date(_this.now.getFullYear() + "/" + month + "/" + _this.now.getDate()));
                        _this.mode = "a";
                    })
                })(n);
                n += 1;
            }
        };
        con.show();
        this.setTit(this.now.getFullYear(), "");//set title
    };
    dt.prototype.initYear = function (from) {
        var _this = this;
        var con = this.m.find(".tb-con-sel");
        this.m.fromYear = from;
        con.html("");
        var n = from;//this.now.getFullYear() - this.now.getFullYear() % 10;
        var str = n + "-" + (n + 11);
        for (var i = 0; i < 3; i++) {
            var tr = $("<tr></tr>").appendTo(con);
            for (var j = 0; j < 4; j++) {
                var nclass = (this.v && n == this.v.getFullYear()) ? "on" : "cur";
                var td = $("<td><a href=\"javascript:void(0)\" class=\"" + nclass + "\" >" + n + "</a></td>").appendTo(tr);
                (function (year) {
                    td.find("a").on("click", function () {
                        _this.now = new Date(year + "/" + (_this.now.getMonth() + 1) + "/" + _this.now.getDate());
                        _this.mode = "b";
                        _this.initMonth();
                    })
                })(n);
                n += 1;
            }
        };
        con.show();
        this.setTit(str, "");
    };
    dt.prototype.now;
    dt.prototype.init = function (d) {
        var _this = this;
        this.now = d;
        this.setTit(d.getFullYear(), (d.getMonth() + 1) + "月");
        var _d = new Date(d.getFullYear() + "/" + (d.getMonth() + 1) + "/1");//副本
        var wk = _d.getDay();
        _d.setDate(wk == 0 ? -6 : 1 - wk);
        var con = this.m.find(".tb-con-a tbody");
        con.html("");
        for (var i = 0; i < 6; i++) {
            var tr = $("<tr></tr>").appendTo(con);
            for (var j = 0; j < 7; j++) {
                var dclass = (_d.getMonth() == d.getMonth()) ? "cur" : "otr";
                var nclass = (this.v && _d.getFullYear() == this.v.getFullYear() && _d.getMonth() == this.v.getMonth() && _d.getDate() == this.v.getDate()) ? "on" : dclass;
                var tody = new Date();
                var istody = (_d.getFullYear() == tody.getFullYear() && _d.getMonth() == tody.getMonth() && _d.getDate() == tody.getDate());
                var td = $("<td><a href=\"javascript:void(0)\" class=\"" + nclass + "\" oldclass=\"" + dclass + "\">" + _d.getDate() + "</a></td>").appendTo(tr);
                if (istody) {
                    td.addClass("istody");
                }
                (function (_dd) {
                    td.find("a").on("click", function () {
                        _this.setV(_dd);
                        this.className = "on";
                    })
                })(job.dnew(_d));
                _d.setDate(_d.getDate() + 1);
            }
        }
        this.m.find(".tb-con-a").show();
    };
    dt.prototype.setV = function (_dd) {
        this.v = _dd;
        var old = this.m.find(".tb-con-a tbody td a.on");
        old.removeClass("on");
        old.addClass(old.attr("oldclass"));
        if (this.call) {
            this.call(_dd.getFullYear() + "-" + (_dd.getMonth() + 1) + "-" + _dd.getDate());
        }
        this.hide();
    };
    dt.prototype.setPosition = function () {
        var winW = $(window).width();//窗口宽
        var winH = $(window).height();//窗口高
        var l = (winW - this.m.width()) / 2; l = l < 0 ? 0 : l;
        var t = (winH - this.m.height()) / 2; t = t < 0 ? 0 : t;
        this.m.css("left", l + "px");
        this.m.css("top", t + "px");
        this.layer.css("height", winH + "px");
    };
    $("<style type=\"text/css\">.mydt { width: 400px; background: #fff; position: fixed; padding:5px; border-radius: 3px; box-shadow: 2px 2px 8px 2px #555; }" +
       " .mydt .tb-tit { position: relative; padding: 0 0 3px; height: 40px; }" +
       " .mydt .tb-tit a { display: block; text-align: center; }" +
       " .mydt .tb-tit h2 { margin: 0 40px; height: 40px; line-height: 40px; }" +
".mydt .tb-tit h2 .tb-tit-con { background-color: #f6f6f6; border-radius: 3px; cursor: pointer; height: 100%; }" +
".mydt .tb-tit h2 .tb-tit-con label { font-size: 22px; padding: 0 10px 0 0; cursor: pointer; }" +
".mydt .tb-tit h2 .tb-tit-con span { font-size: 17px; }" +
".mydt .tb-tit h2 .tb-tit-con:hover { background-color: #f0f0f0; }" +
".mydt .tb-tit .tb-dre {  top: 2px; position: absolute; width: 36px; height: 36px; line-height: 36px; font-weight:bolder; font-size:30px; border-radius:3px; }" +
".mydt .tb-tit .tb-dre:hover { text-decoration:none; background-color:#e0e0e0; }" +
".mydt .tb-tit .tb-left { left: 2px;}" +
".mydt .tb-tit .tb-right { right: 2px;}" +
".mydt table { width: 100%; border-collapse: collapse; }" +
".mydt table th { background-color: #e6e6e6; padding: 8px 0; border: 1px solid #dcdcdc; }" +
".mydt table td { text-align: center; border: 1px solid #dcdcdc; }" +
".mydt table td a { display: block; text-decoration: none; cursor: pointer; }" +
".mydt .tb-con-a td a{ height:48px; line-height:48px; }" +
".mydt .tb-con-sel td { width:25%;}" +
".mydt .tb-con-sel td a{  height:90px; line-height:90px;}" +
".mydt table td a:hover { background-color: #f0f0f0; }" +
".mydt table td .otr { color: #ccc; }" +
".mydt table td .cur { color: #333; }" +
".mydt table td .on {background-color:#3276b1; color:#fff; font-weight:bold; box-shadow:0 0 8px 1px #666;border-radius:5px; }" +
".mydt table td a.on:hover { background-color: #3276b1;color:#fff; }" +
".mydt-layer { position: fixed; width: 100%; left: 0; top: 0; background: #000; opacity: 0.3; }" +
".mydt .tb-dir { padding:3px 0 0;}" +
".mydt .tb-dir a { display: block; border-radius: 3px; height:30px; line-height:30px; text-align:center; font-weight:bold;}" +
".mydt .tb-dir a:hover {background-color: #f0f0f0; }</style>").appendTo($(document.head));
    var job = {
        isDate: function (str) {
            var reg_a = new RegExp("^([0-9]{4})[\/\-]([0-9][0-9]?)[\/\-]([0-9][0-9]?)$");
            return reg_a.test(str);
        },
        dnew: function (date) {
            return new Date(date.getFullYear() + "/" + (date.getMonth() + 1) + "/" + date.getDate());
        },
        d: function (str) {//字符串转日期
            str = str.replace(/\-/gi, "/");
            return new Date(str);
        },
        cre: function (par) {
            return new dt(par);
        }
    }
    return job;
});