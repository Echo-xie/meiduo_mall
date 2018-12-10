let common = {
    // 后台api路径
    host: "http://api.lnsist.top:8000/",
    // ajax请求头封装
    config: {
        headers: {
            // 向后端传递JWT
            'Authorization': 'JWT ' + sessionStorage.token || localStorage.token
        },
        // 设置为true, 才会往服务器传递cookie数据
        withCredentials: true,
        responseType: 'json',
    },
}
