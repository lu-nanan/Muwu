"use strict";
const common_vendor = require("../../common/vendor.js");
const common_assets = require("../../common/assets.js");
const _sfc_main = {
  data() {
    return {
      remeberOrNot: false,
      account: "",
      password: ""
    };
  },
  methods: {
    goApLogin() {
      common_vendor.index.navigateTo({
        url: "/pages/ApLogin/ApLogin"
      });
    },
    goRegister() {
      common_vendor.index.navigateTo({
        url: "/pages/Register/Register"
      });
    },
    handleChange() {
      this.remeberOrNot = !this.remeberOrNot;
    },
    show() {
      common_vendor.index.__f__("log", "at pages/Login/vcLogin.vue:67", this.account, this.password);
    }
  }
};
if (!Array) {
  const _easycom_uni_icons2 = common_vendor.resolveComponent("uni-icons");
  _easycom_uni_icons2();
}
const _easycom_uni_icons = () => "../../uni_modules/uni-icons/components/uni-icons/uni-icons.js";
if (!Math) {
  _easycom_uni_icons();
}
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {
    a: common_assets._imports_0,
    b: common_vendor.o(($event) => $options.goApLogin()),
    c: common_vendor.p({
      type: "person",
      size: "60rpx",
      color: "#6966AD"
    }),
    d: $data.account,
    e: common_vendor.o(($event) => $data.account = $event.detail.value),
    f: common_vendor.p({
      type: "locked",
      size: "60rpx",
      color: "#6966AD"
    }),
    g: $data.password,
    h: common_vendor.o(($event) => $data.password = $event.detail.value),
    i: common_vendor.o(($event) => $options.goRegister())
  };
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/Login/vcLogin.js.map
