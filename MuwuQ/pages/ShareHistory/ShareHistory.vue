<template>
	<!-- #ifdef APP -->
	<scroll-view style="flex:1">
	<!-- #endif -->
		<view style="background-color: #8D8DC1;">
			<historyListUvue :files="files"></historyListUvue>
		</view>
		<view>
			<QRcodeModel :isShow="isModalShow" :qrcodeUrl="qrcodeUrl" :tipText="qrTip" @close="handleModalClose" />
		</view>
	<!-- #ifdef APP -->
	</scroll-view>
	<!-- #endif -->
</template>

<script>
	import mySearchInput from '@/components/mySearchInput.vue'
	import historyListUvue from '../../components/historyList.vue';
	
	import QRcodeModel from '@/components/QRcodeModel.vue';
	export default {
		data() {
			return {
				files: [],
				id: getApp().globalData.userInfo.id,
				urls: getApp().globalData.url,
				isModalShow: false,
				qrcodeUrl: '', // 后端返回的二维码 URL
				qrTip: '扫描二维码登录',
			}
		},
		created() {
			uni.$on('shareTap', function(e) {
				console.log('test', JSON.stringify(e, null, 2));
				this.showQRCodeModal(e)
				}.bind(this));
			uni.request({
				url: this.urls + '/file/shares?userId='+this.id,
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
		methods: {
			formatFileData(backendData) {
				return backendData.map(item => ({
					name: item.fileName,
					date: item.createdAt ?
						new Date(item.createdAt).toISOString()
						.replace('T', ' ')
						.replace(/\:\d+\.\d+Z/, '') :
						new Date().toISOString()
						.replace('T', ' ')
						.replace(/\:\d+\.\d+Z/, ''),
					size: '',
					type: item.type === 'directory' ? '文件夹' : '文件',
					selected: false,
					tag: item.tag || '',
					qrCode: item.qrCode,
				}));
			},
			handleModalClose() {
				this.isModalShow = false;
			},
			showQRCodeModal(file) {
				
					uni.showToast({
					  title: '加载中...',
					  icon: 'loading',
					  duration: 30000, // 防止长时间请求导致提示自动消失
					  mask: true // 显示遮罩层，防止用户操作
					});
				uni.request({
					url: this.urls + '/qr/get?userId='+getApp().globalData.userInfo.id+'&qrPath='+file.qrCode,
					method: 'GET',
					header: {
						//'Accept': 'application/json',
						// 注意：GET 请求通常不需要 Content-Type，可删除此行
						// 'Content-Type': 'application/json'
					},
					// 添加查询参数
					data: {
						userId: getApp().globalData.userInfo.id,// 用户ID
						qrPath:file.qrCode,
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
		},
		components: {
			mySearchInput,
			historyListUvue,
			QRcodeModel,
		}
	}
</script>

<style>

</style>