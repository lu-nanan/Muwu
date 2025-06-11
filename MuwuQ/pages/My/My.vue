<template>
	<view class="page-container">
		<!-- Header Purple Block -->
		<view class="header-purple-block">
			<text class="header-title-main">About myself</text>
			<view class="user-info-centered">
				<text class="username">木 屋</text>
				<text class="user-id">用户id: {{id}}</text>
			</view>
		</view>

		<!-- Content Area for Card and Logout Button -->
		<view class="content-area">
			<!-- Main Content Card with List Items -->
			<view class="content-card">
				<view class="list-item" @tap="goHistory">
					<text class="item-text">分享记录</text>
					<uni-icons type="right" size="18" color="#BDBDBD"></uni-icons>
				</view>

				<view class="list-item" @tap="goChangePass">
					<text class="item-text">修改个人信息</text>
					<uni-icons type="right" size="18" color="#BDBDBD"></uni-icons>
				</view>

				<view class="list-item" @tap="goAboutUs">
					<text class="item-text">关于我们</text>
					<uni-icons type="right" size="18" color="#BDBDBD"></uni-icons>
				</view>

				<view class="list-item" @tap="goTagLibarily">
					<text class="item-text">分类管理</text>
					<uni-icons type="right" size="18" color="#BDBDBD"></uni-icons>
				</view>
				
				<button class="logout-button" @tap="logout">退出登录</button>
				<!-- 
				<view class="logout-button-wrapper">
					<button class="logout-button" @tap="logout">退出登录</button>
				</view> -->
			</view>
			
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			// You can bind username and id from dynamic data if needed
			// usernameText: '用户名',
			id: getApp().globalData.userInfo.id,
		};
	},
	methods: {
		goHistory() {
			uni.navigateTo({
				url: '/pages/ShareHistory/ShareHistory'
			});
		},
		goChangePass() {
			uni.navigateTo({
				url: '/pages/ChangePass/ChangePass'
			});
		},
		goAboutUs() {
			uni.navigateTo({
				url: '/pages/AboutUs/AboutUs'
			});
		},
		goTagLibarily() {
			uni.navigateTo({
				url: '/pages/taglibarily/taglibarily'
			});
		},
		logout() {
			// Implement your logout logic here
			console.log("Logout button tapped");
			uni.showModal({
				title: '提示',
				content: '确定要退出登录吗？',
				success: function (res) {
					if (res.confirm) {
						console.log('用户点击确定');
						// Add actual logout logic, e.g., clearing token, navigating to login page
						// uni.reLaunch({ url: '/pages/login/login' });
						uni.showToast({ title: '已退出登录', icon: 'none' });
						const app=getApp();
						app.globalData.userInfo={id: -1}
						uni.reLaunch({
							url:'/pages/Login/apLogin'
						})
					} else if (res.cancel) {
						console.log('用户点击取消');
					}
				}
			});
		}
	}
};
</script>

<style lang="scss">
.page-container {
	display: flex;
	flex-direction: column;
	height: 87vh;
	background-color: #8D8DC1; /* Light lavender/grey background similar to image */
	box-sizing: border-box;
}

.header-purple-block {
	background-color: #8D8DC1; /* Purple color from image */
	padding: 20rpx 30rpx;
	padding-top: calc(var(--status-bar-height) + 20rpx); // Adjust for status bar
	color: white;
	width: 100%;
	box-sizing: border-box;
}

.header-title-main {
	font-size: 34rpx;
	font-weight: bold;
	margin-bottom: 40rpx; 
	display: block;
    text-align: left;
	padding-left: 10rpx; // Slight indent for "About myself"
}

.user-info-centered {
    text-align: center;
    padding-bottom: 40rpx; // Space at the bottom of the purple block
}

.username {
	font-size: 48rpx;
	font-weight: bold;
	margin-bottom: 12rpx;
	display: block;
}

.user-id {
	font-size: 28rpx;
	color: #E0DDEF; /* Lighter shade of white/purple for ID */
	display: block;
}

.content-area {
    padding: 30rpx 30rpx 0 30rpx; /* Top padding for space, LR padding */
    position: relative; 
    flex-grow: 1; /* Takes remaining vertical space */
    display: flex;
    flex-direction: column;
	box-sizing: border-box;
}

.content-card {
	background-color: white;
	border-radius: 20rpx;
	box-shadow: 0 5rpx 15rpx rgba(0, 0, 0, 0.07); /* Subtle shadow */
	overflow: hidden; /* Ensures border-radius clips list items */
    width: 100%; 
    box-sizing: border-box;
}

.list-item {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 35rpx 30rpx; 
	border-bottom: 1rpx solid #F0F0F0; /* Light separator line */
	background-color: #fff; /* Ensure item background is white */
    transition: background-color 0.15s ease-in-out; /* For touch feedback */
}

.list-item:last-child {
	border-bottom: none; /* No border for the last item */
}

.list-item:active {
    background-color: #F9F9F9; /* Slight darkening on touch */
}

.item-text {
	font-size: 30rpx;
	color: #333333; /* Dark grey text for items */
}

/* uni-icons styling is handled by its attributes (size, color) */

.logout-button-wrapper {
    padding-top: 50rpx;
    padding-bottom: 50rpx;
	width: 100%;
	// box-sizing: border-box;
}

.logout-button {
	background-color: white;
	color: #333333; 
	border: 1rpx solid #EAEAEA; /* Subtle border for the button */
	border-radius: 16rpx; /* Rounded corners for button */
	font-size: 32rpx;
	font-weight: normal;
	padding: 14rpx 0;
	text-align: center;
	margin-top: 28%;
	margin-bottom: 25%;
    box-shadow: 0 3rpx 8rpx rgba(141, 141, 141); /* Subtle shadow for button */
	width: 90%;
	heigh: 2%;
	box-sizing: border-box;
}
.logout-button:active {
    background-color: #FAFAFA; /* Feedback on press */
}

/* Remove default button border styling for uni-app */
.logout-button::after { 
	border: none;
}
</style>