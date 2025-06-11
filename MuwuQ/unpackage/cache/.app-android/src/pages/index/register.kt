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
import io.dcloud.uniapp.extapi.navigateTo as uni_navigateTo
open class GenPagesIndexRegister : BasePage {
    constructor(__ins: ComponentInternalInstance) : super(__ins) {}
    @Suppress("UNUSED_PARAMETER", "UNUSED_VARIABLE")
    override fun `$render`(): Any? {
        val _ctx = this
        val _cache = this.`$`.renderCache
        return createElementVNode("scroll-view", utsMapOf("style" to normalizeStyle(utsMapOf("flex" to "1"))), utsArrayOf(
            createElementVNode("view", utsMapOf("class" to "login-container"), utsArrayOf(
                createElementVNode("view", utsMapOf("class" to "login"), utsArrayOf(
                    createElementVNode("view", utsMapOf("class" to "box"), utsArrayOf(
                        createElementVNode("view", utsMapOf("style" to normalizeStyle(utsMapOf("color" to "rgba(255,255,255,1)", "font-size" to "36px", "font-family" to "AlibabaPuHui", "line-height" to "50px"))), "注册", 4)
                    )),
                    createElementVNode("input", utsMapOf("class" to "uni-input", "placeholder" to "手机")),
                    createElementVNode("input", utsMapOf("class" to "uni-input", "placeholder" to "邮箱")),
                    createElementVNode("input", utsMapOf("class" to "uni-input", "placeholder" to "密码")),
                    createElementVNode("view", utsMapOf("class" to "box"), utsArrayOf(
                        createElementVNode("text", utsMapOf("style" to normalizeStyle(utsMapOf("color" to "white"))), "验证方式", 4),
                        createElementVNode("button", utsMapOf("style" to normalizeStyle(utsMapOf("width" to "30%", "border-radius" to "30rpx", "background" to "#A4ADB3", "color" to "rgba(255,255,255,1)"))), "手机", 4),
                        createElementVNode("button", utsMapOf("style" to normalizeStyle(utsMapOf("width" to "30%", "border-radius" to "30rpx", "background" to "#A4ADB3", "color" to "rgba(255,255,255,1)"))), "邮箱", 4)
                    )),
                    createElementVNode("input", utsMapOf("class" to "uni-input", "placeholder" to "验证码")),
                    createElementVNode("button", utsMapOf("style" to normalizeStyle(utsMapOf("width" to "80%", "border-radius" to "30rpx", "background" to "#A4ADB3", "color" to "rgba(255,255,255,1)"))), "注册", 4),
                    createElementVNode("text", utsMapOf("style" to normalizeStyle(utsMapOf("text-decoration" to "underline", "color" to "rgba(255,255,255,1)", "margin-top" to "auto")), "onClick" to fun(){
                        _ctx.goPage("./login1")
                    }
                    ), "已有账号?", 12, utsArrayOf(
                        "onClick"
                    ))
                ))
            ))
        ), 4)
    }
    override fun `$initMethods`() {
        this.goPage = fun(url: String) {
            uni_navigateTo(NavigateToOptions(url = url))
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
                return utsMapOf("login-container" to padStyleMapOf(utsMapOf("display" to "flex", "justifyContent" to "center", "backgroundColor" to "#000000", "alignItems" to "center", "WebkitTapHighlightColor" to "rgba(0, 0, 0, 0)", "lineHeight" to "18rpx", "fontSize" to "12rpx", "fontWeight" to "400", "fontStyle" to "normal", "color" to "rgba(0,0,0,0)", "marginTop" to 0, "marginRight" to 0, "marginBottom" to 0, "marginLeft" to 0, "paddingTop" to 0, "paddingRight" to 0, "paddingBottom" to 0, "paddingLeft" to 0, "userSelect" to "none", "boxSizing" to "border-box", "borderTopColor" to "rgb(187,187,187)", "borderRightColor" to "rgb(187,187,187)", "borderBottomColor" to "rgb(187,187,187)", "borderLeftColor" to "rgb(187,187,187)", "borderTopWidth" to 1, "borderRightWidth" to 1, "borderBottomWidth" to 1, "borderLeftWidth" to 1, "borderTopStyle" to "solid", "borderRightStyle" to "solid", "borderBottomStyle" to "solid", "borderLeftStyle" to "solid", "width" to "100%", "height" to "100%", "textDecoration" to "none")), "login" to padStyleMapOf(utsMapOf("display" to "flex", "flexDirection" to "column", "alignItems" to "center", "borderTopColor" to "rgb(187,187,187)", "borderRightColor" to "rgb(187,187,187)", "borderBottomColor" to "rgb(187,187,187)", "borderLeftColor" to "rgb(187,187,187)", "borderTopWidth" to 1, "borderRightWidth" to 1, "borderBottomWidth" to 1, "borderLeftWidth" to 1, "borderTopStyle" to "solid", "borderRightStyle" to "solid", "borderBottomStyle" to "solid", "borderLeftStyle" to "solid", "overflow" to "hidden", "width" to "60%", "height" to "80%", "borderTopLeftRadius" to 14, "borderTopRightRadius" to 14, "borderBottomRightRadius" to 14, "borderBottomLeftRadius" to 14, "textDecoration" to "none", "lineHeight" to "18px", "fontSize" to 12, "cursor" to "url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzNSIgaGVpZ2h0PSIzNSIgZmlsbD0ibm9uZSI+PGcgZmlsdGVyPSJ1cmwoI2ZpbHRlcjBfZF8xMTU1XzM4MTc1KSI+PHBhdGggZmlsbD0iIzAwMCIgc3Ryb2tlPSIjZmZmIiBkPSJtMTYuMTU4IDE1LjUyNi0uOTQ5LS4zMTYuMzE3Ljk0OCA0LjM4NyAxMy4xNjMuNDE2IDEuMjQ4LjUxOC0xLjIxIDIuNTg2LTYuMDQ0IDUuOTIyLTIuNDY2IDEuMjMzLS41MTQtMS4yNjctLjQyMi0xMy4xNjMtNC4zODdaIi8+PC9nPjxkZWZzPjxmaWx0ZXIgaWQ9ImZpbHRlcjBfZF8xMTU1XzM4MTc1IiB3aWR0aD0iMzgiIGhlaWdodD0iMzgiIHg9Ii0yIiB5PSItMSIgY29sb3ItaW50ZXJwb2xhdGlvbi1maWx0ZXJzPSJzUkdCIiBmaWx0ZXJVbml0cz0idXNlclNwYWNlT25Vc2UiPjxmZUZsb29kIGZsb29kLW9wYWNpdHk9IjAiIHJlc3VsdD0iQmFja2dyb3VuZEltYWdlRml4Ii8+PGZlQ29sb3JNYXRyaXggaW49IlNvdXJjZUFscGhhIiByZXN1bHQ9ImhhcmRBbHBoYSIgdmFsdWVzPSIwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAxMjcgMCIvPjxmZU9mZnNldCBkeT0iMSIvPjxmZUdhdXNzaWFuQmx1ciBzdGREZXZpYXRpb249IjEiLz48ZmVDb2xvck1hdHJpeCB2YWx1ZXM9IjAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAuNCAwIi8+PGZlQmxlbmQgaW4yPSJCYWNrZ3JvdW5kSW1hZ2VGaXgiIHJlc3VsdD0iZWZmZWN0MV9kcm9wU2hhZG93XzExNTVfMzgxNzUiLz48ZmVCbGVuZCBpbj0iU291cmNlR3JhcGhpYyIgaW4yPSJlZmZlY3QxX2Ryb3BTaGFkb3dfMTE1NV8zODE3NSIgcmVzdWx0PSJzaGFwZSIvPjwvZmlsdGVyPjwvZGVmcz48L3N2Zz4=\") 16 16, default", "fontFamily" to "BlinkMacSystemFont, Helvetica Neue, Arial, Microsoft Yahei, WenQuanYi Micro Hei, Pingfang SC, sans-serif", "marginTop" to 0, "marginRight" to 0, "marginBottom" to 0, "marginLeft" to 0, "paddingTop" to 0, "paddingRight" to 0, "paddingBottom" to 0, "paddingLeft" to 0, "userSelect" to "none", "boxSizing" to "border-box", "boxShadow" to "rgb(85, 98, 105) 0px 2px 6px 7px", "fontWeight" to "400", "fontStyle" to "normal", "color" to "rgba(0,0,0,0)", "backgroundImage" to "none", "backgroundColor" to "rgba(255,255,255,0.22)")), "box" to padStyleMapOf(utsMapOf("display" to "flex", "flexDirection" to "row", "justifyContent" to "space-between", "width" to "100%", "marginTop" to "20rpx", "marginRight" to "20rpx", "marginBottom" to "20rpx", "marginLeft" to "20rpx", "alignItems" to "center", "color" to "#3b2300", "fontSize" to "12rpx")), "uni-input" to padStyleMapOf(utsMapOf("paddingTop" to "12rpx", "paddingRight" to "12rpx", "paddingBottom" to "12rpx", "paddingLeft" to "12rpx", "borderTopLeftRadius" to "30rpx", "borderTopRightRadius" to "30rpx", "borderBottomRightRadius" to "30rpx", "borderBottomLeftRadius" to "30rpx", "marginTop" to "12rpx", "marginRight" to "12rpx", "marginBottom" to "12rpx", "marginLeft" to "12rpx", "width" to "95%", "backgroundColor" to "#ffffff")), "underline-text" to padStyleMapOf(utsMapOf("textDecoration" to "underline", "fontSize" to "12rpx", "color" to "rgba(255,255,255,1)")))
            }
        var inheritAttrs = true
        var inject: Map<String, Map<String, Any?>> = utsMapOf()
        var emits: Map<String, Any?> = utsMapOf()
        var props = normalizePropsOptions(utsMapOf())
        var propsNeedCastKeys: UTSArray<String> = utsArrayOf()
        var components: Map<String, CreateVueComponent> = utsMapOf()
    }
}
