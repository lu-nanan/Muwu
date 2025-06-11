"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  data() {
    return {
      remeberOrNot: false,
      account: "",
      password: ""
    };
  },
  methods: {
    goVcLogin() {
      common_vendor.index.navigateTo({
        url: "../VcLogin/VcLogin"
      });
    },
    goRegister() {
      common_vendor.index.navigateTo({
        url: "../Register/Register"
      });
    },
    goLogin() {
      common_vendor.index.switchTab({
        url: "../index/index"
      });
    },
    handleChange() {
      this.remeberOrNot = !this.remeberOrNot;
    },
    show() {
      common_vendor.index.__f__("log", "at pages/ChangePass/ChangePass.vue:34", this.account, this.password);
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {};
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/ChangePass/ChangePass.js.map
