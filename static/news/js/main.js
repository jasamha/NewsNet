//刷新验证码
function flashVerifyCode() {
//传递参数的目的是：告诉浏览器这是一次新的请求，不使用缓存的数据展示
    //获取原始的图片地址
    $(".get_pic_code").click(function () {
        console.log("zhang__________");

        let src = $('.get_pic_code').attr('src');//==>/user/image_yzm?1
        //在地址后面加1,再修改图片地址
        console.log("输出了啊" + src);
        $('.get_pic_code').attr('src', src + 1);//==>/user/image_yzm?1111

    });
}

//发送短信验证码
// function sendSMSCode() {
//     // 校验参数，保证输入框有数据填写
//     $(".get_code").click(function () {
//         // $(this).removeAttr("onclick");
//         let mobile = $("#register_mobile").val();
//         if (!mobile) {
//             $("#register-mobile-err").html("请填写正确的手机号！");
//             $("#register-mobile-err").show();
//             // $(".get_code").attr("onclick", "sendSMSCode();");
//             return;
//         }
//         let imageCode = $("#imagecode").val();
//         if (!imageCode) {
//             $("#image-code-err").html("请填写验证码！");
//             $("#image-code-err").show();
//             // $(".get_code").attr("onclick", "sendSMSCode();");
//             return;
//         }
//         // 发送短信验证码
//         $.get('/user/sms_verify', {
//             'mobile': mobile,
//             'yzm': imageCode
//         }, function (data) {
//             if (data.result === 1) {
//                 alert('图片验证码错误');
//             } else if (data.result === 2) {
//                 alert('请查看短信');
//             }
//         });
//     });
//
//
//     //  发送短信验证码
// }

