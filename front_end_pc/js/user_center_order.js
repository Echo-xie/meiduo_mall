Vue.filter();
let vm = new Vue({
    el: "#app",
    data: {
        common,
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        // 订单列表
        orders: [],
        // 当前页数
        page: 1,
        // 每页数量
        page_size: 5,
        // 总数量
        count: 0,
        // 字符长度
        maxLen: 15,
    },
    filters: {
        dataFormat: function (value, fmt) {
            let getDate = new Date(value);
            let o = {
                'M+': getDate.getMonth() + 1,
                'd+': getDate.getDate(),
                'h+': getDate.getHours(),
                'm+': getDate.getMinutes(),
                's+': getDate.getSeconds(),
                'q+': Math.floor((getDate.getMonth() + 3) / 3),
                'S': getDate.getMilliseconds()
            };
            if (/(y+)/.test(fmt)) {
                fmt = fmt.replace(RegExp.$1, (getDate.getFullYear() + '').substr(4 - RegExp.$1.length))
            }
            for (let k in o) {
                if (new RegExp('(' + k + ')').test(fmt)) {
                    fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? (o[k]) : (('00' + o[k]).substr(('' + o[k]).length)))
                }
            }
            return fmt;
        },
        ellipsis: function (value) {
            if (!value) return ''
            if (value.length > 35) {
                return value.slice(0, 35) + '...'
            }
            return value
        },
    },
    computed: {
        total_page: function () {  // 总页数
            return Math.ceil(this.count / this.page_size);
        },
        next: function () {  // 下一页
            if (this.page >= this.total_page) {
                return 0;
            } else {
                return this.page + 1;
            }
        },
        previous: function () {  // 上一页
            if (this.page <= 0) {
                return 0;
            } else {
                return this.page - 1;
            }
        },
        page_nums: function () {  // 页码
            // 分页页数显示计算
            // 1.如果总页数<=5
            // 2.如果当前页是前3页
            // 3.如果当前页是后3页,
            // 4.既不是前3页，也不是后3页
            var nums = [];
            if (this.total_page <= 5) {
                for (var i = 1; i <= this.total_page; i++) {
                    nums.push(i);
                }
            } else if (this.page <= 3) {
                nums = [1, 2, 3, 4, 5];
            } else if (this.total_page - this.page <= 2) {
                for (var i = this.total_page; i > this.total_page - 5; i--) {
                    nums.push(i);
                }
            } else {
                for (var i = this.page - 2; i < this.page + 3; i++) {
                    nums.push(i);
                }
            }
            return nums;
        },
    },
    mounted: function () {
        this.get_orders();
    },
    methods: {
        // 获取订单列表
        get_orders: function () {
            axios.get(this.common.host + 'orders/action/', this.common.config)
                .then(response => {
                    this.orders = response.data.results;
                    let orders = this.orders;
                    for (let i = 0; i < orders.length; i++) {
                        for (let j = 0; j < orders[i].ordergoods_set.length; j++) {
                            this.orders[i].ordergoods_set[j].sku.url = '/goods/' + this.orders[i].ordergoods_set[j].sku.id + ".html";
                        }
                    }
                })
                .catch(error => {
                    console.log(error.response.data);
                })
        },
        // 点击页数
        on_page: function (num) {
            if (num != this.page) {
                this.page = num;
                this.get_skus();
            }
        },
        // 去支付
        go_pay: function (order_id) {
            // 发起支付 -- 获取阿里支付url
            axios.get(this.common.host + 'payment/alipay/' + order_id + '/', this.common.config)
                .then(response => {
                    // 跳转到支付宝支付
                    location.href = response.data.alipay_url;
                })
                .catch(error => {
                    console.log(error.response.data);
                })
        },

    },

});