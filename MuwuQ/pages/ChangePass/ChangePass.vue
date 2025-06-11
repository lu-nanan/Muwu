<template>
	<view class="content">
		<image class="background-image" src="/static/register2.png" mode="scaleToFill"></image>
		<view class="login-container">
			<view class="login-title">修改密码</view>

			<view class="input-group">
				<uni-icons type="email" size="60rpx" color="#6966AD"></uni-icons>
				<input v-model="email" class="login-input" placeholder="请输入你注册的邮箱" />
			</view>

			<view class="input-group">
				<uni-icons type="auth" size="60rpx" color="#6966AD"></uni-icons>
				<input v-model="verificationCode" class="Verification-input" placeholder="请输入验证码" />
				<button class="Verification-button" @click="getVerificationCode">获取</button>
			</view>

			<view class="input-group">
				<uni-icons type="locked" size="60rpx" color="#6966AD"></uni-icons>
				<input v-model="password" type="password" class="login-input" placeholder="请输入新密码" />
			</view>

			<view class="input-group">
				<uni-icons type="locked-filled" size="60rpx" color="#6966AD"></uni-icons>
				<input v-model="confirmPassword" type="password" class="login-input" placeholder="再次输入以确认密码" />
			</view>


			<button class="login-button" @click="handleRegister">确认</button>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				phone: '',
				email: '',
				verificationCode: '',
				password: '',
				confirmPassword: '',
			};
		},
		methods: {
			// 获取验证码
			getVerificationCode() {
				if (!this.email) {
					uni.showToast({
						title: '请输入邮箱',
						icon: 'none'
					});
					return;
				}
				// 模拟发送验证码到邮箱
				uni.showToast({
					title: '验证码已发送至邮箱',
					icon: 'success'
				});
			},
			// 注册事件
			handleRegister() {
				const phoneRegex = /^1[3-9]\d{9}$/;
				const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
				const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{10,}$/;

				if (!phoneRegex.test(this.phone)) {
					uni.showToast({
						title: '请输入正确的手机号',
						icon: 'none'
					});
					return;
				}
				if (!emailRegex.test(this.email)) {
					uni.showToast({
						title: '请输入正确的邮箱',
						icon: 'none'
					});
					return;
				}
				if (!this.verificationCode) {
					uni.showToast({
						title: '请输入验证码',
						icon: 'none'
					});
					return;
				}
				if (this.password !== this.confirmPassword) {
					uni.showToast({
						title: '两次输入的密码不一致',
						icon: 'none'
					});
					return;
				}
				if (!passwordRegex.test(this.password)) {
					uni.showToast({
						title: '密码必须包含字母和数字，且长度大于10位',
						icon: 'none'
					});
					return;
				}
				// 注册逻辑（模拟）
				uni.showToast({
					title: '注册成功',
					icon: 'success'
				});
				// 清空表单
				this.phone = '';
				this.email = '';
				this.verificationCode = '';
				this.password = '';
				this.confirmPassword = '';
			},
		},
	}
</script>

<style lang="scss">
	.content {
		position: relative;
		height: 100vh;
		width: 100vw;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		/* 确保内容垂直居中 */
	}

	.background-image {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: -1;
		// object-fit: cover;
	}

	.login-container {
		margin-top: 0%;
		width: 85%;
		height: auto;
		background-color: rgba(255, 255, 255, 0.7);
		border: 2px solid #7e7bb9;
		border-radius: 10px;
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 20rpx;
	}

	.login-title {
		color: #6966AD;
		margin-bottom: 10%;
		font-size: 70rpx;
		font-weight: bold;
		width: 100%;
		text-align: center;
	}

	.input-group {
		width: 100%;
		display: flex;
		flex-direction: row;
		align-items: center;
		margin-bottom: 20rpx;
		padding-bottom: 3rpx;
		border-bottom: 1rpx solid #ccc;
	}

	.login-button {
		margin-top: 10%;
		width: 480rpx;
		height: 100rpx;
		border: 1.5px solid #6966AD;
		border-radius: 24px;
		background-color: #ffffff;
		font-size: 18px;
		font-weight: bold;
		color: #6966AD;
		text-align: center;
		transition: all 0.3s ease;
		align-self: center;
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

	.login-input,
	.Verification-input {
		flex: 1;
		font-size: 32rpx;
		padding: 0 10rpx;
		text-align: left;
	}

	.login-input::placeholder,
	.Verification-input::placeholder {
		color: #c8c8c8;
	}

	.to-login {
		display: flex;
		flex-direction: row;
		width: 100%;
		margin-top: 6%;
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
</style>