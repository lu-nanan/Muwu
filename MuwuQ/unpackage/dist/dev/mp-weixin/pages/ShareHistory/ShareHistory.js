"use strict";
const common_vendor = require("../../common/vendor.js");
const mySearchInput = () => "../../components/mySearchInput.js";
const historyListUvue = () => "../../components/historyList.js";
const _sfc_main = {
  data() {
    return {};
  },
  methods: {},
  components: {
    mySearchInput,
    historyListUvue
  }
};
if (!Array) {
  const _component_mySearchInput = common_vendor.resolveComponent("mySearchInput");
  const _component_historyListUvue = common_vendor.resolveComponent("historyListUvue");
  (_component_mySearchInput + _component_historyListUvue)();
}
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {};
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/ShareHistory/ShareHistory.js.map
