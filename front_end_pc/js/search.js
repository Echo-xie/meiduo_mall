var vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'], // 修改vue模板符号，防止与django冲突
    data: {
        common,
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        page: 1,        // 当前页数
        page_size: 6,   // 每页数量
        count: 0,       // 总数量
        skus: [],       // 数据
        query: '',      // 查询关键字
        cart_total_count: 0, // 购物车总数量
        cart: [],       // 购物车数据
        cart_goods_show: false,  // 购物车商品显示控制
    },

    computed: {
        // 总页数
        total_page: function () {
            return Math.ceil(this.count / this.page_size);
        },

        // 下一页
        next: function () {
            if (this.page >= this.total_page) {
                return 0;
            } else {
                return this.page + 1;
            }
        },

        // 上一页
        previous: function () {
            if (this.page <= 0) {
                return 0;
            } else {
                return this.page - 1;
            }
        },

        // 页码
        page_nums: function () {
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
        }
    },

    mounted: function () {
        this.query = this.get_query_string('q');
        this.get_search_result();
        this.get_cart();
    },

    methods: {
        logout() {
            sessionStorage.clear();
            localStorage.clear();
            location.href = '/login.html';
        },

        // 获取url路径参数
        get_query_string: function (name) {
            var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
            var r = window.location.search.substr(1).match(reg);
            if (r != null) {
                return decodeURI(r[2]);
            }
            return null;
        },

        // 请求查询结果
        get_search_result: function () {
            axios.get(this.common.host + 'goods/skus_search/', {
                params: {
                    text: this.query,
                    page: this.page,
                    page_size: this.page_size,
                },
                responseType: 'json'
            })
                .then(response => {
                    this.count = response.data.count;
                    this.skus = response.data.results;
                    for (var i = 0; i < this.skus.length; i++) {
                        this.skus[i].url = '/goods/' + this.skus[i].id + ".html";
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
                this.get_search_result();
            }
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