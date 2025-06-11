"use strict";
const common_vendor = require("../common/vendor.js");
const _sfc_main = {
  props: ["file"],
  data() {
    return {
      // name: "�ļ���1",
      // date: "2024-12-1",
      // size: "123G",
      // tag: "����"
    };
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {
    a: common_vendor.t($props.file.name),
    b: common_vendor.t($props.file.tag),
    c: common_vendor.t($props.file.date),
    d: common_vendor.t($props.file.size)
  };
}
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createComponent(Component);
//# sourceMappingURL=../../.sourcemap/mp-weixin/components/cloudFileListItem.js.map
