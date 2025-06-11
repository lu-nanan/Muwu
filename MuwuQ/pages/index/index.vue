<template>
	<view class="content">
		<myNavagationBar></myNavagationBar>

		<uni-search-bar class="searchbar" @confirm="search" :focus="false" @blur="blur" @focus="focus"
			:placeholder="path"></uni-search-bar>

		<!-- <spaceUsageDisplay></spaceUsageDisplay> -->
		<cloudFileList :files="files" style="margin-bottom: 12rpx; "></cloudFileList>
		<view>
			<QRcodeModel :isShow="isModalShow" :qrcodeUrl="qrcodeUrl" :tipText="qrTip" @close="handleModalClose" />
		</view>
	</view>

</template>

<script>
	import myNavagationBar from '@/components/myNavigationBar.vue'
	import mySearchInput from '@/components/mySearchInput.vue'
	import cloudFileList from '@/components/cloudFileList.vue'
	import QRcodeModel from '@/components/QRcodeModel.vue';


	export default {
		data() {
			return {
				id: getApp().globalData.userInfo.id,
				path: getApp().globalData.userInfo.id,
				files: [],
				isModalShow: false,
				qrcodeUrl: '', // 后端返回的二维码 URL
				qrTip: '扫描二维码登录',
				urls:getApp().globalData.url,
			};
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
			uni.$on('jump', function(e) {
				if (e.name === '..') {
					if (this.path != this.id) {
						this.path = this.path.slice(0, this.path.lastIndexOf('/'));
					} else {
						uni.showToast({
							title: '根目录不能再往上了'
						})
					}
				} else {
					this.path = this.path + '/' + e.name;
				}
				if (e.type === '文件夹') {
					
						uni.showToast({
						  title: '加载中...',
						  icon: 'loading',
						  duration: 30000, // 防止长时间请求导致提示自动消失
						  mask: true // 显示遮罩层，防止用户操作
						});
					uni.request({
						url: this.urls +'/file/list',
						method: 'GET',
						header: {
							'Accept': 'application/json',
							// 注意：GET 请求通常不需要 Content-Type，可删除此行
							// 'Content-Type': 'application/json'
						},
						// 添加查询参数
						data: {
							path: this.path, // 当前浏览路径
							userId: this.id // 用户ID
						},
						success: (res) => {
							
								console.log(res)
							uni.hideToast();
							if (res.statusCode === 200) {
								this.files = this.formatFileData(res.data);

								const file = {
									name: '..',
									type: '文件夹'
								};
								this.files.push(file);
							} else {
								console.error('获取文件列表失败：', res.statusCode);
							}
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
				} else {
					uni.showActionSheet({
						itemList: ['删除', '分享','下载','AI操作'],
						success: (res) => {
							if (res.tapIndex === 0) {
								// 用户点击了删除按钮
								console.log('用户点击了删除按钮');
								uni.request({
									url: this.urls +'/file/delete?filePath='+this.path +'&userId='+this.id,
									method: 'DELETE',
									header: {
										//'Accept': 'application/json',
										// 注意：GET 请求通常不需要 Content-Type，可删除此行
										// 'Content-Type': 'application/json'
									},
									// 添加查询参数
									data: {
										filePath: this.path, // 当前浏览路径
										userId: this.id // 用户ID
									},
									success: (res) => {
										console.log(res)
										 uni.hideLoading();
										      
										      if (res.statusCode === 200) {
										        uni.showToast({
										          title: '删除成功',
										          icon: 'success'
										        });
										        // 刷新文件列表或执行其他操作
										        this.loadFileList();
										      } else {
										        uni.showToast({
										          title: `删除失败: ${res.data.message || '未知错误'}`,
										          icon: 'none'
										        });
										      }
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
								// 在此处添加删除文件的逻辑
							} else if (res.tapIndex === 1) {
								// 用户点击了分享按钮
								console.log('aaaa', e);
								// 在此处添加分享文件的逻辑
								this.showQRCodeModal();
							}
							else if (res.tapIndex === 2){
								console.log('test下载');
								uni.request({
									url:this.urls +'/source/preview',
									method: 'GET',
									header: {
										//'Accept': 'application/json',
										// 注意：GET 请求通常不需要 Content-Type，可删除此行
										// 'Content-Type': 'application/json'
									},
									// 添加查询参数
									data: {
										filePath: this.path, // 当前浏览路径
										userId: getApp().globalData.userInfo.id // 用户ID
									},
									success: (res) => {
										uni.hideToast();
										console.log(res)
										//plus.runtime.openWeb(res.data.url);
										plus.runtime.openURL(res.data.url, (error) => {
										    if (error) {
										      console.error('打开链接失败:', error.message);
										      uni.showToast({
										        title: '无法打开链接，请检查网络或手动复制到浏览器',
										        icon: 'none'
										      });
										    } else {
										      console.log('链接已成功打开');
										    }
										  });
									},
									fail: (err) => {
										console.log(err)
										if (err.errMsg.includes('request:fail')) {
											// 打印失败类型和状态码
											console.log('请求失败（网络错误）：', err.errMsg, '状态码：', err.statusCode);
										} else {
											// 打印其他失败信息
											console.log('请求失败，错误信息：', err.errMsg);
										}
									}
								});
							}
							else if (res.tapIndex === 3){
								console.log('testAI');
								console.log(e.fileType);
								
								let contents = '';
								let op = '';
								if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg'].includes(e.fileType)){
								uni.showActionSheet({
									itemList:['ocr','SR','subtitles'],
									success:(ress)=>{
										if(ress.tapIndex === 0){
											op='ocr'
											contents = `检测到文件类型 (${e.fileType})，将进行${op}操作`;
											this.AIModal(op,contents);
										}
										else if(ress.tapIndex === 1){
											op= 'SR'
											contents = `检测到文件类型 (${e.fileType})，将进行${op}操作`;
											this.AIModal(op,contents);
										}
										else if(ress.tapIndex === 2){
											op = 'subtitles'
											contents = `检测到文件类型 (${e.fileType})，将进行${op}操作`;
											this.AIModal(op,contents);
										}
										
										},
										fail: (err) => {
												console.error('显示操作菜单失败:', err);
											}
										});
										}
										/*else if (e.fileType === 'pdf'){
											op ='GetPdfText'
											contents = `检测到文件类型 (${e.fileType})，将进行${op}操作`;
											this.AIModal(op,contents);
										}*/
										else if (e.fileType === 'md'){
											op ='mind'
											contents = `检测到文件类型 (${e.fileType})，将进行${op}操作`;
											this.AIModal(op,contents);
										}else if (e.fileType === 'docx'){
											op ='Topdf'
											contents = `检测到文件类型 (${e.fileType})，将进行${op}操作`;
											this.AIModal(op,contents);
										} else{
											
											uni.showToast({
												title: '不支持该文件类型',
												icon: 'error'
											});
										}
										
							}
						},
						fail: (err) => {
							console.error('显示操作菜单失败:', err);
						}
					});
				}
			}.bind(this));
			
				uni.showToast({
				  title: '加载中...',
				  icon: 'loading',
				  duration: 30000, // 防止长时间请求导致提示自动消失
				  mask: true // 显示遮罩层，防止用户操作
				});
			uni.request({
				url: this.urls +'/file/list',
				method: 'GET',
				header: {
					'Accept': 'application/json',
					// 注意：GET 请求通常不需要 Content-Type，可删除此行
					// 'Content-Type': 'application/json'
				},
				// 添加查询参数
				data: {
					path: this.path, // 当前浏览路径
					userId: this.id // 用户ID
				},
				success: (res) => {
					console.log(res)
					uni.hideToast();
					if (res.statusCode === 200) {
						this.files = this.formatFileData(res.data);

						const file = {
							name: '..',
							type: '文件夹',
							
						};
						this.files.push(file);
					} else {
						console.error('获取文件列表失败：', res.statusCode);
					}
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
		methods: {
			AIModal(op,contents){
				uni.showModal({
				   title: '确认操作',
				   content: contents,
				   confirmText: '确认',
				   cancelText: '取消',
				   success: (res) => {
				     if (res.confirm) {
				       console.log('用户点击确认');
				       // 执行确认后的逻辑（如删除、提交等）
														uni.request({
															url:this.urls +'/extends/' +op +'?filePath=' +this.path +'&userId='+this.id,
															method: 'POST',
															header: {
																//'Accept': 'application/json',
																// 注意：GET 请求通常不需要 Content-Type，可删除此行
																// 'Content-Type': 'application/json'
															},
															// 添加查询参数
															data: {
																filePath: this.path, // 当前浏览路径
																userId: this.id // 用户ID
															},
															success: (res) => {
																uni.hideToast();
																console.log(res)
																//plus.runtime.openWeb(res.data.url);
																uni.showModal({
																	showCancel:false,
																	content:res.data.result,
																})
															},
															fail: (err) => {
																console.log(err)
																if (err.errMsg.includes('request:fail')) {
																	// 打印失败类型和状态码
																	console.log('请求失败（网络错误）：', err.errMsg, '状态码：', err.statusCode);
																} else {
																	// 打印其他失败信息
																	console.log('请求失败，错误信息：', err.errMsg);
																}
															}
														});
				       
				     } else if (res.cancel) {
				       console.log('用户点击取消');
				       // 执行取消后的逻辑（如提示或无操作）
				     }
				   }
				 });
			},
			async showQRCodeModal() {
				
					uni.showToast({
					  title: '加载中...',
					  icon: 'loading',
					  duration: 30000, // 防止长时间请求导致提示自动消失
					  mask: true // 显示遮罩层，防止用户操作
					});
				uni.request({
					url: this.urls +'/file/share',
					method: 'GET', // 显式声明GET请求，匹配后端接口
					header: {
						'Accept': 'application/json' // 声明期望JSON响应
					},
					data: {
						path: this.path, // 实际文件路径（需替换为真实变量）
						userId: getApp().globalData.userInfo.id // 用户ID（从全局数据获取）
					},
					success: (res) => {
						uni.hideToast();
						console.log(res)
						if (res.statusCode === 200) {


							this.qrTip = res.data.url;
							this.qrcodeUrl = `data:image/png;base64,${res.data.qrcode}`;
							this.isModalShow = true;
						} else {
							uni.showToast({
								title: '获取二维码失败',
								icon: 'none'
							});
						}
					},
					fail: (err) => {

						console.error('请求失败:', error);
						uni.showToast({
							title: '网络错误',
							icon: 'none'
						});
					}
				});
			},
			 
			
			handleModalClose() {
				this.isModalShow = false;
			},
			search(res) {
					uni.showToast({
					  title: '加载中...',
					  icon: 'loading',
					  duration: 30000, // 防止长时间请求导致提示自动消失
					  mask: true // 显示遮罩层，防止用户操作
					});
				uni.request({
					url: this.urls +'/file/search',
					method: 'GET',
					header: {
						'Accept': 'application/json',
						// 注意：GET 请求通常不需要 Content-Type，可删除此行
						// 'Content-Type': 'application/json'
					},
					// 添加查询参数
					data: {
						keyword: res.value, // 当前浏览路径
						userId: getApp().globalData.userInfo.id // 用户ID
					},
					success: (res) => {
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
			blur(res) {
				uni.showToast({
					title: 'blur事件，输入值为：' + res.value,
					icon: 'none'
				})
			},
			focus(e) {
				uni.showToast({
					title: 'focus事件，输出值为：' + e.value,
					icon: 'none'
				})
			},
			change(e) {
				console.log('e:', e);
			},
			formatFileData(backendData) {
				return backendData.map(item => ({
					name: item.name,
					
					date: item.uploadTime ?
						new Date(item.uploadTime).toISOString()
						.replace('T', ' ')
						.replace(/\:\d+\.\d+Z/, '') :
						new Date().toISOString()
						.replace('T', ' ')
						.replace(/\:\d+\.\d+Z/, ''),
					size: item.type === 'directory' ?
						'-' :
						(item.size ? `${(item.size / 1024).toFixed(2)}KB` : '0B'),
					type: item.type === 'directory' ? '文件夹' : '文件',
					selected: false,
					trueSize:item.size,
					fileType:item.file_type,
					tag: item.tag || ''
				}));
			}
		},
		components: {
			myNavagationBar,
			mySearchInput,
			QRcodeModel,
			cloudFileList,
		}
	}
</script>


<style>
	.content {
		display: flex;
		flex-direction: column;
		background-color: #8D8DC1;
		width: 100%;
		min-height: 100vh;
	}
</style>