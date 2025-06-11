@file:Suppress("UNCHECKED_CAST", "USELESS_CAST", "INAPPLICABLE_JVM_NAME", "UNUSED_ANONYMOUS_PARAMETER", "NAME_SHADOWING")
package uni.UNI54AC7C7
import io.dcloud.uniapp.*
import io.dcloud.uniapp.extapi.*
import io.dcloud.uniapp.framework.*
import io.dcloud.uniapp.runtime.*
import io.dcloud.uniapp.vue.*
import io.dcloud.uniapp.vue.shared.*
import io.dcloud.unicloud.*
import io.dcloud.uts.*
import io.dcloud.uts.Map
import io.dcloud.uts.Set
import io.dcloud.uts.UTSAndroid
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Deferred
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import io.dcloud.uniapp.extapi.request as uni_request
open class GenPagesIndexCloudpan : BasePage {
    constructor(__ins: ComponentInternalInstance) : super(__ins) {}
    @Suppress("UNUSED_PARAMETER", "UNUSED_VARIABLE")
    override fun `$render`(): Any? {
        val _ctx = this
        val _cache = this.`$`.renderCache
        return createElementVNode("view", utsMapOf("class" to "container"), utsArrayOf(
            createElementVNode("button", utsMapOf("onClick" to _ctx.testConnection), "测试后端连接", 8, utsArrayOf(
                "onClick"
            ))
        ))
    }
    override fun `$initMethods`() {
        this.testConnection = fun() {
            val apiUrl = "https://muwutools.top/getAllUserInfo/getAllUserInfo"
            uni_request<Any>(RequestOptions(url = apiUrl, method = "GET", sslVerify = false, success = fun(res){
                if (res.statusCode === 200) {
                    console.log("后端返回的字符串:", res.data, " at pages/index/cloudpan.uvue:19")
                } else {
                    console.error("请求失败，状态码:", res.statusCode, " at pages/index/cloudpan.uvue:21")
                }
            }
            , fail = fun(err){
                console.error("请求出错:", err, " at pages/index/cloudpan.uvue:25")
            }
            ))
        }
    }
    open lateinit var testConnection: () -> Unit
    companion object {
        val styles: Map<String, Map<String, Map<String, Any>>> by lazy {
            normalizeCssStyles(utsArrayOf(
                styles0
            ), utsArrayOf(
                GenApp.styles
            ))
        }
        val styles0: Map<String, Map<String, Map<String, Any>>>
            get() {
                return utsMapOf("container" to padStyleMapOf(utsMapOf("display" to "flex", "justifyContent" to "center", "alignItems" to "center", "height" to "100rpx")))
            }
        var inheritAttrs = true
        var inject: Map<String, Map<String, Any?>> = utsMapOf()
        var emits: Map<String, Any?> = utsMapOf()
        var props = normalizePropsOptions(utsMapOf())
        var propsNeedCastKeys: UTSArray<String> = utsArrayOf()
        var components: Map<String, CreateVueComponent> = utsMapOf()
    }
}
