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
open class GenPagesIndexIndex : BasePage {
    constructor(__ins: ComponentInternalInstance) : super(__ins) {
        onLoad(fun(_: OnLoadOptions) {}, __ins)
        onReady(fun() {}, __ins)
    }
    @Suppress("UNUSED_PARAMETER", "UNUSED_VARIABLE")
    override fun `$render`(): Any? {
        val _ctx = this
        val _cache = this.`$`.renderCache
        val _component_uni_data_select = resolveComponent("uni-data-select")
        return createElementVNode("view", null, utsArrayOf(
            createVNode(_component_uni_data_select, utsMapOf("modelValue" to _ctx.selectedIndex, "onUpdate:modelValue" to fun(`$event`: Number){
                _ctx.selectedIndex = `$event`
            }
            , "localdata" to _ctx.range, "onChange" to _ctx.change), null, 8, utsArrayOf(
                "modelValue",
                "onUpdate:modelValue",
                "localdata",
                "onChange"
            )),
            createElementVNode("text", null, "aaa")
        ))
    }
    open var range: UTSArray<UTSJSONObject> by `$data`
    open var selectedIndex: Number by `$data`
    @Suppress("USELESS_CAST")
    override fun data(): Map<String, Any?> {
        return utsMapOf("range" to utsArrayOf(
            object : UTSJSONObject() {
                var value: Number = 0
                var text = "篮球"
                var disable = true
            },
            object : UTSJSONObject() {
                var value: Number = 1
                var text = "足球"
            },
            object : UTSJSONObject() {
                var value: Number = 2
                var text = "游泳"
            }
        ), "selectedIndex" to 1)
    }
    override fun `$initMethods`() {
        this.change = fun(e: Event) {
            console.log("e:", e, " at pages/index/index.uvue:40")
        }
    }
    open lateinit var change: (e: Event) -> Unit
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
                return utsMapOf("picker-container" to padStyleMapOf(utsMapOf("display" to "flex", "flexDirection" to "row", "justifyContent" to "space-between", "marginTop" to "10rpx", "marginRight" to "10rpx", "marginBottom" to "10rpx", "marginLeft" to "10rpx", "width" to "100%")), "pickers" to padStyleMapOf(utsMapOf("paddingLeft" to 10, "paddingRight" to 10)), "uni-px-5" to padStyleMapOf(utsMapOf("paddingLeft" to 10, "paddingRight" to 10)), "uni-pb-5" to padStyleMapOf(utsMapOf("paddingBottom" to 10)))
            }
        var inheritAttrs = true
        var inject: Map<String, Map<String, Any?>> = utsMapOf()
        var emits: Map<String, Any?> = utsMapOf()
        var props = normalizePropsOptions(utsMapOf())
        var propsNeedCastKeys: UTSArray<String> = utsArrayOf()
        var components: Map<String, CreateVueComponent> = utsMapOf()
    }
}
