<template>
	<view class="login-container">
		<view class="login-box">
			<view class="login-textbox">
				<text class="login-title" v-show="show1">上传信息确认</text>
			</view>

			<view class="form-section" v-show="show1">
				<!-- 路径输入框 -->
				<view class="input-group">
					<uni-icons type="map" size="60rpx" color="#6966AD" class="input-icon"></uni-icons>
					<input class="login-input" placeholder="请输入路径" v-model="localPath" @input="changePath()" />
				</view>

				<!-- 标签输入框 -->
				<view class="input-group">
					<uni-icons type="info" size="60rpx" color="#6966AD" class="input-icon"></uni-icons>
					<input class="login-input" v-model="localTag" @input="changeTag()" />
				</view>

				<button class="login-button" @click="Accept()">
					确认
				</button>
			</view>

			<view class="ai-suggestion-section" v-show="show2">
				<text class="ai-title">AI建议</text>
				<text class="ai-description">{{ aiTip }}</text>
				<view class="ai-buttons-group">
					<button class="ai-button reject" @click="suggetResult(false)">
						拒绝
					</button>
					<button class="ai-button accept" @click="suggetResult(true)">
						接受
					</button>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		props: {
			// 父组件传递的参数
			path: { // 初始路径
				type: String,
				default: '1'
			},
			tag: { // 初始标签
				type: String,
				default: 'aaaaa'
			},
		},
		data() {
			return {
				localPath: this.path, // 用props中的path初始化本地数据
				localTag: this.tag,
				aiTip:'',
				show1:true,
				show2:false,
				urls:getApp().globalData.url,
			};
		},
		watch: {
		    path(newValue, oldValue) {
		      this.localPath=newValue;
		    },
			tag(newValue, oldValue) {
			  this.localTag=newValue;
			  }
			},
			
		methods: {
			
			changePath(e) {
				this.localPath=e;
			},
			changeTag(e) {
				this.localTag=e;
			},
			Accept(){
				uni.showToast({
				  title: '加载中...',
				  icon: 'loading',
				  duration: 30000, // 防止长时间请求导致提示自动消失
				  mask: true // 显示遮罩层，防止用户操作
				});
				uni.request({
									url: this.urls +'/file/check',
									method: 'POST', // 修改请求方法为POST
										header: {
											'Accept': 'application/json',
											'Content-Type': 'application/x-www-form-urlencoded' // POST请求传递表单参数时建议使用此格式
										},
										data: {
											userId: getApp().globalData.userInfo.id, // 示例用户ID，需替换为实际值
											tag: this.tag, // 示例标签，需替换为实际值
											path: this.localPath // 示例路径，需替换为实际值
										},
									success: (res) => {
										console.log(this.localPath);
										
											console.log(this.localTag);
										uni.hideToast();
										console.log('1',res)
										console.log('2',res.data)
										console.log('3',res.data.suggest)
										const suggest = res.data.suggest;
										uni.showToast({
											icon:'success'
										});
										console.log(suggest)
										if(suggest){
											this.aiTip=suggest;
											console.log('4',suggest);
											this.show1=false;
											this.show2=true;
										}
										else{
											
											uni.$emit('uploadend');
										}
									},
									fail: (err) => {
										if (err.errMsg.includes('request:fail')) {
											this.message = err.errMsg + ' ' + err.statusCode;
										} else {
											this.message = `连接失败，错误信息：${err.errMsg}`;
										}
									}
								})
								},
			suggetResult(sure){
				uni.showToast({
				  title: '加载中...',
				  icon: 'loading',
				  duration: 30000, // 防止长时间请求导致提示自动消失
				  mask: true // 显示遮罩层，防止用户操作
				});
				uni.request({
					url: this.urls +'/file/suggest',
					method: 'GET', // 修改请求方法为POST
						header: {
							'Accept': 'application/json',
						},
						data: {
							accept: sure,
							userId: getApp().globalData.userInfo.id, // 示例用户ID，需替换为实际值
							 // 示例标签，需替换为实际值
							filePath:this.localPath // 示例路径，需替换为实际值
						},
						success: (res) => {
							uni.hideToast();
							uni.showToast({
								icon:'success'
							});
							console.log(res);
							console.log(res.data)
							this.showResult(res);
							},
							fail: (err) => {
								if (err.errMsg.includes('request:fail')) {
									this.message = err.errMsg + ' ' + err.statusCode;
								} else {
									this.message = `连接失败，错误信息：${err.errMsg}`;
								}
							}
				});
			},
			showResult(res) {
				uni.showModal({
					title: '结果',
					content: '结果已保存至该图片相同目录', // 假设 res.data.text 是需要显示的内容
					confirmText: '复制',
					cancelText: '关闭',
					success: (modalRes) => { // 重命名参数避免冲突
					uni.$emit('uploadend');
					this.show2=false;
					this.show1=true;
						if (modalRes.confirm) {
							// 用户点击了"复制"按钮
							const textToCopy = res.data.result; // 从外层 res 中获取需要复制的文本
							console.log('复制的文本:', textToCopy);

							uni.setClipboardData({
								data: textToCopy,
								success: () => {
									uni.showToast({
										title: '复制成功',
										icon: 'success'
									});
								},
								fail: (err) => {
									console.error('复制失败:', err);
									uni.showToast({
										title: '复制失败',
										icon: 'none'
									});
								}
							});
						} else if (modalRes.cancel) {
							// 用户点击了"分享"按钮
							console.log('用户选择分享');
							// 这里添加分享逻辑
						}
					}
				});
			},
		}
	};
