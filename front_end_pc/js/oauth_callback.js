var vm = new Vue({
    el: '#app',
    data: {
        common,
        is_show_waiting: true,

        error_old_password: false,
        error_phone: false,
        error_sms_code: false,
        error_phone_message: '',
        error_sms_code_message: '',

        sms_code_tip: '获取短信验证码',
        sending_flag: false, // 正在发送短信标志

        password: '',
        mobile: '',
        sms_code: '',
        openid: ''    // 加密后的openid
    },

    mounted: function () {
        // 从路径中获取qq重定向返回的code
        let code = this.get_query_string('code');
        axios.get(this.common.host + 'oauth/qq/user/?code=' + code, {withCredentials: true}).then(response => {
            // 如果有token, 表示用户已绑定, 并登录成功
            if (response.data.token) {
                // 保存登录成功的jwt
                sessionStorage.clear();
                localStorage.clear();
                // session级别存储
                sessionStorage.user_id = response.data.user_id;
                sessionStorage.username = response.data.username;
                sessionStorage.token = response.data.token;

                // 获取state跳转页面
                var state = this.get_query_string('state');
                // 跳转
                location.href = state
                // location.href = decodeURIComponent(state);  // url解码
            } else { // 用户未绑定
                // 获取openid
                this.openid = response.data.openid;
                // 显示绑定界面
                this.is_show_waiting = false;
            }
        })
            .catch(error => {
                alert(error.response.data.message);
            })
    },

    methods: {
        // 获取url路径参数
        get_query_string: function (name) {
            var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
            var r = window.location.search.substr(1).match(reg);
            if (r != null) {
                return decodeURI(r[2]);
            }
            return null;
        },

        check_pwd: function () {
            var len = this.password.length;
            if (len < 8 || len > 20) {
                this.error_password = true;
            } else {
                this.error_password = false;
            }
        },
        check_phone: function () {
            var re = /^1[345789]\d{9}$/;
            if (re.test(this.mobile)) {
                this.error_phone = false;
            } else {
                this.error_phone_message = '您输入的手机号格式不正确';
                this.error_phone = true;
            }
        },
        check_sms_code: function () {
            if (!this.sms_code) {
                this.error_sms_code_message = '请填写短信验证码';
                this.error_sms_code = true;
            } else {
                this.error_sms_code = false;
            }
        },


        // 发送手机短信验证码
        send_sms_code: function () {

            // 重新发送短信后，隐藏提示信息
            this.error_sms_code = false;

            if (this.sending_flag) {
                return;
            }
            this.sending_flag = true;

            // 校验参数，保证输入框有数据填写
            this.check_phone();

            if (this.error_phone) {
                this.sending_flag = false;
                return;
            }

            // 向后端接口发送请求，让后端发送短信验证码
            axios.get(this.common.host + 'vm/sms_code/' + this.mobile + '/')
                .then(response => {
                    // 表示后端发送短信成功
                    // 倒计时60秒，60秒后允许用户再次点击发送短信验证码的按钮
                    var num = 60;
                    // 设置一个计时器
                    var t = setInterval(() => {
                        if (num == 1) {
                            // 如果计时器到最后, 清除计时器对象
                            clearInterval(t);
                            // 将点击获取验证码的按钮展示的文本回复成原始文本
                            this.sms_code_tip = '获取短信验证码';
                            // 将点击按钮的onclick事件函数恢复回去
                            this.sending_flag = false;
                        } else {
                            num -= 1;
                            // 展示倒计时信息
                            this.sms_code_tip = num + '秒';
                        }
                    }, 1000, 60)
                })
                .catch(error => {
                    if (error.response.status == 400) {
                        // 展示发送短信错误提示
                        this.error_sms_code = true;
                        this.error_sms_code_message = error.response.data.message;
                    } else {
                        console.log(error.response.data);
                    }
                    this.sending_flag = false;
                })
        },


        // 绑定open_id和美多用户
        on_submit: function () {
            // 检测表单
            this.check_pwd();
            this.check_phone();
            this.check_sms_code();
            // 检测通过
            if (!this.error_old_password && !this.error_phone && !this.error_sms_code) {
                // 发请求绑定openid和美多用户
                axios.post(this.common.host + 'oauth/qq/user/', {
                    password: this.password,
                    mobile: this.mobile,
                    sms_code: this.sms_code,
                    openid: this.openid
                }, {withCredentials: true})
                    .then(response => {
                        // 绑定成功，即登录成功，需要记录用户登录状态
                        sessionStorage.clear();
                        localStorage.clear();
                        sessionStorage.token = response.data.token;
                        sessionStorage.user_id = response.data.user_id;
                        sessionStorage.username = response.data.username;

                        // QQ登录成功，跳转到指定界面
                        location.href = this.get_query_string('state');
                    })
                    .catch(error => {
                        if (error.response.status == 400) {
                            this.error_sms_code_message = error.response.data.message;
                            this.error_sms_code = true;
                        } else {
                            console.log(error.response.data);
                        }
                    })
            }

        }
    }
});
