<template>
	<view class="content">
		<image class="background-image" src="/static/register2.png" mode="scaleToFill"></image>
		<view class="login-container">
			<view class="login-title">注册</view>

			<view class="input-group">
				<uni-icons type="phone" size="60rpx" color="#6966AD"></uni-icons>
				<input v-model="phone" class="login-input" placeholder="请输入你的手机号" />
			</view>

			<view class="input-group">
				<uni-icons type="email" size="60rpx" color="#6966AD"></uni-icons>
				<input v-model="email" class="login-input" placeholder="请输入你的邮箱" />
			</view>

			<view class="input-group">
				<uni-icons type="auth" size="60rpx" color="#6966AD"></uni-icons>
				<input v-model="verificationCode" class="Verification-input" placeholder="请输入验证码" />
				<button class="Verification-button" @click="getVerificationCode">获取</button>
			</view>

			<view class="input-group">
				<uni-icons type="locked" size="60rpx" color="#6966AD"></uni-icons>
				<input v-model="password" type="password" class="login-input" placeholder="请输入密码" />
			</view>

			<view class="input-group">
				<uni-icons type="locked-filled" size="60rpx" color="#6966AD"></uni-icons>
				<input v-model="confirmPassword" type="password" class="login-input" placeholder="再次输入以确认密码" />
			</view>

			<view class="to-login">
				<text class="rn-text">已有账号？</text>
				<text class="r-text"> 点此登录</text>
			</view>

			<button class="login-button" @click="handleRegister">注册</button>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				urls:getApp().globalData.url,
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
				uni.request({
				  url: this.urls + '/verification/sendRegisterVerificationCode',
				  method: 'POST', // 修改为 POST
				  header: {
				    'Content-Type': 'application/json' // 明确指定 JSON 格式
				  },
				  data: {
				    // 填写 SendVerificationCodeRequest 对应的字段
				    email: this.email, // 假设手机号在 this.phone
				    // 其他必要参数...
				  },
				  success: (res) => {
				    uni.hideToast();
				    console.log(res);
				    
				    if (res.statusCode === 200) {
				      uni.showToast({
				        title: '验证码发送成功',
				        icon: 'success'
				      });
				    } else {
				      uni.showToast({
				        title: res.data.message || '发送失败',
				        icon: 'none'
				      });
				    }
				  },
				  fail: (err) => {
				    console.error('请求失败:', err);
				    uni.showToast({
				      title: '网络请求失败',
				      icon: 'none'
				    });
				  }
				});
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
				uni.request({
				  url: this.urls + '/auth/register', // 修改路径为后端接口路径
				  method: 'POST',                    // 修改为 POST 方法
				  header: {
				    'Content-Type': 'application/json' // 指定 JSON 格式
				  },
				  data: {
				    // 根据后端 RegisterRequest 类填写字段
					username:'无名',
				    verificationCode: this.verificationCode,    // 用户名
				    passwordHash: this.password,    // 密码
				    email: this.email,          // 邮箱
				    telephone: this.phone,          // 手机号
				    // 其他必要字段...
				  },
				  success: (res) => {
				    uni.hideToast();
				    console.log('注册响应:', res);
				    
				    if (res.statusCode === 200) {
				      // 注册成功，处理响应数据
				      uni.showToast({
				        title: '注册成功',
				        icon: 'success'
				      });
				      
				      // 跳转到登录页或其他页面
				    } else {
				      // 注册失败，显示错误信息
					  console.log(res);
				      uni.showToast({
				        title: res.data.message || '注册失败',
				        icon: 'none'
				      });
				    }
				  },
				  fail: (err) => {
				    console.error('请求失败:', err);
				    uni.showToast({
				      title: '网络请求失败',
				      icon: 'none'
				    });
				  }
				});
				// 注册逻辑（模拟）
				/*uni.showToast({
					title: '注册成功',
					icon: 'success'
				});
				// 清空表单
				this.phone = '';
				this.email = '';
				this.verificationCode = '';
				this.password = '';
				this.confirmPassword = '';*/
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