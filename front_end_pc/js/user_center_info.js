var vm = new Vue({
    el: '#app',
    data: {
        common,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        username: '',
        mobile: '',
        email: '',
        email_active: false,
        set_email: false,
        send_email_btn_disabled: false,
        send_email_tip: '重新发送验证邮件',
        email_error: false,
        histories: []
    },

    mounted: function () {
        // 1. 获取用户个人信息
        axios.get(this.common.host + 'users/detail/', this.common.config)
            .then(response => {
                // 显示用户数据
                this.user_id = response.data.id;
                this.username = response.data.username;
                this.mobile = response.data.mobile;
                this.email = response.data.email;
                this.email_active = response.data.email_active;
                localStorage.token = response.data.token;
            })
            .catch(error => {
                // 未登录，跳转到登录界面
                if (error.response.status == 401 || error.response.status == 403) {
                    location.href = '/login.html?next=/user_center_info.html';
                }
            });

        // 2. 补充请求浏览历史
    },

    methods: {
        // 退出
        logout: function () {
            sessionStorage.clear();
            localStorage.clear();
            location.href = '/login.html';
        },

        check_email: function () {
            var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
            if (re.test(this.email)) {
                this.email_error = false;
            } else {
                this.email_error = true;
            }
        },

        // 保存email
        save_email: function () {
            this.check_email();
            if (!this.email_error) {
                // 提交的表单数据
                let data = {email: this.email}
                axios.put(this.common.host + 'users/email/', data, this.common.config)
                    .then(response => {
                        this.set_email = false;
                        this.send_email_btn_disabled = true;
                        this.send_email_tip = '已发送验证邮件'
                    })
                    .catch(error => {
                        alert(error.data);
                    });
            }
        }
    }
});


