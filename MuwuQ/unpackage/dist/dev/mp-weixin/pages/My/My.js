"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  data() {
    return {};
  },
  methods: {
    goHistory() {
      common_vendor.index.navigateTo({
        url: "/pages/ShareHistory/ShareHistory"
      });
    },
    goChangePass() {
      common_vendor.index.navigateTo({
        url: "/pages/ChangePass/ChangePass"
      });
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {
    a: common_vendor.o(($event) => $options.goHistory()),
    b: common_vendor.o(($event) => $options.goChangePass())
  };
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/My/My.js.map
