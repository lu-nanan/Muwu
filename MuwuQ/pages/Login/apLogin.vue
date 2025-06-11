<template>
	<view class="login-container">
		<image class="background-image" src="/static/login3.png" mode="heightFix"></image>

		<view class="login-box">
			<view class="login-textbox">
				<text class="login-title">登录</text>
				<text class="y-text" @click="goVcLogin()">验证码登录</text>
			</view>

			<view class="input-groups">
				<view class="input-group">
					<uni-icons type="person" size="60rpx" color="#6966AD"></uni-icons />
					<input class="login-input" v-model="account" placeholder="账号/手机号/邮箱">
				</view>

				<view class="input-group">
					<uni-icons type="locked" size="60rpx" color="#6966AD"></uni-icons>
					<input class="login-input" type="password" v-model="password" placeholder="登录密码" />
				</view>

				<view class="remeberme">
					<checkbox-group name="" @change="handleChange()">
						<checkbox value="checkbox1" :style="{ transform: 'scale(0.6)' }" />
					</checkbox-group>
					<text class="z-text">记住我</text>
					<text class="w-text">忘记密码</text>
				</view>

				<button class="login-button" @click="checkPassword()">登录</button>

				<view class="to-register">
					<text class="rn-text">没有账号？</text>
					<text class="r-text" @click="goRegister()"> 点此注册</text>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				remeberOrNot: false,
				account: '',
				password: '',
				urls:getApp().globalData.url,
			}
		},
		methods: {
			goVcLogin() {
				uni.navigateTo({
					url: '/pages/Login/vcLogin'
				})
			},
			goRegister() {
				uni.navigateTo({
					url: '/pages/Register/Register'
				})
			},
			handleChange() {
				this.remeberOrNot = !this.remeberOrNot
				uni.setStorageSync('rememberme',this.remeberOrNot);
				console.log(this.remeberOrNot)
			},
			show() {
				console.log(this.account, this.password)
			},
			onload(){
				
				this.rememberOrNot=uni.getStorageSync('rememberme');
				if(rememberOrNot){
				this.account = uni.getStorageSync('account');
				this.password = uni.getStorageSync('password');
				}
			},
			async checkPassword() {
				if (!this.account.trim()) {
					uni.showToast({
						title: '请输入账号',
						icon: 'none'
					});
					return;
				}
				if (!this.password.trim()) {
					uni.showToast({
						title: '请输入密码',
						icon: 'none'
					});
					return;
				}

				const url = this.urls +'/auth/login';
				const data = {
					account: this.account,
					password: this.password,
				};

				try {
					uni.showToast({
					  title: '加载中...',
					  icon: 'loading',
					  duration: 30000, // 防止长时间请求导致提示自动消失
					  mask: true // 显示遮罩层，防止用户操作
					});
					const res = await uni.request({
						url,
						method: 'POST',
						data,
						header: {
							'Content-Type': 'application/json',
						},
					});

					if (res.data.message === '登录成功') {
						uni.hideToast();
						uni.showToast({
							title: '登录成功',
							icon: 'success'
						});
						/*if(this.rememberOrNot){
						uni.setStorageSync('account',account);
						uni.setStorageSync('password',password);
						}
						else{
							uni.removeStorageSync('account');
							uni.removeStorageSync('password');
						}*/
						const app=getApp();
						app.globalData.userInfo={id: res.data.userId}
						uni.reLaunch({
							url: '/pages/index/index'
						});
					} else {
						uni.showToast({
							title:'账号或密码错误',
							icon: 'error'
						});
					}
				} catch (error) {
					uni.showToast({
						title: '网络请求失败',
						icon: 'none'
					});
					console.error(error);
				}
			},
		}
	}
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

	.login-box {
		width: 80%;
		background-color: rgba(255, 255, 255, 0.85);
		border-radius: 24rpx;
		padding: 40rpx;
		display: flex;
		flex-direction: column;
	}

	.login-textbox {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
		width: 100%;
		margin-bottom: 40rpx;
	}

	.input-groups {
		width: 100%;
	}

	.input-group {
		margin-bottom: 30rpx;
		width: 100%;
		display: flex;
		flex-direction: row;
		padding-bottom: 10rpx;
		border-bottom: 1rpx solid #ccc;
		align-items: center;
	}

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
		font-size: 70rpx;
		font-weight: bold;
		text-align: left;
	}

	.y-text {
		font-size: 28rpx;
		color: #6966AD;
		align-self: flex-start;
	}

	.remeberme {
		display: flex;
		flex-direction: row;
		align-items: center;
		margin-top: 20rpx;
		margin-bottom: 10rpx;
	}

	.z-text {
		font-size: 28rpx;
		color: #343434;
	}

	.w-text {
		margin-left: auto;
		font-size: 28rpx;
		color: #343434;
	}

	.to-register {
		display: flex;
		flex-direction: row;
		margin-top: 50rpx;
		justify-content: center;
	}

	.rn-text {
		font-size: 28rpx;
		color: #343434;
	}

	.r-text {
		font-size: 28rpx;
		color: #6966AD;
		border-bottom: 1rpx solid #6966AD;
		font-weight: bold;
	}

	.login-button {
		margin-top: 60rpx;
		width: 80%;
		height: 80rpx;
		border: 1.5px solid #6966AD;
		border-radius: 40rpx;
		background-color: #ffffff;
		font-size: 36rpx;
		font-weight: bold;
		color: #6966AD;
		display: flex;
		align-items: center;
		justify-content: center;
		align-self: center;
		margin-left: auto;
		margin-right: auto;
	}
</style>