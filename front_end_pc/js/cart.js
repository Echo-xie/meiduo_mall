var vm = new Vue({
    el: '#app',
    data: {
        common,
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        cart: [],					// 购物车中所有的商品
        total_selected_count: 0,
        origin_input: 0     // 用于记录手动输入前的值
    },

    computed: {
        // 商品总数量
        total_count: function () {
            var total = 0;
            for (var i = 0; i < this.cart.length; i++) {
                total += parseInt(this.cart[i].count);
				//  计算每件商品的小计金额: 小计金额 = 单价 * 数量
                this.cart[i].amount = (parseFloat(this.cart[i].price)
                    * parseFloat(this.cart[i].count)).toFixed(2); // 保留两位小数
            }
            return total;
        },

        // 选中商品的总金额
        total_selected_amount: function () {
            var total = 0;
            this.total_selected_count = 0;
            for (var i = 0; i < this.cart.length; i++) {
                if (this.cart[i].selected) {
                    total += (parseFloat(this.cart[i].price) * parseFloat(this.cart[i].count));
                    this.total_selected_count += parseInt(this.cart[i].count);
                }
            }
            return total.toFixed(2); // 保留两位小数
        },

        // 当前全选按钮是否为勾选状态
        selected_all: function () {
            var selected = true;
            for (var i = 0; i < this.cart.length; i++) {
                if (this.cart[i].selected == false) {
                    selected = false;   // 只要有一个商品没有勾选,全选按钮就不打勾
                    break;
                }
            }
            return selected;
        }
    },

    mounted: function () {
        // 获取购物车数据
        
    },

    methods: {
        // 点击了退出
        logout: function () {
            sessionStorage.clear();
            localStorage.clear();
            location.href = '/login.html';
        },

        // 点击减少商品数量
        on_minus: function (index) {
            if (this.cart[index].count > 1) {
                var count = this.cart[index].count - 1;
                this.update_count(index, count);
            }
        },

        // 点击增加商品数量
        on_add: function (index) {
            var count = this.cart[index].count + 1;
            this.update_count(index, count);
        },

        // 全选商品
        on_selected_all: function () {
            var selected = !this.selected_all;
           
        },

        // 删除购物车商品
        on_delete: function (index) {

        },

        // 手动输入商品数量
        on_input: function (index) {
            var val = parseInt(this.cart[index].count);
            if (isNaN(val) || val <= 0) {
                this.cart[index].count = this.origin_input;
            } else {
                // 更新购物车数据
            }
        },

        // 更新购物车数量
        update_count: function (index, count) {

        },

        // 更新购物车选中状态
        update_selected: function (index) {

        }
    }
});