var vm = new Vue({
    el: '#app',
    data: {
        common,
        username: sessionStorage.username || localStorage.username,
        user_id,
        token,
        skus: [],
        freight: 0,               // 运费
        total_count: 0,
        total_amount: 0,
        payment_amount: 0,
        order_submitting: false, // 正在提交订单标志
        pay_method: 1,           // 支付方式,
        nowsite: 0,              // 默认地址
        addresses: []
    },

    mounted: function () {
        // 获取地址信息
        axios.get(this.common.host + 'users/addresses/', this.common.config)
            .then(response => {
                this.addresses = response.data.addresses;
                this.nowsite = response.data.default_address_id;
            })
            .catch(error => {
                status = error.response.status;
                if (status == 401 || status == 403) {
                    location.href = 'login.html?next=/user_center_site.html';
                } else {
                    alert(error.response.data.detail);
                }
            })

        // 获取结算商品信息
        axios.get(this.common.host + 'orders/settlement/', this.common.config)
            .then(response => {
                this.skus = response.data.skus;
                this.freight = response.data.freight;
                this.total_count = 0;
                this.total_amount = 0;
                for (var i = 0; i < this.skus.length; i++) {
                    var amount = parseFloat(this.skus[i].price) * this.skus[i].count;
                    this.skus[i].amount = amount.toFixed(2);
                    this.total_count += this.skus[i].count;
                    this.total_amount += amount;
                }
                this.payment_amount = parseFloat(this.freight) + this.total_amount;
                this.payment_amount = this.payment_amount.toFixed(2);
                this.total_amount = this.total_amount.toFixed(2);
            })
            .catch(error => {
                if (error.response.status == 401) {
                    location.href = '/login.html?next=/cart.html';
                } else {
                    console.log(error.response.data);
                }
            })
    },

    methods: {
        // 退出
        logout: function () {
            sessionStorage.clear();
            localStorage.clear();
            location.href = '/login.html';
        },

        // 提交订单
        on_order_submit: function () {
            if (this.order_submitting == false) {
                this.order_submitting = true;
                let data_ = {
                    address: this.nowsite,
                    pay_method: this.pay_method
                };
                axios.post(this.common.host + 'orders/action/', data_, this.common.config)
                    .then(response => {
                        location.href = '/order_success.html?order_id=' + response.data.order_id
                            + '&amount=' + this.payment_amount
                            + '&pay=' + this.pay_method;
                    })
                    .catch(error => {
                        this.order_submitting = false;
                        alert(error.response.data[0]);
                    })
            }
        }
    }
});