<template>
	
	<view class="login-container" style="background-color: #8D8DC1;">
		<view class="login-box">
			<view class="login-textbox">
				<text class="login-title" >{{title}}</text>
			</view>
	
			<view class="form-section" >
				<!-- 名称输入框 -->
				<view class="input-group">
					<uni-icons type="map" size="60rpx" color="#6966AD" class="input-icon"></uni-icons>
					<input class="login-input" placeholder="请输入新标签名" v-model="newTagName" />
				</view>
	
				<!-- 类型输入框 -->
				<view class="login-button" style="position: relative;" >
					<uni-icons  color="#6966AD" class="input-icon" style="position: absolute; left: 20rpx;" >标签类型:</uni-icons>
					
					<picker mode="selector" :range="tagTypes" @change="handleFileChange" class="nav-item">
						{{ tagType }}
					</picker>
				</view>
	
				<button class="login-button" @click="addTag" >
					确认
				</button>
			</view>
	
		</view>
	</view>
</template>

<script>
	export default {
		 onLoad(options) {
		   if (options.oldTag) {
		     try {
		       // 解码并解析参数
		       const decodedParams = decodeURIComponent(options.oldTag);
		       const parsedData = JSON.parse(decodedParams);
		       
		       // 将解析后的数据保存到data中
		       this.oldTag = parsedData;
			   this.title ='修改标签(无法修改标签类型)'
		       console.log('已保存参数到data:', this.oldTag);
		     } catch (error) {
		       console.error('参数解析失败:', error);
		       // 解析失败时保持data为空
		       this.oldTag = null;
		     }
		   } else {
		     // 没有传递参数时，data保持为空
		     console.log('未传递oldTag参数，data保持为空');
		   }
		 },
		data() {
			return {
				title:'新建标签',
				oldTag:null,
				option:' ',
				newTagName:'',
				tagTypes:['文件','图片'],
				tagType:'文件',
				id:getApp().globalData.userInfo.id,
				urls:getApp().globalData.url,
			};
		},
		methods: {
			handleFileChange(e) {
				this.tagType = this.tagTypes[e.detail.value]
			},
			addTag(){
			if (this.oldTag=== null){
			uni.request({
				url: this.urls + '/tag/add?userId='+this.id+'&tag='+this.newTagName+'&type='+this.tagType,
				method: 'POST',
				header: {
				},
				// 添加查询参数
				data: {
					userId: this.id,// 用户ID
					tag:this.newTagName,
					type:this.tagType,
				},
				success: (res) => {
					console.log(res)
					console.log(this.tagType)
					console.log(this.newTagName)
					uni.hideToast();
					if (res.statusCode === 200) {
						uni.showToast({
							icon:'success'
						});
					uni.navigateBack();
					} else {
						console.error('失败1：', res.statusCode);
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
			}
			else {
				console.log('aaaaaaaaaaaaa',this.oldTag);
				uni.request({
					url: this.urls + '/tag/update?userId='+this.id+'&newtag='+this.newTagName+'&type='+this.oldTag.type+'&oldtag='+this.oldTag.tag,
					method: 'POST',
					header: {
					},
					// 添加查询参数
					data: {
						userId: this.id,// 用户ID
						oldtag:this.oldTag.tag,
						newtag:this.newTagName,
						type:this.oldTag.type,
					},
					success: (res) => {
						console.log(res)
						console.log(this.tagType)
						console.log(this.newTagName)
						uni.hideToast();
						if (res.statusCode === 200) {
							uni.showToast({
								icon:'success'
							});
						uni.navigateBack();
						} else {
							console.error('失败2：', res.statusCode);
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
			}
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

	.nav-item {
		flex: 1;
		text-align:center;
		padding: 0 15px;
		
	}
	
</style>