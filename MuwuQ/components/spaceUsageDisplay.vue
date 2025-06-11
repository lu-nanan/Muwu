<template>
	<view>
		<view class="content-wrapper">
				<view class="content">
					<!-- 左侧环状图 -->
					<view class="chart-container">
						<view class="chart-inner">
							<view class="ring-progress"
								:style="{ background: `conic-gradient(#FFD700 ${usedPercents}%, #EAEEF4 0%)` }">
								<view class="ring-inner">
		<!-- 							<text class="percentage">{{ Math.round(usedPercent) }}%</text> -->
									<text class="usage-label">内存使用率</text>
								</view>
							</view>
						</view>
					</view>
		
					<!-- 右侧数据 -->
					<view class="data-container">
						<view class="data-item">
							<text class="label">已用内存</text>
							<text class="value">{{ usedStorage }} / {{ totalStorage }}</text>
						</view>
						<view class="data-item">
							<text class="label">文件数目</text>
							<text class="value">{{ fileCount }} 个</text>
						</view>
						<view class="data-item">
							<text class="infos">已用 {{usePercentages}}, 可放心使用</text>
						</view>
					</view>
				</view>
			</view>
	</view>
</template>

<script>
	export default {
		name:"spaceUsageDisplay",
		data() {
			return {
				usedStorage: '3.2GB',
				totalStorage: '8.0GB',
				usedPercents: 40,
				fileCount: 152
			};
		},
		computed:{
			usePercentages: function() {
				let usedPercent = 40
				return usedPercent + "%"
			}
		}
	}
</script>

<style>
/* 内容容器 */
	.content-wrapper {
		/* 为固定的导航栏腾出空间 */
		width: 100%;
		padding: 20rpx;
		display: flex;
		flex-direction: row;
		box-sizing: border-box;
	}

	.content {
		width: 100%;
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
		padding: 40rpx 20rpx;
		background: #8d8dc1;
		border-radius: 10rpx;
/* 		box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05); */
	}

	/* 环状图容器 */
	.chart-container {
		width: 38%;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.chart-inner {
		position: relative;
		width: 240rpx;
		height: 240rpx;
	}

	/* 环形进度条 */
	.ring-progress {
		width: 100%;
		height: 100%;
		border-radius: 50%;
		display: flex;
		justify-content: center;
		align-items: center;
		mask: radial-gradient(transparent 55%, white 56%);
		-webkit-mask: radial-gradient(transparent 55%, white 56%);
	}

	.ring-inner {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}

	.percentage {
		font-size: 48rpx;
		font-weight: bold;
		color: #2FC25B;
	}

	.usage-label {
		position: absolute;
		font-size: 24rpx;
		color: #ffffff;
/* 		margin-top: 6rpx; */
	}

	/* 数据容器 */
	.data-container {
		flex: 1;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: flex-start;
		padding-left: 40rpx;
	}

	.data-item {
		margin-bottom: 30rpx;
		width: 100%;
	}

	.label {
		display: block;
		font-size: 26rpx;
		color: #dfdfdf;
		margin-bottom: 8rpx;
	}

	.value {
		font-size: 32rpx;
		color: #ffffff;
		font-weight: bold;
	}
	
	.infos{
		font-size: 26rpx;
		color: #ffffff;
		margin-bottom: 8rpx;
	}
</style>