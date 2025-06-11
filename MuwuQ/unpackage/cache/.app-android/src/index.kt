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
import io.dcloud.uniapp.extapi.connectSocket as uni_connectSocket
import io.dcloud.uniapp.extapi.exit as uni_exit
import io.dcloud.uniapp.extapi.showToast as uni_showToast
val runBlock1 = run {
    __uniConfig.getAppStyles = fun(): Map<String, Map<String, Map<String, Any>>> {
        return GenApp.styles
    }
}
fun initRuntimeSocket(hosts: String, port: String, id: String): UTSPromise<SocketTask?> {
    if (hosts == "" || port == "" || id == "") {
        return UTSPromise.resolve(null)
    }
    return hosts.split(",").reduce<UTSPromise<SocketTask?>>(fun(promise: UTSPromise<SocketTask?>, host: String): UTSPromise<SocketTask?> {
        return promise.then(fun(socket): UTSPromise<SocketTask?> {
            if (socket != null) {
                return UTSPromise.resolve(socket)
            }
            return tryConnectSocket(host, port, id)
        }
        )
    }
    , UTSPromise.resolve(null))
}
val SOCKET_TIMEOUT: Number = 500
fun tryConnectSocket(host: String, port: String, id: String): UTSPromise<SocketTask?> {
    return UTSPromise(fun(resolve, reject){
        val socket = uni_connectSocket(ConnectSocketOptions(url = "ws://" + host + ":" + port + "/" + id, fail = fun(_) {
            resolve(null)
        }
        ))
        val timer = setTimeout(fun(){
            socket.close(CloseSocketOptions(code = 1006, reason = "connect timeout"))
            resolve(null)
        }
        , SOCKET_TIMEOUT)
        socket.onOpen(fun(e){
            clearTimeout(timer)
            resolve(socket)
        }
        )
        socket.onClose(fun(e){
            clearTimeout(timer)
            resolve(null)
        }
        )
        socket.onError(fun(e){
            clearTimeout(timer)
            resolve(null)
        }
        )
    }
    )
}
fun initRuntimeSocketService(): UTSPromise<Boolean> {
    val hosts: String = "192.168.52.1,192.168.142.1,10.68.73.229,127.0.0.1"
    val port: String = "8090"
    val id: String = "app-android_1Hv53T"
    if (hosts == "" || port == "" || id == "") {
        return UTSPromise.resolve(false)
    }
    var socketTask: SocketTask? = null
    __registerWebViewUniConsole(fun(): String {
        return "!function(){\"use strict\";function e(e,t){try{return{type:e,args:n(t)}}catch(e){}return{type:e,args:[]}}function n(e){return e.map((function(e){return t(e)}))}function t(e,n){if(void 0===n&&(n=0),n>=7)return{type:\"object\",value:\"[Maximum depth reached]\"};switch(typeof e){case\"string\":return{type:\"string\",value:e};case\"number\":return function(e){return{type:\"number\",value:String(e)}}(e);case\"boolean\":return function(e){return{type:\"boolean\",value:String(e)}}(e);case\"object\":return function(e,n){if(null===e)return{type:\"null\"};if(function(e){return e.\$&&r(e.\$)}(e))return function(e,n){return{type:\"object\",className:\"ComponentPublicInstance\",value:{properties:Object.entries(e.\$.type).map((function(e){return o(e[0],e[1],n+1)}))}}}(e,n);if(r(e))return function(e,n){return{type:\"object\",className:\"ComponentInternalInstance\",value:{properties:Object.entries(e.type).map((function(e){return o(e[0],e[1],n+1)}))}}}(e,n);if(function(e){return e.style&&null!=e.tagName&&null!=e.nodeName}(e))return function(e,n){return{type:\"object\",value:{properties:Object.entries(e).filter((function(e){var n=e[0];return[\"id\",\"tagName\",\"nodeName\",\"dataset\",\"offsetTop\",\"offsetLeft\",\"style\"].includes(n)})).map((function(e){return o(e[0],e[1],n+1)}))}}}(e,n);if(function(e){return\"function\"==typeof e.getPropertyValue&&\"function\"==typeof e.setProperty&&e.\$styles}(e))return function(e,n){return{type:\"object\",value:{properties:Object.entries(e.\$styles).map((function(e){return o(e[0],e[1],n+1)}))}}}(e,n);if(Array.isArray(e))return{type:\"object\",subType:\"array\",value:{properties:e.map((function(e,r){return function(e,n,r){var o=t(e,r);return o.name=\"\".concat(n),o}(e,r,n+1)}))}};if(e instanceof Set)return{type:\"object\",subType:\"set\",className:\"Set\",description:\"Set(\".concat(e.size,\")\"),value:{entries:Array.from(e).map((function(e){return function(e,n){return{value:t(e,n)}}(e,n+1)}))}};if(e instanceof Map)return{type:\"object\",subType:\"map\",className:\"Map\",description:\"Map(\".concat(e.size,\")\"),value:{entries:Array.from(e.entries()).map((function(e){return function(e,n){return{key:t(e[0],n),value:t(e[1],n)}}(e,n+1)}))}};if(e instanceof Promise)return{type:\"object\",subType:\"promise\",value:{properties:[]}};if(e instanceof RegExp)return{type:\"object\",subType:\"regexp\",value:String(e),className:\"Regexp\"};if(e instanceof Date)return{type:\"object\",subType:\"date\",value:String(e),className:\"Date\"};if(e instanceof Error)return{type:\"object\",subType:\"error\",value:e.message||String(e),className:e.name||\"Error\"};var a=void 0,i=e.constructor;i&&i.get\$UTSMetadata\$&&(a=i.get\$UTSMetadata\$().name);return{type:\"object\",className:a,value:{properties:Object.entries(e).map((function(e){return o(e[0],e[1],n+1)}))}}}(e,n);case\"undefined\":return{type:\"undefined\"};case\"function\":return function(e){return{type:\"function\",value:\"function \".concat(e.name,\"() {}\")}}(e);case\"symbol\":return function(e){return{type:\"symbol\",value:e.description}}(e);case\"bigint\":return function(e){return{type:\"bigint\",value:String(e)}}(e)}}function r(e){return e.type&&null!=e.uid&&e.appContext}function o(e,n,r){var o=t(n,r);return o.name=e,o}\"function\"==typeof SuppressedError&&SuppressedError;var a=[\"log\",\"warn\",\"error\",\"info\",\"debug\"],i=null,u=[],c={};function s(e){null!=i?i(JSON.stringify(Object.assign({type:\"console\",data:e},c))):u.push.apply(u,e)}var f=a.reduce((function(e,n){return e[n]=console[n].bind(console),e}),{}),p=/^\\s*at\\s+[\\w/./-]+:\\d+\$/;function l(){function n(n){return function(){for(var t=[],r=0;r<arguments.length;r++)t[r]=arguments[r];var o=function(e,n,t){if(t||2===arguments.length)for(var r,o=0,a=n.length;o<a;o++)!r&&o in n||(r||(r=Array.prototype.slice.call(n,0,o)),r[o]=n[o]);return e.concat(r||Array.prototype.slice.call(n))}([],t,!0);if(o.length){var a=o[o.length-1];\"string\"==typeof a&&p.test(a)&&o.pop()}f[n].apply(f,o),s([e(n,t)])}}return function(){var e=console.log,n=Symbol();try{console.log=n}catch(e){return!1}var t=console.log===n;return console.log=e,t}()?(a.forEach((function(e){console[e]=n(e)})),function(){a.forEach((function(e){console[e]=f[e]}))}):function(){}}var y=null,g=new Set,d={};function v(e){if(null!=y){var n=e.map((function(e){var n=e&&\"promise\"in e&&\"reason\"in e,t=n?\"UnhandledPromiseRejection: \":\"\";if(n&&(e=e.reason),e instanceof Error&&e.stack)return e.message&&!e.stack.includes(e.message)?\"\".concat(t).concat(e.message,\"\\n\").concat(e.stack):\"\".concat(t).concat(e.stack);if(\"object\"==typeof e&&null!==e)try{return t+JSON.stringify(e)}catch(e){return t+String(e)}return t+String(e)})).filter(Boolean);n.length>0&&y(JSON.stringify(Object.assign({type:\"error\",data:n},d)))}else e.forEach((function(e){g.add(e)}))}function m(e){var n={type:\"WEB_INVOKE_APPSERVICE\",args:{data:{name:\"console\",arg:e}}};return window.__uniapp_x_postMessageToService?window.__uniapp_x_postMessageToService(n):window.__uniapp_x_.postMessageToService(JSON.stringify(n))}!function(){if(!window.__UNI_CONSOLE_WEBVIEW__){window.__UNI_CONSOLE_WEBVIEW__=!0;var e=\"[web-view]\".concat(window.__UNI_PAGE_ROUTE__?\"[\".concat(window.__UNI_PAGE_ROUTE__,\"]\"):\"\");l(),function(e,n){if(void 0===n&&(n={}),i=e,Object.assign(c,n),null!=e&&u.length>0){var t=u.slice();u.length=0,s(t)}}((function(e){m(e)}),{channel:e}),function(e,n){if(void 0===n&&(n={}),y=e,Object.assign(d,n),null!=e&&g.size>0){var t=Array.from(g);g.clear(),v(t)}}((function(e){m(e)}),{channel:e}),window.addEventListener(\"error\",(function(e){v([e.error])})),window.addEventListener(\"unhandledrejection\",(function(e){v([e])}))}}()}();"
    }
    , fun(data: String){
        socketTask?.send(SendSocketMessageOptions(data = data))
    }
    )
    return UTSPromise.resolve().then(fun(): UTSPromise<Boolean> {
        return initRuntimeSocket(hosts, port, id).then(fun(socket): Boolean {
            if (socket == null) {
                return false
            }
            socketTask = socket
            return true
        }
        )
    }
    ).`catch`(fun(): Boolean {
        return false
    }
    )
}
val runBlock2 = run {
    initRuntimeSocketService()
}
var firstBackTime: Number = 0
open class GenApp : BaseApp {
    constructor(__ins: ComponentInternalInstance) : super(__ins) {
        onLaunch(fun(_: OnLaunchOptions) {
            console.log("App Launch", " at App.uvue:5")
        }
        , __ins)
        onAppShow(fun(_: OnShowOptions) {
            console.log("App Show", " at App.uvue:8")
        }
        , __ins)
        onAppHide(fun() {
            console.log("App Hide", " at App.uvue:11")
        }
        , __ins)
        onLastPageBackPress(fun() {
            console.log("App LastPageBackPress", " at App.uvue:15")
            if (firstBackTime == 0) {
                uni_showToast(ShowToastOptions(title = "再按一次退出应用", position = "bottom"))
                firstBackTime = Date.now()
                setTimeout(fun(){
                    firstBackTime = 0
                }, 2000)
            } else if (Date.now() - firstBackTime < 2000) {
                firstBackTime = Date.now()
                uni_exit(null)
            }
        }
        , __ins)
        onExit(fun() {
            console.log("App Exit", " at App.uvue:32")
        }
        , __ins)
    }
    companion object {
        val styles: Map<String, Map<String, Map<String, Any>>> by lazy {
            normalizeCssStyles(utsArrayOf(
                styles0
            ))
        }
        val styles0: Map<String, Map<String, Map<String, Any>>>
            get() {
                return utsMapOf("uni-row" to padStyleMapOf(utsMapOf("flexDirection" to "row")), "uni-column" to padStyleMapOf(utsMapOf("flexDirection" to "column")))
            }
    }
}
val GenAppClass = CreateVueAppComponent(GenApp::class.java, fun(): VueComponentOptions {
    return VueComponentOptions(type = "app", name = "", inheritAttrs = true, inject = Map(), props = Map(), propsNeedCastKeys = utsArrayOf(), emits = Map(), components = Map(), styles = GenApp.styles)
}
, fun(instance): GenApp {
    return GenApp(instance)
}
)
val GenPagesIndexLogin1Class = CreateVueComponent(GenPagesIndexLogin1::class.java, fun(): VueComponentOptions {
    return VueComponentOptions(type = "page", name = "", inheritAttrs = GenPagesIndexLogin1.inheritAttrs, inject = GenPagesIndexLogin1.inject, props = GenPagesIndexLogin1.props, propsNeedCastKeys = GenPagesIndexLogin1.propsNeedCastKeys, emits = GenPagesIndexLogin1.emits, components = GenPagesIndexLogin1.components, styles = GenPagesIndexLogin1.styles)
}
, fun(instance): GenPagesIndexLogin1 {
    return GenPagesIndexLogin1(instance)
}
)
val GenPagesIndexIndexClass = CreateVueComponent(GenPagesIndexIndex::class.java, fun(): VueComponentOptions {
    return VueComponentOptions(type = "page", name = "", inheritAttrs = GenPagesIndexIndex.inheritAttrs, inject = GenPagesIndexIndex.inject, props = GenPagesIndexIndex.props, propsNeedCastKeys = GenPagesIndexIndex.propsNeedCastKeys, emits = GenPagesIndexIndex.emits, components = GenPagesIndexIndex.components, styles = GenPagesIndexIndex.styles)
}
, fun(instance): GenPagesIndexIndex {
    return GenPagesIndexIndex(instance)
}
)
val GenPagesIndexMyClass = CreateVueComponent(GenPagesIndexMy::class.java, fun(): VueComponentOptions {
    return VueComponentOptions(type = "page", name = "", inheritAttrs = GenPagesIndexMy.inheritAttrs, inject = GenPagesIndexMy.inject, props = GenPagesIndexMy.props, propsNeedCastKeys = GenPagesIndexMy.propsNeedCastKeys, emits = GenPagesIndexMy.emits, components = GenPagesIndexMy.components, styles = GenPagesIndexMy.styles)
}
, fun(instance): GenPagesIndexMy {
    return GenPagesIndexMy(instance)
}
)
val GenPagesIndexCloudpanClass = CreateVueComponent(GenPagesIndexCloudpan::class.java, fun(): VueComponentOptions {
    return VueComponentOptions(type = "page", name = "", inheritAttrs = GenPagesIndexCloudpan.inheritAttrs, inject = GenPagesIndexCloudpan.inject, props = GenPagesIndexCloudpan.props, propsNeedCastKeys = GenPagesIndexCloudpan.propsNeedCastKeys, emits = GenPagesIndexCloudpan.emits, components = GenPagesIndexCloudpan.components, styles = GenPagesIndexCloudpan.styles)
}
, fun(instance): GenPagesIndexCloudpan {
    return GenPagesIndexCloudpan(instance)
}
)
val GenPagesIndexLogin2Class = CreateVueComponent(GenPagesIndexLogin2::class.java, fun(): VueComponentOptions {
    return VueComponentOptions(type = "page", name = "", inheritAttrs = GenPagesIndexLogin2.inheritAttrs, inject = GenPagesIndexLogin2.inject, props = GenPagesIndexLogin2.props, propsNeedCastKeys = GenPagesIndexLogin2.propsNeedCastKeys, emits = GenPagesIndexLogin2.emits, components = GenPagesIndexLogin2.components, styles = GenPagesIndexLogin2.styles)
}
, fun(instance): GenPagesIndexLogin2 {
    return GenPagesIndexLogin2(instance)
}
)
val GenPagesIndexRegisterClass = CreateVueComponent(GenPagesIndexRegister::class.java, fun(): VueComponentOptions {
    return VueComponentOptions(type = "page", name = "", inheritAttrs = GenPagesIndexRegister.inheritAttrs, inject = GenPagesIndexRegister.inject, props = GenPagesIndexRegister.props, propsNeedCastKeys = GenPagesIndexRegister.propsNeedCastKeys, emits = GenPagesIndexRegister.emits, components = GenPagesIndexRegister.components, styles = GenPagesIndexRegister.styles)
}
, fun(instance): GenPagesIndexRegister {
    return GenPagesIndexRegister(instance)
}
)
val GenPagesApLoginApLoginClass = CreateVueComponent(GenPagesApLoginApLogin::class.java, fun(): VueComponentOptions {
    return VueComponentOptions(type = "page", name = "", inheritAttrs = GenPagesApLoginApLogin.inheritAttrs, inject = GenPagesApLoginApLogin.inject, props = GenPagesApLoginApLogin.props, propsNeedCastKeys = GenPagesApLoginApLogin.propsNeedCastKeys, emits = GenPagesApLoginApLogin.emits, components = GenPagesApLoginApLogin.components, styles = GenPagesApLoginApLogin.styles)
}
, fun(instance): GenPagesApLoginApLogin {
    return GenPagesApLoginApLogin(instance)
}
)
fun createApp(): UTSJSONObject {
    val app = createSSRApp(GenAppClass)
    return UTSJSONObject(Map<String, Any?>(utsArrayOf(
        utsArrayOf(
            "app",
            app
        )
    )))
}
fun main(app: IApp) {
    definePageRoutes()
    defineAppConfig()
    (createApp()["app"] as VueApp).mount(app, GenUniApp())
}
open class UniAppConfig : io.dcloud.uniapp.appframe.AppConfig {
    override var name: String = "xiangmu111"
    override var appid: String = "__UNI__54AC7C7"
    override var versionName: String = "1.0.0"
    override var versionCode: String = "100"
    override var uniCompilerVersion: String = "4.57"
    constructor() : super() {}
}
fun definePageRoutes() {
    __uniRoutes.push(UniPageRoute(path = "pages/index/login1", component = GenPagesIndexLogin1Class, meta = UniPageMeta(isQuit = true), style = utsMapOf("navigationBarTitleText" to "1", "backgroundColorContent" to "#324148")))
    __uniRoutes.push(UniPageRoute(path = "pages/index/index", component = GenPagesIndexIndexClass, meta = UniPageMeta(isQuit = false), style = utsMapOf("navigationBarTitleText" to "aaa", "backgroundColorContent" to "#fff3cd", "enablePullDownRefresh" to false)))
    __uniRoutes.push(UniPageRoute(path = "pages/index/my", component = GenPagesIndexMyClass, meta = UniPageMeta(isQuit = false), style = utsMapOf("navigationBarTitleText" to "uni-app 1", "backgroundColorContent" to "#fff3cd")))
    __uniRoutes.push(UniPageRoute(path = "pages/index/cloudpan", component = GenPagesIndexCloudpanClass, meta = UniPageMeta(isQuit = false), style = utsMapOf("navigationBarTitleText" to "uni-app 1", "backgroundColorContent" to "#fff3cd")))
    __uniRoutes.push(UniPageRoute(path = "pages/index/login2", component = GenPagesIndexLogin2Class, meta = UniPageMeta(isQuit = false), style = utsMapOf("navigationBarTitleText" to "", "backgroundColorContent" to "#324148")))
    __uniRoutes.push(UniPageRoute(path = "pages/index/register", component = GenPagesIndexRegisterClass, meta = UniPageMeta(isQuit = false), style = utsMapOf("navigationBarTitleText" to "", "backgroundColorContent" to "#324148")))
    __uniRoutes.push(UniPageRoute(path = "pages/ApLogin/ApLogin", component = GenPagesApLoginApLoginClass, meta = UniPageMeta(isQuit = false), style = utsMapOf("navigationBarTitleText" to "账号密码登录")))
}
val __uniTabBar: Map<String, Any?>? = utsMapOf("color" to "#333333", "selectedColor" to "#28a745", "backgroundColor" to "#fff8e1", "list" to utsArrayOf(
    utsMapOf("pagePath" to "pages/index/index", "text" to "首页"),
    utsMapOf("pagePath" to "pages/index/cloudpan", "text" to "云盘"),
    utsMapOf("pagePath" to "pages/index/my", "text" to "我的")
))
val __uniLaunchPage: Map<String, Any?> = utsMapOf("url" to "pages/index/login1", "style" to utsMapOf("navigationBarTitleText" to "1", "backgroundColorContent" to "#324148"))
fun defineAppConfig() {
    __uniConfig.entryPagePath = "/pages/index/login1"
    __uniConfig.globalStyle = utsMapOf("navigationBarTextStyle" to "black", "navigationBarTitleText" to "uni-app x", "navigationBarBackgroundColor" to "#fff8e1", "backgroundColor" to "#F8F8F8", "background" to "#fff3cd")
    __uniConfig.getTabBarConfig = fun(): Map<String, Any>? {
        return utsMapOf("color" to "#333333", "selectedColor" to "#28a745", "backgroundColor" to "#fff8e1", "list" to utsArrayOf(
            utsMapOf("pagePath" to "pages/index/index", "text" to "首页"),
            utsMapOf("pagePath" to "pages/index/cloudpan", "text" to "云盘"),
            utsMapOf("pagePath" to "pages/index/my", "text" to "我的")
        ))
    }
    __uniConfig.tabBar = __uniConfig.getTabBarConfig()
    __uniConfig.conditionUrl = ""
    __uniConfig.uniIdRouter = utsMapOf()
    __uniConfig.ready = true
}
open class GenUniApp : UniAppImpl() {
    open val vm: GenApp?
        get() {
            return getAppVm() as GenApp?
        }
    open val `$vm`: GenApp?
        get() {
            return getAppVm() as GenApp?
        }
}
fun getApp(): GenUniApp {
    return getUniApp() as GenUniApp
}
