"use strict";
const common_vendor = require("../common/vendor.js");
const _sfc_main = {
  data() {
    return {
      sortOptions: ["最近使用", "最久未用", "从大到小", "从小到大"],
      currentSort: "最近使用",
      fileOptions: ["所有文件", "图片", "文件", "文件夹", "视频", "音频"],
      currentFile: "图片",
      isBatchMode: false
    };
  },
  methods: {
    handleSortChange(e) {
      this.currentSort = this.sortOptions[e.detail.value];
    },
    handleFileChange(e) {
      this.currentFile = this.fileOptions[e.detail.value];
    },
    toggleBatchMode() {
      this.isBatchMode = !this.isBatchMode;
      common_vendor.index.$emit("toggleBatchModes", this.isBatchMode);
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {
    a: common_vendor.t($data.currentSort),
    b: $data.sortOptions,
    c: common_vendor.o((...args) => $options.handleSortChange && $options.handleSortChange(...args)),
    d: common_vendor.t($data.currentFile),
    e: $data.fileOptions,
    f: common_vendor.o((...args) => $options.handleFileChange && $options.handleFileChange(...args)),
    g: common_vendor.t($data.isBatchMode ? "完成" : "批量操作"),
    h: $data.isBatchMode ? 1 : "",
    i: common_vendor.o((...args) => $options.toggleBatchMode && $options.toggleBatchMode(...args))
  };
}
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createComponent(Component);
//# sourceMappingURL=../../.sourcemap/mp-weixin/components/myNavigationBar.js.map