$(function () {
    flashVerifyCode();
    $("#login_out").click(function () {
        $.post("/user/login_out",{
            'csrf_token':$('#csrf_token').val()
        },function (data) {
            if (data.result === 1) {
                $(".user_btns").show();
                $(".user_login").hide();
            }

        })
        // $('.user_btns').hide();
        // $('.user_login').show();
        // $('.lgin_pic').attr('src', '/static/news/images/' + data.avatar);
    });
    // 打开登录框
    $('.login_btn').click(function () {
        $('.login_form_con').show();
    });

    // 点击关闭按钮关闭登录框或者注册框
    $('.shutoff').click(function () {
        $(this).closest('form').hide();
    });

    // 隐藏错误
    $(".login_form #mobile").focus(function () {
        $("#login-mobile-err").hide();
    });
    $(".login_form #password").focus(function () {
        $("#login-password-err").hide();
    });

    $(".register_form #mobile").focus(function () {
        $("#register-mobile-err").hide();
    });
    $(".register_form #imagecode").focus(function () {
        $("#register-image-code-err").hide();
    });
    $(".register_form #smscode").focus(function () {
        $("#register-sms-code-err").hide();
    });
    $(".register_form #password").focus(function () {
        $("#register-password-err").hide();
    });


    // 点击输入框，提示文字上移 TODO 这里有bug
    $('.form_group').on('click focusin', function () {
        $(this).children('.input_tip').animate({
            'top': -5,
            'font-size': 12
        }, 'fast').siblings('input').focus().parent().addClass('hotline');
    });

    // 输入框失去焦点，如果输入框为空，则提示文字下移
    $('.form_group input').on('blur focusout', function () {
        $(this).parent().removeClass('hotline');
        let val = $(this).val();
        if (val === '') {
            $(this).siblings('.input_tip').animate({'top': 22, 'font-size': 14}, 'fast');
        }
    });


    // 打开注册框
    $('.register_btn').click(function () {
        $('.register_form_con').show();
    });


    // 登录框和注册框切换
    $('.to_register').click(function () {
        $('.login_form_con').hide();
        $('.register_form_con').show();
    });

    // 登录框和注册框切换
    $('.to_login').click(function () {
        $('.login_form_con').show();
        $('.register_form_con').hide();
    });

    // 根据地址栏的hash值来显示用户中心对应的菜单
    let sHash = window.location.hash;
    if (sHash !== '') {
        let sId = sHash.substring(1);
        let oNow = $('.' + sId);
        let iNowIndex = oNow.index();
        $('.option_list li').eq(iNowIndex).addClass('active').siblings().removeClass('active');
        oNow.show().siblings().hide();
    }

    // 用户中心菜单切换
    let $li = $('.option_list li');
    let $frame = $('#main_frame');

    $li.click(function () {
        if ($(this).index() === 5) {
            $('#main_frame').css({'height': 900});
        }
        else {
            $('#main_frame').css({'height': 660});
        }
        $(this).addClass('active').siblings().removeClass('active');

    });

    //  登录表单提交
    $(".login_form_con").submit(function (e) {
        e.preventDefault();
        let mobile = $(".login_form #mobile").val();
        let password = $(".login_form #password").val();
        let csrf_token = $('#csrf_token').val();
        console.log(mobile + password);
        if (!mobile) {
            $("#login-mobile-err").show();
            return;
        }

        if (!password) {
            $("#login-password-err").show();
            return;
        }

        // 发起登录请求
        $.post("/user/login", {
            mobile: mobile,
            password: password,
            csrf_token: csrf_token

        }, function (data) {

            if (data.result === 1) {
                alert('请填写完整数据');
            } else if (data.result === 2) {
                alert('mobile错误');
            } else if (data.result === 3) {
                alert('密码错误');
            } else if (data.result === 4) {
                // alert("登陆成功了" + data.result);
                $(".login_form_con").hide();
                //将右上角的用户信息展示出来，并隐藏登录注册div
                $('.user_btns').hide();
                $('.user_login').show();
                $('.lgin_pic').attr('src', '/static/news/images/' + data.avatar);
                $('#user_name').text(data.nick_name);
            }
        })
    });


    //  注册按钮点击
    $(".register_form_con").submit(function (e) {
        // 阻止默认提交操作
        e.preventDefault();

        // 取到用户输入的内容
        let mobile = $("#register_mobile").val();
        let smscode = $("#smscode").val();
        let password = $("#register_password").val();
        //短信验证码中已经验证了图片验证码了
        let imagecode = $("#imagecode").val();
        let csrf_token = $('#csrf_token').val();
        console.log(mobile + password + csrf_token);
        if (!mobile) {
            $("#register-mobile-err").show();
            return;
        }
        if (!smscode) {
            $("#register-sms-code-err").show();
            return;
        }
        if (!password) {
            $("#register-password-err").html("请填写密码!").show();
            return;
        }

        if (password.length < 6) {
            $("#register-password-err").html("密码长度不能少于6位").show();
            return;
        }

        // 发起注册请求
        $.post('/user/register', {
            mobile: mobile,
            image_verify: imagecode,
            password: password,
            sms_verify: smscode,
            csrf_token: csrf_token
        }, function (data) {
            console.log(data.result);
            if (data.result === 1) {
                alert('输入有为空');
            } else if (data.result === 2) {
                alert('图片验证码错误');
            } else if (data.result === 3) {
                alert("短信验证码错误")

            } else if (data.result === 4) {
                alert("请重新检查密码长度")
            } else if (data.result === 5) {
                alert("输入的手机号码已经存在")
                $('.login_form_con').show();
                $('.register_form_con').hide();
            } else if (data.result === 7) {
                alert("数据库访问异常")
            }
            else if (data.result === 8) {
                alert('注册成功');
                $('.login_form_con').show();
                $('.register_form_con').hide();
            }
        });

    })
});

let imageCodeId = "";

//调用该函数模拟点击左侧按钮
function fnChangeMenu(n) {
    let $li = $('.option_list li');
    if (n >= 0) {
        $li.eq(n).addClass('active').siblings().removeClass('active');
        // 执行 a 标签的点击事件
        $li.eq(n).find('a')[0].click()
    }
}

// 发送短信验证码
function sendSMSCode() {
    // 校验参数，保证输入框有数据填写
    $(".get_code").removeAttr("onclick");
    let mobile = $("#register_mobile").val();
    if (!mobile) {
        $("#register-mobile-err").html("请填写正确的手机号！");
        $("#register-mobile-err").show();
        $(".get_code").attr("onclick", "sendSMSCode();");
        return;
    }
    let imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err").html("请填写验证码！");
        $("#image-code-err").show();
        $(".get_code").attr("onclick", "sendSMSCode();");
        return;
    }

    // TODO 发送短信验证码
    $.get('/user/sms_verify', {
        'mobile': mobile,
        'yzm': imageCode
    }, function (data) {
        if (data.result === 1) {
            alert('图片验证码错误_sms_verify');
        } else if (data.result === 2) {
            alert('请查看短信');
        }
    });
}

// 一般页面的iframe的高度是660
// 新闻发布页面iframe的高度是900
function fnSetIframeHeight(num) {
    let $frame = $('#main_frame');
    $frame.css({'height': num});
}

function getCookie(name) {
    let r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function generateUUID() {
    let d = new Date().getTime();
    if (window.performance && typeof window.performance.now === "function") {
        d += performance.now(); //use high-precision timer if available
    }
    let uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        let r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return uuid;
}
