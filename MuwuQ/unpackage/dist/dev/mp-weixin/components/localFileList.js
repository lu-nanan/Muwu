"use strict";
const common_vendor = require("../common/vendor.js");
const localFileListItem = () => "./localFileListItem.js";
const _sfc_main = {
  data() {
    return {
      isBatchModes: false,
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
          selected: true
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
    localFileListItem
  },
  created() {
    common_vendor.index.$on("toggleBatchModes", (function(e) {
      common_vendor.index.__f__("log", "at components/localFileList.vue:101", "监听到事件，携带参数为：" + e);
      if (this.isBatchModes === true && e === false) {
        const selectedFiles = this.files.filter(function(file) {
          return file.selected;
        });
        for (let i = 0; i < selectedFiles.length; i++) {
          common_vendor.index.__f__("log", "at components/localFileList.vue:110", selectedFiles[i].name);
        }
        for (let i = 0; i < this.files.length; i++) {
          this.files[i].selected = false;
        }
      }
      this.isBatchModes = e;
    }).bind(this));
  },
  methods: {
    selected(name) {
      if (this.isBatchModes === true) {
        for (let i = 0; i < this.files.length; i++) {
          if (this.files[i].name === name) {
            this.files[i].selected = !this.files[i].selected;
            break;
          }
        }
      }
      for (let i = 0; i < this.files.length; i++) {
        if (this.files[i].name === name) {
          common_vendor.index.__f__("log", "at components/localFileList.vue:134", this.files[i].name, this.files[i].selected);
          break;
        }
      }
    }
  }
};
if (!Array) {
  const _component_localFileListItem = common_vendor.resolveComponent("localFileListItem");
  _component_localFileListItem();
}
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {
    a: common_vendor.f($data.files, (file, index, i0) => {
      return {
        a: "30a2749f-0-" + i0,
        b: common_vendor.p({
          file
        }),
        c: file.selected && $data.isBatchModes ? 1 : "",
        d: common_vendor.o(($event) => $options.selected(file.name), index),
        e: index
      };
    })
  };
}
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createComponent(Component);
//# sourceMappingURL=../../.sourcemap/mp-weixin/components/localFileList.js.map
