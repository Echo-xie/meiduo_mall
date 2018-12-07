var vm = new Vue({
    el: '#app',
    // 定义属性
    data: {
        common,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        username: sessionStorage.username || localStorage.username,
        is_show_edit: false,   // 是否显示编辑地址窗口

        provinces: [],      // 省份
        cities: [],			    // 城市
        districts: [],          // 区县
        addresses: [],      // 用户所有的地址

        limit: 0,
        default_address_id: '',
        form_address: {     // 新增或编辑地址时,用户录入的字段信息
            receiver: '',
            province_id: '',
            city_id: '',
            district_id: '',
            place: '',
            mobile: '',
            tel: '',
            email: '',
        },

        error_receiver: false,
        error_place: false,
        error_mobile: false,
        error_email: false,
        editing_address_index: '', // 正在编辑的地址在addresses中的下标，''表示新增地址
        is_set_title: [],
        input_title: ''
    },

    // 初始化界面数据 -- 页面挂载后触发函数
    mounted: function () {
        // 查询所有的省份
        axios.get(this.common.host + 'areas/list/0/', this.common.config)
            .then(response => {
                // 获取省列表
                this.provinces = response.data;
            })
            .catch(error => {
                alert(error.response.data);
            });
        // 查询登陆用户收货地址列表
        axios.get(this.common.host + 'users/addresses/', this.common.config)
            .then(response => {
                // 赋值当前登陆用户所有收货地址列表
                this.addresses = response.data.addresses;
                // 设置收货地址数量上限
                this.limit = response.data.limit;
                // 设置当前登陆用户ID
                this.user_id = response.data.user_id;
                // 设置默认收货地址
                this.default_address_id = response.data.default_address_id;
            })
            .catch(error => {
                console.log(error.response.data);
            })
    },

    // 侦听属性 -- 数据变化就触发函数
    watch: {
        // 省份改变, 获取城市 -- form_address.province_id变化触发函数
        'form_address.province_id': function () {
            // 如果省份ID存在
            if (this.form_address.province_id) {
                // ajax请求
                axios.get(this.common.host + 'areas/list/' + this.form_address.province_id + '/')
                    .then(response => {
                        // 获取城市列表
                        this.cities = response.data;
                        // 清空区县列表
                        this.districts = "";
                    })
                    .catch(error => {
                        console.log(error.response.data);
                        this.cities = [];
                    });
            }
        },
        // 城市改变，获取区县 -- form_address.city_id变化触发函数
        'form_address.city_id': function () {
            // 如果城市ID存在
            if (this.form_address.city_id) {
                // ajax请求
                axios.get(this.common.host + 'areas/list/' + this.form_address.city_id + '/')
                    .then(response => {
                        // 获取区县列表
                        this.districts = response.data;
                    })
                    .catch(error => {
                        console.log(error.response.data);
                        this.districts = [];
                    });
            }
        }
    },

    // 定义方法
    methods: {
        // 退出
        logout: function () {
            sessionStorage.clear();
            localStorage.clear();
            location.href = '/login.html';
        },

        // 清空所有错误
        clear_all_errors: function () {
            this.error_receiver = false;
            this.error_mobile = false;
            this.error_place = false;
            this.error_email = false;
        },

        // 展示新增地址界面
        show_add: function () {
            // 查询收货地址数量
            axios.get(this.common.host + 'users/address/count/', this.common.config)
                .then(response => {
                    // 收货地址总数
                    count = response.data.count;
                    // 如果手术地址总数大于上限
                    if (count >= this.limit) {
                        alert("保存地址数据已达到上限");
                        return;
                    }
                    // 显示新增收货地址
                    this.clear_all_errors();
                    this.editing_address_index = '';
                    this.form_address.receiver = '';
                    this.form_address.province_id = '';
                    this.form_address.city_id = '';
                    this.form_address.district_id = '';
                    this.form_address.place = '';
                    this.form_address.mobile = '';
                    this.form_address.tel = '';
                    this.form_address.email = '';
                    this.is_show_edit = true;
                })
                .catch(error => {
                    alert(error.response.data.message);
                });
        },

        // 展示编辑地址界面
        show_edit: function (index) {
            // 清空所有错误
            this.clear_all_errors();
            // 修改地址下标赋值
            this.editing_address_index = index;
            // 获取当前下标的地址信息
            this.form_address = JSON.parse(JSON.stringify(this.addresses[index]));
            // 显示地市编辑框
            this.is_show_edit = true;
        },

        // 校验收货人
        check_receiver: function () {
            if (!this.form_address.receiver) {
                this.error_receiver = true;
            } else {
                this.error_receiver = false;
            }
        },

        // 校验详细地址
        check_place: function () {
            if (!this.form_address.place) {
                this.error_place = true;
            } else {
                this.error_place = false;
            }
        },

        // 校验手机
        check_mobile: function () {
            var re = /^1[345789]\d{9}$/;
            if (re.test(this.form_address.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile = true;
            }
        },

        // 校验邮箱
        check_email: function () {
            if (this.form_address.email) {
                var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
                if (re.test(this.form_address.email)) {
                    this.error_email = false;
                } else {
                    this.error_email = true;
                }
            }
        },

        // 保存地址
        save_address: function () {
            if (this.error_receiver ||
                this.error_place ||
                this.error_mobile ||
                this.error_email ||
                !this.form_address.province_id ||
                !this.form_address.city_id ||
                !this.form_address.district_id) {
                alert('信息填写有误');
                return
            }
            // 标题设置为收货人
            this.form_address.title = this.form_address.receiver;
            // 如果没有修改地址下标
            if (this.editing_address_index === '') {
                // 新增地址
                axios.post(this.common.host + 'users/addresses/', this.form_address, this.common.config)
                    .then(response => {
                        // 将新地址添加到数组头部
                        this.addresses.splice(0, 0, response.data);
                        this.is_show_edit = false;  // 隐藏弹出窗口
                    })
                    .catch(error => {
                        if (error.response.status == 400) {
                            alert(error.response.data.message);
                        }
                        console.log(error.response);
                    })
            } else { // 有修改地址下标
                // 修改地址
                axios.put(this.common.host + 'users/addresses/' + this.addresses[this.editing_address_index].id + '/', this.form_address, this.common.config)
                    .then(response => {
                        // 修改数据
                        this.addresses[this.editing_address_index] = response.data;
                        this.is_show_edit = false;  // 隐藏弹出窗口
                    })
                    .catch(error => {
                        if (error.response.status == 400) {
                            alert(error.response.data.message);
                        }
                        console.log(error.response);
                    })
            }

        },

        // 删除地址
        del_address: function (index) {
            // 删除ajax请求
            axios.delete(this.common.host + 'users/addresses/' + this.addresses[index].id + "/", this.common.config)
                .then(response => {
                    // 删除收货地址列表中数据
                    this.address = this.addresses.splice(index, 1);
                    //
                    alert("删除成功");
                })
                .catch(error => {
                    alert(error.response.data.message);
                });
        },

        // 设置默认地址
        set_default: function (index) {
            // ajax请求
            axios.put(this.common.host + 'users/addresses/' + this.addresses[index].id + "/status/", {}, this.common.config)
                .then(response => {
                    // 修改默认地址ID
                    this.default_address_id = this.addresses[index].id;
                })
                .catch(error => {
                    alert(error.response.data.message);
                });
        },

        // 展示编辑标题
        show_edit_title: function (index) {
            this.input_title = this.addresses[index].title;
            for (var i = 0; i < index; i++) {
                this.is_set_title.push(false);
            }
            this.is_set_title.push(true);
        },

        // 保存地址标题
        save_title: function (index) {
            if (!this.input_title) {
                alert("请填写标题后再保存！");
            } else {
                axios.put(this.common.host + 'users/addresses/' + this.addresses[index].id + '/title/', {title: this.input_title}, this.common.config)
                    .then(response => {
                        this.addresses[index].title = this.input_title;
                        this.is_set_title = [];
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    })
            }
        },

        // 取消保存地址
        cancel_title: function (index) {
            this.is_set_title = [];
        }
    }
});