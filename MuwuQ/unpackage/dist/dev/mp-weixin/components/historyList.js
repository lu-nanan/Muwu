"use strict";
const common_vendor = require("../common/vendor.js");
const historyListItem = () => "./historyListItem.js";
const _sfc_main = {
  data() {
    return {
      // 示例文件数据
      files: [
        {
          name: "文件夹1",
          date: "2024-12-01",
          size: "1.22G",
          type: "文件夹",
          selected: false
        },
        {
          name: "文件夹2",
          date: "2024-12-01",
          size: "1.22G",
          type: "文件夹",
          selected: false
        },
        {
          name: "旅行照片",
          date: "2024-11-28",
          size: "5.6M",
          type: "图片",
          selected: false
        },
        {
          name: "工作报告",
          date: "2024-11-25",
          size: "2.3M",
          type: "文档",
          selected: false
        },
        {
          name: "会议视频",
          date: "2024-11-20",
          size: "156M",
          type: "视频",
          selected: false
        },
        {
          name: "语音备忘录",
          date: "2024-11-18",
          size: "3.2M",
          type: "音频",
          selected: false
        },
        {
          name: "项目计划书",
          date: "2024-11-15",
          size: "1.8M",
          type: "文档",
          selected: false
        },
        {
          name: "家庭视频",
          date: "2024-11-10",
          size: "230M",
          type: "视频",
          selected: false
        },
        {
          name: "工作文件夹",
          date: "2024-11-05",
          size: "1.22G",
          type: "文件夹",
          selected: false
        },
        {
          name: "系统备份",
          date: "2024-11-01",
          size: "4.5G",
          type: "文件夹",
          selected: false
        }
      ]
    };
  },
  components: {
    historyListItem
  }
};
if (!Array) {
  const _component_historyListItem = common_vendor.resolveComponent("historyListItem");
  _component_historyListItem();
}
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {
    a: common_vendor.f($data.files, (file, index, i0) => {
      return {
        a: "7ca2692c-0-" + i0,
        b: common_vendor.p({
          file
        }),
        c: index
      };
    })
  };
}
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createComponent(Component);
//# sourceMappingURL=../../.sourcemap/mp-weixin/components/historyList.js.map
