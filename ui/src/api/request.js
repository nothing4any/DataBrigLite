//首先引入axios
import axios from 'axios'
//然后通过create方法来创建一个请求服务
//然后create方法内有一些配置项，比如接口域名`baseURL`、接口请求超时时间`timeout`
//接口url`url`
//接口请求方式`method`等等，需要我们按需传入
// create an axios instance
const service = axios.create({
    baseURL: process.env.VUE_APP_BASE_API,
    timeout: 5000
})

// 添加请求拦截器
service.interceptors.request.use(
    config => {
        // 从localStorage获取token
        const token = localStorage.getItem('token')
        // 如果token存在，则添加到请求头中
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`  // Bearer 是token的标准格式
        }
        return config
    },
    error => {
        return Promise.reject(error)
    }
)

//下面会定义两个拦截器，分别是 `请求拦截器`，`响应拦截器`
//`请求拦截器`是前端请求后端接口前处理的一些逻辑，比如开启loading，配置header请求头等等
//`响应拦截器`就是后端响应我们前端，返回回来的数据，比如我们可以在这响应拦截器内拿到status Code
//拿到后端接口返回的code，关闭loading、根据code码处理一些详细的逻辑等等一系列操作
//request interceptor   请求拦截器
// service.interceptors.request.use(
//   config => {
//     // do something before request is sent。在发送请求之前做一些事情
//     // 请求之前的设置
//     // 添加请求头信息，可以根据需要自行选择，也可以不要
//     // 例如请求头加入"tken"键
//     config.headers['token'] = "xxxxxx"
//     return config
//   },
//   error => {
//     // do something with request error// 请求错误时
//     console.log(error) // for debug
//     return Promise.reject(error)
//   }
// )
// response interceptor  响应拦截器
// service.interceptors.response.use(
//   response => {
//     const res = response.data
//
//     // if the custom code is not 20000, it is judged as an error.// 在这里限定了返回的必须要有返回码——code键，且返回码不为200时视为请求结果错误的
//     if (res.code !== 200) {
//       // 这是错误信息提示
// // 如果返回值有键-message，则错误信息是自定义的返回信息值，否则只提示'Error'
//       alert(res.message || 'Error')
// // 你也可以加入其它一些返回码的判断，也可以根据某些返回码跳转到某些页面
//       return Promise.reject(new Error(res.message || 'Error'))
//     } else {
//       return res
//     }
//   },
//   error => {
//     alert(res.message || 'Error')
//     return Promise.reject(error)
//   }
// )
// 最后暴露我们声明的 service 服务
export default service