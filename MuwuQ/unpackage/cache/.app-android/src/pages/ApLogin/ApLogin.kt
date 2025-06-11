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
open class GenPagesApLoginApLogin : BasePage {
    constructor(__ins: ComponentInternalInstance) : super(__ins) {}
    @Suppress("UNUSED_PARAMETER", "UNUSED_VARIABLE")
    override fun `$render`(): Any? {
        val _cache = this.`$`.renderCache
        val _component_uni_icons = resolveComponent("uni-icons")
        val _component_checkbox = resolveComponent("checkbox")
        return createElementVNode("view", utsMapOf("class" to "login-container"), utsArrayOf(
            createElementVNode("image", utsMapOf("class" to "background-image", "src" to "/static/login.png", "mode" to "heightFix")),
            createElementVNode("view", utsMapOf("class" to "login-title"), "登录"),
            createElementVNode("view", utsMapOf("class" to "input-group"), utsArrayOf(
                createVNode(_component_uni_icons, utsMapOf("type" to "person", "size" to "30", "color" to "#6966AD")),
                createElementVNode("input", utsMapOf("class" to "login-input", "placeholder" to "账号/手机号/邮箱"))
            )),
            createElementVNode("view", utsMapOf("class" to "input-group"), utsArrayOf(
                createVNode(_component_uni_icons, utsMapOf("type" to "locked", "size" to "30", "color" to "#6966AD")),
                createElementVNode("input", utsMapOf("class" to "login-input", "placeholder" to "登录密码"))
            )),
            createElementVNode("view", utsMapOf("class" to "remeberme"), utsArrayOf(
                createVNode(_component_checkbox, utsMapOf("value" to "checkbox1", "style" to normalizeStyle(utsMapOf("transform" to "scale(0.7)"))), null, 8, utsArrayOf(
                    "style"
                )),
                createElementVNode("text", utsMapOf("class" to "checkbox-text"), "记住我")
            )),
            createElementVNode("view", utsMapOf("class" to "to-register"), utsArrayOf(
                createElementVNode("text", utsMapOf("class" to "ztext"), "没有账号？"),
                createElementVNode("text", utsMapOf("class" to "ztext"), "点此注册")
            )),
            createElementVNode("view", null, utsArrayOf(
                createElementVNode("text", utsMapOf("class" to "bottom-title"), "木屋"),
                createElementVNode("text", utsMapOf("class" to "bottom-title"), "MuwuTools")
            ))
        ))
    }
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
                return utsMapOf("login-container" to padStyleMapOf(utsMapOf("position" to "fixed", "height" to "100%", "width" to "100%")), "background-image" to padStyleMapOf(utsMapOf("position" to "fixed", "width" to "100%", "height" to "100%", "top" to 0, "left" to 0, "zIndex" to -1)), "input-group" to padStyleMapOf(utsMapOf("marginLeft" to "5%", "marginTop" to "21rpx", "width" to "55%", "display" to "flex", "gridTemplateColumns" to "auto 1fr", "marginBottom" to "20rpx", "paddingBottom" to "3rpx", "borderBottomWidth" to "1rpx", "borderBottomStyle" to "solid", "borderBottomColor" to "#cccccc")), "login-input" to padStyleMapOf(utsMapOf("height" to "30rpx", "fontSize" to "16rpx", "paddingTop" to 0, "paddingRight" to "10rpx", "paddingBottom" to 0, "paddingLeft" to "10rpx", "textAlign" to "center", "fontSize::placeholder" to "14rpx", "color::placeholder" to "#c8c8c8")), "login-title" to padStyleMapOf(utsMapOf("color" to "#6966AD", "marginLeft" to "7%", "marginTop" to "22%", "marginBottom" to "10%", "fontSize" to "30rpx", "fontWeight" to "bold")), "remeberme" to padStyleMapOf(utsMapOf("marginLeft" to "5%", "marginTop" to "7%", "display" to "flex", "gridTemplateColumns" to "auto 1fr")), "checkbox-text" to padStyleMapOf(utsMapOf("fontSize" to "17rpx", "color" to "#343434")))
            }
        var inheritAttrs = true
        var inject: Map<String, Map<String, Any?>> = utsMapOf()
        var emits: Map<String, Any?> = utsMapOf()
        var props = normalizePropsOptions(utsMapOf())
        var propsNeedCastKeys: UTSArray<String> = utsArrayOf()
        var components: Map<String, CreateVueComponent> = utsMapOf()
    }
}
