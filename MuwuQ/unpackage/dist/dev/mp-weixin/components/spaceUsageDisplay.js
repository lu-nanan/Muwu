"use strict";
const common_vendor = require("../common/vendor.js");
const _sfc_main = {
  name: "spaceUsageDisplay",
  data() {
    return {
      usedStorage: "3.2GB",
      totalStorage: "8.0GB",
      usedPercents: 40,
      fileCount: 152
    };
  },
  computed: {
    usePercentages: function() {
      let usedPercent = 40;
      return usedPercent + "%";
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {
    a: `conic-gradient(#FFD700 ${$data.usedPercents}%, #EAEEF4 0%)`,
    b: common_vendor.t($data.usedStorage),
    c: common_vendor.t($data.totalStorage),
    d: common_vendor.t($data.fileCount),
    e: common_vendor.t($options.usePercentages)
  };
}
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createComponent(Component);
//# sourceMappingURL=../../.sourcemap/mp-weixin/components/spaceUsageDisplay.js.map
