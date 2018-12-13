var vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        common,
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        cart_total_count: 0, // 购物车总数量
        cart: [], // 购物车数据,
        cart_goods_show: false,  // 购物车商品显示控制
        f1_tab: 1, // 1F 标签页控制
        f2_tab: 1, // 2F 标签页控制
        f3_tab: 1, // 3F 标签页控制
    },

    mounted: function () {
        this.get_cart();
    },

    methods: {
        // 退出
        logout: function () {
            sessionStorage.clear();
            localStorage.clear();
            location.href = '/login.html';
        },
        // 获取购物车数据
        get_cart: function () {
            axios.get(this.common.host + 'carts/action/', this.common.config)
                .then(response => {
                    this.cart = response.data;
                    if (this.cart.length <= 0) {
                        this.cart_goods_show = false;
                        return;
                    }
                    this.cart_goods_show = true;
                    this.cart_total_count = 0;
                    for (var i = 0; i < this.cart.length; i++) {
                        if (this.cart[i].name.length > 25) {
                            this.cart[i].name = this.cart[i].name.substring(0, 25) + '...';
                        }
                        this.cart_total_count += this.cart[i].count;
                        this.cart[i].url = '/goods/' + this.cart[i].id + ".html";

                    }
                })
                .catch(error => {
                    console.log(error.response.data);
                })
        },
    }
});