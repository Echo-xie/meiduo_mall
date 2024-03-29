var vm = new Vue({
    el: '#app',
    data: {
        common,
        error_name: false,
        error_old_password: false,
        error_check_password: false,
        error_phone: false,
        error_allow: false,
        error_sms_code: false,

        username: '',
        password: '',
        password2: '',
        mobile: '',
        sms_code: '',
        allow: false,

        sms_code_tip: '获取短信验证码',
        sending_flag: false, 			// 正在发送短信标志
        error_name_message: '', 		// 用户名错误提示
        error_phone_message: '', 		// 手机号错误提示
        error_sms_code_message: '' 		// 短信验证码错误
    },

    methods: {
        check_username: function () {
            // 初始化默认为false
            this.error_name = false;
            // 获取输入用户名长度
            let len = this.username.length;
            // 校验用户名长度 -- 不符合
            if (len < 5 || len > 20) {
                // 设置错误信息
                this.error_name_message = '请输入5-20个字符的用户名';
                // 展示错误信息
                this.error_name = true;
                // 函数返回
                return
            }
            // 访问后台判断用户名是否重复
            // 拼接url请求路径
            let url = this.common.host + "vm/username/" + this.username + "/count/"
            // ajax请求
            axios.get(url, {responseType: 'json'})
                .then(response => {
                    if (response.data.count > 0) {
                        this.error_name_message = '用户名已存在';
                        this.error_name = true;
                    }
                })
                .catch(error => {
                    console.log(error.response.data);
                })
        },
        check_pwd: function () {
            this.error_password = false;
            let len = this.password.length;
            if (len < 8 || len > 20) {
                this.error_password = true;
                // 函数返回
                return
            }
        },
        check_cpwd: function () {
            this.error_check_password = false;
            if (this.password !== this.password2) {
                this.error_check_password = true;
                // 函数返回
                return
            }
        },
        check_phone: function () {
            this.error_phone = false;
            let re = /^1[345789]\d{9}$/;
            if (!re.test(this.mobile)) {
                this.error_phone_message = '请输入正确的手机号码';
                this.error_phone = true;
                // 函数返回
                return
            }
            // 访问后台判断手机号码是否重复
            // 拼接url请求路径
            let url = this.common.host + "vm/mobile/" + this.mobile + "/count/"
            // ajax请求
            axios.get(url, {responseType: 'json'})
                .then(response => {
                    if (response.data.count > 0) {
                        this.error_phone_message = '手机号码已存在';
                        this.error_phone = true;
                    }
                })
                .catch(error => {
                    console.log(error.response.data);
                })
        },
        check_sms_code: function () {
            this.error_sms_code = false;
            if (!this.sms_code) {
                this.error_sms_code = true;
                // 函数返回
                return
            }
        },
        check_allow: function () {
            this.error_allow = false;
            if (!this.allow) {
                this.error_allow = true;
                // 函数返回
                return
            }
        },

        // 发送短信验证码功能
        send_sms_code: function () {
            // 如果显示了短信验证码出错提示, 则隐藏它
            this.error_sms_code = false;
            // 正在发送短信, 阻止事件运行
            if (this.sending_flag) {
                // 正在下发短信验证码
                return
            }
            // 获取短信验证码前先检查手机号码是否正常
            this.check_phone();
            // 校验手机号码后判断
            if (this.error_phone) {
                // 短信验证码校验出错
                this.sending_flag = false;
                return
            }
            this.sending_flag = true;  // 表示正在等待服务器下发短信

            // 拼接url请求路径
            let url = this.common.host + "vm/sms_code/" + this.mobile + "/";
            // ajax请求
            axios.get(url)
                .then(response => {
                    console.log('获取短信验证码成功');
                    // 倒计时60秒, 60秒后允许用户再次点击发送短信验证码的按钮
                    var num = 60;
                    // 设置一个计时器
                    var t = setInterval(() => {
                        if (num == 1) {
                            // 如果计时器到最后, 清除计时器对象
                            clearInterval(t);
                            // 将点击获取验证码的按钮展示的文本恢复成原始文本
                            this.sms_code_tip = '获取短信验证码';
                            // 将点击按钮的onclick事件函数恢复回去
                            this.sending_flag = false;
                        } else {
                            num -= 1;
                            // 展示倒计时信息
                            this.sms_code_tip = num + '秒';
                        }
                    }, 1000, 60);
                })
                .catch(error => {
                    // 显示出错信息
                    this.error_sms_code = true;
                    this.error_sms_code_message = error.response.data.message;
                    // 将点击按钮的onclick事件函数恢复回去
                    this.sending_flag = false;
                })
        },

        // 注册
        on_submit: function () {
            this.check_username();
            this.check_pwd();
            this.check_cpwd();
            this.check_phone();
            this.check_sms_code();
            this.check_allow();
            if (!this.error_name && !this.error_old_password && !this.error_check_password && !this.error_phone && !this.error_sms_code && !this.error_allow) {
                // alert('注册');
                var data = {
                    username: this.username,
                    password: this.password,
                    password2: this.password2,
                    mobile: this.mobile,
                    sms_code: this.sms_code,
                    allow: this.allow
                };
                axios.post(this.common.host + 'vm/user_register/', data)
                    .then(response => {
                        // 清除之前保存的数据
                        // 清理session级别存储
                        sessionStorage.clear();
                        // 清理本地级别存储
                        localStorage.clear();
                        // 保存用户的登录状态数据 -- 本地级别存储
                        localStorage.token = response.data.token;
                        localStorage.username = response.data.username;
                        localStorage.user_id = response.data.id;
                        // 跳转到首页
                        location.href = '/index.html';
                    })
                    .catch(error => {
                        if (error.response.status === 400) {
                            if ('non_field_errors' in error.response.data) {
                                this.error_sms_code = true;
                                this.error_sms_code_message = error.response.data.non_field_errors[0];
                            } else {
                                alert('注册失败')
                            }
                        } else {
                            alert('注册失败')
                        }
                    })
            }
        }
    }
});
