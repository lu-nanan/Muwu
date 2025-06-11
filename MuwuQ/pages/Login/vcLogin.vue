<template>
	<view class="login-container">
		<image class="background-image" src="/static/login3.png" mode="heightFix"></image>

		<view class="login-box">
			<view class="login-textbox">
				<text class="login-title">登录</text>
				<text class="y-text" @click="goApLogin()">账号密码登录</text>
			</view>

			<view class="input-groups">
				<view class="input-group">
					<uni-icons type="person" size="60rpx" color="#6966AD"></uni-icons>
					<input class="login-input" v-model="account" placeholder="手机号/邮箱" />
				</view>

				<view class="input-group">
					<uni-icons type="locked" size="60rpx" color="#6966AD"></uni-icons>
					<input class="login-input" v-model="password" placeholder="验证码" />
					<button class="Verification-button" @click="getVerification()">获取</button>
				</view>

				<button class="login-button" @click="checkVerification()">登录</button>

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
			}
		},
		methods: {
			goApLogin() {
				uni.navigateTo({
					url: '/pages/Login/apLogin'
				})
			},
			goRegister() {
				uni.navigateTo({
					url: '/pages/Register/Register'
				})
			},
			// 获取验证码
			async getVerification() {
				const account = this.account.trim();
				if (!account) {
					uni.showToast({
						title: '请输入邮箱',
						icon: 'none'
					});
					return;
				}

				// 简单邮箱格式验证
				const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
				if (!emailRegex.test(account)) {
					uni.showToast({
						title: '请输入有效的邮箱地址',
						icon: 'none'
					});
					return;
				}

				try {
					const res = await uni.request({
						url: 'https://1e2c207f.r21.cpolar.top/verification/send',
						method: 'POST',
						data: {
							email: account
						}, // 传递邮箱
						header: {
							'Content-Type': 'application/x-www-form-urlencoded', // 表单格式
						},
					});

					if (res.data === '验证码发送成功。') {
						uni.showToast({
							title: '验证码已发送',
							icon: 'success'
						});
					} else {
						uni.showToast({
							title: res.data,
							icon: 'none'
						}); // 显示后端错误信息
					}
				} catch (error) {
					uni.showToast({
						title: '发送失败，请重试',
						icon: 'none'
					});
					console.error('发送验证码错误:', error);
				}
			},

			// 验证验证码并登录
			async checkVerification() {
				const account = this.account.trim();
				const code = this.password.trim();
				if (!account || !code) {
					uni.showToast({
						title: '请输入邮箱和验证码',
						icon: 'none'
					});
					return;
				}

				try {
					const res = await uni.request({
						url: 'https://1e2c207f.r21.cpolar.top/verification/verify',
						method: 'POST',
						data: {
							email: account,
							code
						}, // 传递邮箱和验证码
						header: {
							'Content-Type': 'application/x-www-form-urlencoded',
						},
					});

					if (res.data === '验证码验证成功。') {
						uni.showToast({
							title: '登录成功',
							icon: 'success'
						});
						// 保存登录状态（示例）
						uni.setStorageSync('isLoggedIn', true);
						// 跳转到首页
						uni.reLaunch({
							url: '/pages/index/index'
						});
					} else {
						uni.showToast({
							title: res.data,
							icon: 'none'
						});
					}
				} catch (error) {
					uni.showToast({
						title: '验证失败，请重试',
						icon: 'none'
					});
					console.error('验证码验证错误:', error);
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
		margin-top: 0%;
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

	.Verification-button {
		font-size: 32rpx;
		width: auto;
		height: 80rpx;
		border: 1.5px solid #6966AD;
		border-radius: 154px;
		background-color: #ffffff;
		color: #6966AD;
		text-align: center;
		transition: all 0.3s ease;
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