</script>

<style lang="scss">
	.login-container {
		display: flex;
		position: fixed;
		height: 100%;
		width: 100%;
		justify-content: center;
		align-items: center;
	}

	.background-image {
		position: fixed;
		width: 100%;
		height: 100%;
		top: 0;
		left: 0;
		z-index: -1;
	}

	// Removed .info-box as its structure changed

	.login-box {
		width: 80%;
		// margin-top: 0%; // Original property, can be kept or removed
		background-color: rgba(255, 255, 255, 0.85);
		border-radius: 24rpx;
		padding: 40rpx;
		display: flex;
		flex-direction: column;
		box-sizing: border-box;
	}

	.login-textbox {
		display: flex;
		flex-direction: row;
		justify-content: center; // Centering title as per image
		align-items: center;
		width: 100%;
		margin-bottom: 40rpx;
	}

	.form-section {
		// New container for inputs and confirm button
		width: 100%;
		display: flex;
		flex-direction: column;
	}

	// .input-groups { // This class from original code wrapped multiple input-group, not used in this way here.
	// 	width: 100%;
	// }

	.input-group {
		margin-bottom: 30rpx; // Spacing between input groups
		width: 100%;
		display: flex;
		flex-direction: row;
		padding-bottom: 10rpx;
		border-bottom: 1rpx solid #ccc;
		align-items: center;
		box-sizing: border-box;
	}

	// .Verification-button { // This class is from the original snippet, not used in this specific UI design
	// 	font-size: 32rpx;
	// 	width: auto;
	// 	height: 80rpx;
	// 	border: 1.5px solid #6966AD;
	// 	border-radius: 154px;
	// 	background-color: #ffffff;
	// 	color: #6966AD;
	// 	text-align: center;
	// 	transition: all 0.3s ease;
	// }

	.login-input {
		flex: 1;
		height: 60rpx;
		font-size: 32rpx;
		padding: 0 10rpx;
		margin-left: 20rpx;
	}

	.login-input::placeholder {
		color: #c8c8c8;
	}

	.login-title {
		color: #6966AD;
		font-size: 50rpx; // Adjusted for image appearance, original was 70rpx
		font-weight: bold;
		text-align: center; // Changed from 'left' to 'center'
	}

	// .y-text, .remeberme, .z-text, .w-text, .to-register, .rn-text, .r-text classes from original are not used in this UI.
	// Keeping them in case they are part of a larger style guide, but they don't apply here.

	.login-button {
		// For the "确认" button
		margin-top: 30rpx; // Adjusted spacing
		width: 100%; // Full width as per image
		height: 80rpx;
		border: 1.5px solid #6966AD;
		border-radius: 20rpx; // Rounded corners as per image
		background-color: #ffffff;
		font-size: 36rpx;
		font-weight: bold;
		color: #6966AD;
		display: flex;
		align-items: center;
		justify-content: center;
		box-sizing: border-box;
	}

	// --- Styles for AI Suggestion Section ---
	.ai-suggestion-section {
		margin-top: 50rpx; // Spacing from the form/confirm button
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 10rpx; // Space between text elements in AI section
		width: 100%;
	}

	.ai-title {
		font-size: 38rpx;
		font-weight: bold;
		color: #6966AD;
	}

	.ai-description,
	.ai-action-text {
		font-size: 28rpx;
		color: #555555; // Slightly darker text for readability
		text-align: center;
	}

	.ai-action-text {
		margin-bottom: 15rpx; // Space before the AI buttons
	}

	.ai-buttons-group {
		display: flex;
		flex-direction: row;
		justify-content: space-between; // Distribute buttons
		width: 100%;
		margin-top: 10rpx;
	}

	.ai-button {
		width: 48%; // Each button takes almost half width
		height: 70rpx;
		border: 1.5px solid #6966AD;
		border-radius: 15rpx; // Rounded corners
		background-color: #ffffff;
		font-size: 32rpx;
		font-weight: bold;
		color: #6966AD;
		display: flex;
		align-items: center;
		justify-content: center;
		box-sizing: border-box;
	}
</style>