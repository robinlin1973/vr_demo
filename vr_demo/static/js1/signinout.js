
function isValidEmail(n) {
    var t = new RegExp(/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i);
    return t.test(n)
}

function isValidUser(n) {
    return !(n.indexOf("|") > -1)
}

function showwaitverification() {
    $("#btnResendVerify").prop("disabled", !0);
    $("#btnResendVerify").undoCountdown({
        seconds: 120,
        term: lang.confirmemail,
        onComplete: function() {
            $("#btnResendVerify").removeAttr("disabled");
            $("#btnResendVerify").html(lang.confirmemailagain)
        }
    })
}

SecurityManager = {
    sendresetpwd: function(n) {
        showresetwaiting(0);
        var t = getRequestUri() + "sendforgot?username=" + n;
        $.ajax({
            type: "GET",
            url: t
        }).done(function() {
            showresetwaiting(1);
            alert(lang.resetpwd)
        }).fail(function() {
            showresetwaiting(1)
        })
    },
    checkactive: function() {
        showwaitverification();
        var n = getRequestUri() + "getaccountactive";
        $.ajax({
            type: "GET",
            url: n
        }).done(function(n) {
            n == "1" && setStoreValue("active", "1")
        }).fail(function() {})
    },
    checkprime: function() {
        var t = !0,
            n = getCurrentNZTime(),
            r = n.getFullYear().toString() + (n.getMonth() + 1).toString() + n.getDate().toString(),
            i;
        getStoreValue("prime") != null && getStoreValue("prime") == r && (t = !1);
        t && (removeStoreValue("prime"), i = getRequestUri() + "getaccountprime", $.ajax({
            type: "GET",
            url: i
        }).done(function(n) {
            n != null && n != "" && setStoreValue("prime", n)
        }).fail(function() {}))
    },
    submitcode: function(n) {
        var t = getRequestUri() + "submitauthcode?code=" + n;
        $.ajax({
            type: "GET",
            url: t
        }).done(function(n) {
            n != null && n != "" ? (setStoreValue("prime", n), finishloading(lang.lblcodedone)) : finishloadingerror(lang.lblnocode)
        }).fail(function() {})
    },
    sendverify: function() {
        showwaitverification();
        var n = getRequestUri() + "verifyaccount";
        $.ajax({
            type: "GET",
            url: n
        }).done(function() {}).fail(function() {})
    },
    register: function(n, t, i, r) {
        showloginwaiting(0);
        var u = getRequestUri() + "registeraccount?username=" + n + "&password=" + t + "&email=" + i + "&fcode=" + r;
        $.ajax({
            type: "POST",
            url: u
        }).done(function(n) {
            showloginwaiting(1);
            $("#loginregscreen").hide();
            $("#diverrorreg").hide();
            $("#username").val("");
            $("#password").val("");
            setStoreValue("guid", n.split("|")[0]);
            setStoreValue("uname", $("#registerusername").val());
            $("#progresssreginfo").hide();
            n.split("|").length > 1 ? (showwaitverification(), $("#pnlRegisteredActivate").show()) : (setStoreValue("active", "1"), $("#pnlRegistered").show())
        }).fail(function(n, t, i) {
            showloginwaiting(1);
            $("#loginregscreen").show();
            $("#progresssreginfo").hide();
            i.toString() == "Found" ? ($("#regerrmsg").html(n.responseText.replace(/\"/g, "")), $("#diverrorpwd").show()) : ($("#regerrmsg").html("Error!"), $("#diverrorpwd").show())
        })
    },
    login: function(n, t) {
        showloginwaiting(0);
        var i = getRequestUri() + "loginaccount?username=" + n + "&password=" + t;
        $.ajax({
            type: "POST",
            url: i
        }).done(function(n) {
            setStoreValue("guid", n.split("|")[0]);
            setStoreValue("uname", n.split("|")[1]);
            n.split("|").length > 2 && setStoreValue("active", 1);
            reloadPage()
        }).fail(function(n, t, i) {
            showloginwaiting(1);
            i.toString() == "Unauthorized" ? ($("#loginerrmsg").html(lang.loginerror), $("#diverrorlogin").show()) : ($("#loginerrmsg").html(lang.syserror), $("#diverrorlogin").show())
        })
    },
    loginexternal: function(n, t) {
        showloginwaiting(0);
        var i = getRequestUri() + "loginexternal?accessToken=" + n + "&source=" + t;
        $.ajax({
            type: "POST",
            url: i
        }).done(function(n) {
            setStoreValue("guid", n.split("|")[0]);
            setStoreValue("uname", n.split("|")[1]);
            setStoreValue("externallogin", t);
            n.split("|").length > 2 && setStoreValue("active", 1);
            reloadPage()
        }).fail(function(n, t, i) {
            showloginwaiting(1);
            i.toString() == "Unauthorized" ? ($("#loginerrmsg").html(lang.loginerror), $("#diverrorlogin").show()) : ($("#loginerrmsg").html(lang.syserror), $("#diverrorlogin").show())
        })
    }
};


function showloginwaiting(n) {
    n == 0 ? ($(".loadingReg").show(), $(".regscreen").find("input,select,textarea,button").prop("disabled", !0)) : ($(".loadingReg").hide(), $(".regscreen").find("input,select,textarea,button").prop("disabled", !1))
}

function getRequestUri() {
    return $("#baseRequestAddr").val()
}

function getRequestUriheader() {
    var n = new Date,
        t = n.getUTCDate() + n.getUTCMonth() + 1;
    return Sha1.hash($("#sessionId").val().substring(0, 5) + t.toString())
}

function getRequestUriheaderpub() {
    var n = new Date,
        t = n.getUTCDate() * 2 + n.getUTCMonth() + 1;
    return Sha1.hash($("#sessionId").val().substring(0, 7) + t.toString())
}

$("#login-form-link").click(function(n) {
    $("#login-form").delay(100).fadeIn(100);
    $("#register-form").fadeOut(100);
    $("#register-form-link").removeClass("active");
    $(this).addClass("active");
    n.preventDefault()
});

$("#register-form-link").click(function(n) {
    $("#register-form").delay(100).fadeIn(100);
    $("#login-form").fadeOut(100);
    $("#login-form-link").removeClass("active");
    $(this).addClass("active");
    n.preventDefault()
});

$("#chxcheckagree").click(function() {
    $(this).is(":checked") ? $("#btnregbuttonloginmodel").removeAttr("disabled") : $("#btnregbuttonloginmodel").attr("disabled", !0)
});

var poolData = { UserPoolId : 'us-east-2_kRoPjEqA4',
    ClientId : '74j09n3pu351l77dkqise15i8o'
};

//var CognitoUserPool = AmazonCognitoIdentity.CognitoUserPool;
//var CognitoUser = AmazonCognitoIdentity.CognitoUser;
//var AuthenticationDetails = AmazonCognitoIdentity.AuthenticationDetails;

function registerclick() {
    $("#diverrorpwd").hide();

    if (!isValidEmail($("#registeremail").val())){
        $("#regerrmsg").html("Email Address Error!");
        $("#diverrorpwd").show();
        return
    }

    if (!isValidUser($("#registerusername").val())){
        $("#regerrmsg").html("User Name Error!");
        $("#diverrorpwd").show();
        return
    }

    if ($("#registerpassword").val() != $("#confirmpassword").val()){
        $("#regerrmsg").html("Password not matching!");
        $("#diverrorpwd").show();
        return
    }

    var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
    var attributeList = [];
    var email = $("#registeremail").val();
    var username = $("#registerusername").val();
    var password = $("#registerpassword").val();

    var dataEmail = {
        Name : 'email',
        Value : email
    };

    var attributeEmail = new AmazonCognitoIdentity.CognitoUserAttribute(dataEmail);

    attributeList.push(attributeEmail);

    userPool.signUp(username, password, attributeList, null, function(err, result){
        if (err) {
//            alert(JSON.stringify(err));
            $("#regerrmsg").html(err["message"]);
            $("#diverrorpwd").show();
            return;
        }else{
            alert("check the mail");
            cognitoUser = result.user;
            console.log('user name is ' + cognitoUser.getUsername());
        }
    });


    return;
}

function loginclick() {
    $("#diverrorlogin").hide();
    var username = $("#username").val();
    var password = $("#password").val();

    var authenticationData = {
        Username : username,
        Password : password,
    };
    var authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails(authenticationData);

    var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
    var userData = {
        Username : username,
        Pool : userPool
    };
    var cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
    cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: function (result) {
            var accessToken = result.getAccessToken().getJwtToken();
//            alert(JSON.stringify(result));
            window.location.replace("/");
            /* Use the idToken for Logins Map when Federating User Pools with identity pools or when passing through an Authorization Header to an API Gateway Authorizer*/
            var idToken = result.idToken.jwtToken;
        },

        onFailure: function(err) {
//            alert(JSON.stringify(err));
            $("#loginerrmsg").html(err["message"]);
//            $("#loginerrmsg").html(JSON.stringify(err));
            $("#diverrorlogin").show();
        },
    });
}

function setUserName(){
    var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
    var cognitoUser = userPool.getCurrentUser();

    if (cognitoUser != null) {
        cognitoUser.getSession(function(err, session) {
            if (err) {
                alert(err);
                return;
            }
            console.log(cognitoUser.signInUserSession.accessToken.jwtToken);
            $('#profile').replaceWith(cognitoUser.username);
        });
    }
}

function getUserName(){
    var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
    var cognitoUser = userPool.getCurrentUser();

    if (cognitoUser != null) {
        cognitoUser.getSession(function(err, session) {
            if (err) {
                alert(err);
                return;
            }
            console.log(cognitoUser.signInUserSession.accessToken.jwtToken);
            $('#profile').replaceWith(cognitoUser.username);
            $('#sign').replaceWith("");
            return cognitoUser.username;
        });
    }

    $('#profile').replaceWith("");
    $('#sign').replaceWith("SignIn/Up");
}

$(".loginpopover").popover({
    html: !0,
    trigger: "manual",
    content: function() {
        return $("#popover-content").html()
    }
}).click(function(n) {
    $(this).popover("show");
    clickedAway = !1;
    isVisible = !0;
    n.preventDefault()
});
$(document).click(function() {
    isVisible & clickedAway ? ($(".loginpopover").popover("hide"), isVisible = clickedAway = !1) : clickedAway = !0
})

function logingoff() {
    var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
    var cognitoUser = userPool.getCurrentUser();

    if (cognitoUser != null) {
        cognitoUser.signOut();
        window.location.replace("/");
//        $('#profile').replaceWith("");
//        $('#sign').replaceWith("SignIn/Up");
    }
}