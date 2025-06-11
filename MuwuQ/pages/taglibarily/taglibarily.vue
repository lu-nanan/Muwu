<template>
	<view class="content">
		<tagList :files="files"></tagList>
	</view>

</template>

<script>
	import tagList from '@/components/tagList.vue'
	
	
	export default {
		onShow() {
		 setTimeout(() => {
		    this.reload();
		  }, 1000); // 延迟时间（毫秒）
		},
		data() {
			return {
				
					files: [],
					id: getApp().globalData.userInfo.id,
					urls: getApp().globalData.url,
			}
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
		created() {
			uni.$on('tagSelected', function(e) {
				
					uni.showActionSheet({
						itemList: ['删除', '修改',],
						success: (res) => {
							if (res.tapIndex === 0) {
								// 用户点击了删除按钮
								console.log('用户点击了删除按钮');
								// 在此处添加删除文件的逻辑
								uni.request({
									url: this.urls + '/tag/delete?userId='+this.id+'&tag='+e.tag+'&type='+e.type,
									method: 'POST',
									header: {
										//'Accept': 'application/json',
										// 注意：GET 请求通常不需要 Content-Type，可删除此行
										// 'Content-Type': 'application/json'
									},
									// 添加查询参数
									data: {
										userId: this.id,// 用户ID
										tag:e.tag,
										type:e.name,
									},
									success: (res) => {
										console.log(res)
										uni.hideToast();
										if (res.statusCode === 200) {
										uni.showToast({
											icon:'success'
										});
										this.reload();
										} else {
											console.error('失败3：', res.statusCode);
										}
										console.log(this.files)
									},
									fail: (err) => {
										if (err.errMsg.includes('request:fail')) {
											// 打印失败类型和状态码
											console.log('请求失败（网络错误）：', err.errMsg, '状态码：', err.statusCode);
										} else {
											// 打印其他失败信息
											console.log('请求失败，错误信息：', err.errMsg);
										}
									}
								});
							} else if (res.tapIndex === 1) {
								// 用户点击了分享按钮
								console.log('aaaa', e);
								// 在此处添加分享文件的逻辑
								this.goChangeTag(e);
							}
							},
									
							
						fail: (err) => {
							console.error('显示操作菜单失败:', err);
						}
					});
				
			}.bind(this));
			this.reload();
		},
		methods: {
			reload(){
				uni.request({
					url: this.urls + '/tag/get',
					method: 'GET',
					header: {
						//'Accept': 'application/json',
						// 注意：GET 请求通常不需要 Content-Type，可删除此行
						// 'Content-Type': 'application/json'
					},
					// 添加查询参数
					data: {
						userId: this.id // 用户ID
					},
					success: (res) => {
						console.log(res)
						uni.hideToast();
						if (res.statusCode === 200) {
							this.files = this.formatFileData(res.data);
						
						} else {
							console.error('获取文件列表失败：', res.statusCode);
						}
						console.log(this.files)
					},
					fail: (err) => {
						if (err.errMsg.includes('request:fail')) {
							// 打印失败类型和状态码
							console.log('请求失败（网络错误）：', err.errMsg, '状态码：', err.statusCode);
						} else {
							// 打印其他失败信息
							console.log('请求失败，错误信息：', err.errMsg);
						}
					}
				});
			},
			goChangeTag(e) {
			  // 1. 将对象序列化为JSON字符串
			  const params = JSON.stringify(e);
			  // 2. 对JSON字符串进行URL编码，避免特殊字符问题
			  const encodedParams = encodeURIComponent(params);
			  uni.navigateTo({
			    url: `/pages/taglibarily/tagUpload?oldTag=${encodedParams}`
			  });
			},
			formatFileData(backendData) {
  const fileTags = backendData.FileTag || [];
  const photoTags = backendData.PhotoTag || [];
  
  // 生成"文件"分类下的所有标签项
  const fileItems = fileTags.map(tag => ({
    name: '文件',
    date: '',
    size: '',
    type: '文件',
    selected: false,
    tag: tag
  }));
  
  // 生成"图片"分类下的所有标签项
  const photoItems = photoTags.map(tag => ({
    name: '图片',
    date: '',
    size: '',
    type: '图片',
    selected: false,
    tag: tag
  }));
  
  // 合并两个分类的结果
  return [...fileItems, ...photoItems];
},
		},
		components: {
			tagList,
		}
	}
</script>


<style lang="scss">
.content {
	display: flex;
	flex-direction: column;
  background-color: #8D8DC1;
  width: 100%;
  height: 100%;
}
</style>