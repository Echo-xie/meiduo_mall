var vm = new Vue({
    // 标签ID
    el: '#app',
    // 属性
    data: {
        host: host,
        error_username: false,
        error_pwd: false,
        error_pwd_message: '请填写密码',
        username: '',
        password: '',
        remember: false
    },
    // 页面挂载时调用
    mounted: function () {
        // jwt令牌
        token_ = localStorage.token;
        // 用户ID
        user_id_ = localStorage.user_id;
        // 用户名
        username_ = localStorage.username;
        if (token_ && user_id_ && username_) {
            this.remember = true
        }
    }
    ,
    // 函数
    methods: {
        // 获取url查询字符串参数值
        get_query_string: function (name) {
            var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
            var r = window.location.search.substr(1).match(reg);
            if (r !== null) {
                return decodeURI(r[2]);
            }
            return null;
        },

        // 检查用户名是否合法
        check_username: function () {
            if (!this.username) {
                this.error_username = true;
            } else {
                this.error_username = false;
            }
        },

        // 检查密码是否合法
        check_pwd: function () {
            if (!this.password) {
                this.error_pwd_message = '请填写密码';
                this.error_pwd = true;
            } else {
                this.error_pwd = false;
            }
        },

        // 表单提交: 执行登录操作
        on_submit: function () {
            // 验证用户名
            this.check_username();
            // 验证密码
            this.check_pwd();
            // 如果验证通过
            if (this.error_username == false && this.error_pwd == false) {
                // ajax post请求 -- 用户登陆
                axios.post(this.host + 'vm/authorizations/', {
                    username: this.username,
                    password: this.password
                })
                    .then(response => {
                        // 使用浏览器本地存储保存token
                        // 清空session级别存储
                        sessionStorage.clear();
                        // 清空本地级别存储
                        localStorage.clear();
                        // 如果记住登陆勾选
                        if (this.remember) {
                            // 记住登录
                            // 进行本地级别存储JWT
                            localStorage.token = response.data.token;
                            localStorage.user_id = response.data.user_id;
                            localStorage.username = response.data.username;
                        } else {
                            // 未记住登录
                            // 进行session级别存储JWT
                            sessionStorage.token = response.data.token;
                            sessionStorage.user_id = response.data.user_id;
                            sessionStorage.username = response.data.username;
                        }
                        // 获取跳转页面路径
                        var return_url = this.get_query_string('next');
                        // 如果没有跳转页面 -- 默认跳转至首页
                        if (!return_url) {
                            return_url = '/index.html';
                        }
                        // 页面跳转
                        location.href = return_url;
                    })
                    .catch(error => {
                        if (error.response.status == 400) {
                            this.error_pwd_message = '用户名或密码错误';
                        } else {
                            this.error_pwd_message = '服务器错误';
                        }
                        this.error_pwd = true;
                    })
            }
        },

        // qq登录
        qq_login: function () {
            let next_ = this.get_query_string("next") || "/";
            axios.get(this.host + "oauth/qq/authorization/?next=" + next_)
                .then(resp => {
                    location.href = resp.data.login_url;
                })
                .catch(error => {
                    console.log(error.response.data);
                })
        }
    }
});
