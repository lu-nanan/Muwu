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
    goVcLogin() {
      common_vendor.index.navigateTo({
        url: "@/pages/Login/vcLogin"
      });
    },
    goRegister() {
      common_vendor.index.navigateTo({
        url: "@/pages/Register/register"
      });
    },
    handleChange() {
      this.remeberOrNot = !this.remeberOrNot;
      common_vendor.index.__f__("log", "at pages/Login/apLogin.vue:63", this.remeberOrNot);
    },
    show() {
      common_vendor.index.__f__("log", "at pages/Login/apLogin.vue:66", this.account, this.password);
    },
    async checkPassword() {
      if (!this.account.trim()) {
        common_vendor.index.showToast({
          title: "请输入账号",
          icon: "none"
        });
        return;
      }
      if (!this.password.trim()) {
        common_vendor.index.showToast({
          title: "请输入密码",
          icon: "none"
        });
        return;
      }
      const url = "https://274c7adb.r21.cpolar.top/auth/login";
      const data = {
        account: this.account,
        password: this.password
      };
      try {
        const res = await common_vendor.index.request({
          url,
          method: "POST",
          data,
          header: {
            "Content-Type": "application/json"
          }
        });
        if (res.data === "登录成功") {
          common_vendor.index.showToast({
            title: "登录成功",
            icon: "success"
          });
          common_vendor.index.setStorageSync("isLoggedIn", true);
          common_vendor.index.reLaunch({
            url: "/pages/index/index"
          });
        } else {
          common_vendor.index.showToast({
            title: res.data,
            icon: "none"
          });
        }
      } catch (error) {
        common_vendor.index.showToast({
          title: "网络请求失败",
          icon: "none"
        });
        common_vendor.index.__f__("error", "at pages/Login/apLogin.vue:120", error);
      }
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
    b: common_vendor.o(($event) => $options.goVcLogin()),
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
    i: common_vendor.o(($event) => $options.handleChange()),
    j: common_vendor.o(($event) => $options.checkPassword()),
    k: common_vendor.o(($event) => $options.goRegister())
  };
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/Login/apLogin.js.map
