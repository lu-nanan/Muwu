"use strict";
const common_vendor = require("../../common/vendor.js");
const myNavagationBar = () => "../../components/myNavigationBar.js";
const mySearchInput = () => "../../components/mySearchInput.js";
const spaceUsageDisplay = () => "../../components/spaceUsageDisplay.js";
const cloudFileList = () => "../../components/cloudFileList.js";
const _sfc_main = {
  data() {
    return {};
  },
  // computed: {
  // 	// 根据搜索文本和当前文件类型筛选文件
  // 	filteredFiles() {
  // 		return this.files.filter(file => {
  // 			// 搜索文本过滤
  // 			const matchSearch = this.searchText === '' ||
  // 				file.name.toLowerCase().includes(this.searchText.toLowerCase());
  // 			// 文件类型过滤
  // 			const matchType = this.currentFile === '文件类型' ||
  // 				this.currentFile === '所有文件' ||
  // 				file.type === this.currentFile;
  // 			return matchSearch && matchType;
  // 		});
  // 	}
  // },
  methods: {},
  components: {
    myNavagationBar,
    mySearchInput,
    spaceUsageDisplay,
    cloudFileList
  }
};
if (!Array) {
  const _component_myNavagationBar = common_vendor.resolveComponent("myNavagationBar");
  const _component_mySearchInput = common_vendor.resolveComponent("mySearchInput");
  const _component_spaceUsageDisplay = common_vendor.resolveComponent("spaceUsageDisplay");
  const _component_cloudFileList = common_vendor.resolveComponent("cloudFileList");
  (_component_myNavagationBar + _component_mySearchInput + _component_spaceUsageDisplay + _component_cloudFileList)();
}
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {};
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/index/index.js.map
