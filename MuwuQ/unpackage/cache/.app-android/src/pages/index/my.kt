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
import io.dcloud.uniapp.extapi.reLaunch as uni_reLaunch
open class GenPagesIndexMy : BasePage {
    constructor(__ins: ComponentInternalInstance) : super(__ins) {}
    @Suppress("UNUSED_PARAMETER", "UNUSED_VARIABLE")
    override fun `$render`(): Any? {
        val _ctx = this
        val _cache = this.`$`.renderCache
        return createElementVNode("view", utsMapOf("class" to "container"), utsArrayOf(
            createElementVNode("text", null, "用户名"),
            createElementVNode("text", null, "主键"),
            createElementVNode("scroll-view", utsMapOf("class" to "scontainer"), utsArrayOf(
                createElementVNode("text", null, "历史记录"),
                createElementVNode("text", null, "修改"),
                createElementVNode("text", null, "清除"),
                createElementVNode("text", null, "分类管理"),
                createElementVNode("button", utsMapOf("class" to "exit", "onClick" to fun(){
                    _ctx.goPage("./login1")
                }
                ), "退出登录", 8, utsArrayOf(
                    "onClick"
                ))
            ))
        ))
    }
    override fun `$initMethods`() {
        this.goPage = fun(url: String) {
            uni_reLaunch(ReLaunchOptions(url = url))
        }
    }
    open lateinit var goPage: (url: String) -> Unit
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
                return utsMapOf("container" to padStyleMapOf(utsMapOf("display" to "flex", "justifyContent" to "center", "alignItems" to "center", "width" to "100%", "height" to "100%")), "scontainer" to padStyleMapOf(utsMapOf("display" to "flex", "flexDirection" to "column", "justifyContent" to "flex-start", "alignItems" to "center", "width" to "80%", "flexGrow" to 1, "overflowY" to "auto", "borderTopWidth" to 1, "borderRightWidth" to 1, "borderBottomWidth" to 1, "borderLeftWidth" to 1, "borderTopStyle" to "solid", "borderRightStyle" to "solid", "borderBottomStyle" to "solid", "borderLeftStyle" to "solid", "borderTopColor" to "#cccccc", "borderRightColor" to "#cccccc", "borderBottomColor" to "#cccccc", "borderLeftColor" to "#cccccc", "marginTop" to 10, "marginRight" to 0, "marginBottom" to 10, "marginLeft" to 0)), "exit" to padStyleMapOf(utsMapOf("marginTop" to "auto")))
            }
        var inheritAttrs = true
        var inject: Map<String, Map<String, Any?>> = utsMapOf()
        var emits: Map<String, Any?> = utsMapOf()
        var props = normalizePropsOptions(utsMapOf())
        var propsNeedCastKeys: UTSArray<String> = utsArrayOf()
        var components: Map<String, CreateVueComponent> = utsMapOf()
    }
}
