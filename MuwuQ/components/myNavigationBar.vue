<template>
	<view>
		<view class="custom-navbar">
			<!-- 排序方式 -->
			<picker mode="selector" :range="sortOptions" @change="handleSortChange" class="nav-item">
				<view class="nav-item-text">{{ currentSort }}</view>
			</picker>

			<!-- 文件类型 -->
			<picker mode="selector" :range="fileOptions" @change="handleFileChange" class="nav-item">
				<view class="nav-item-text">{{ currentFile }}</view>
			</picker>

			<!-- 批量操作 -->
			<view class="nav-item" @click="toggleBatchMode">
				<text class="nav-item-text" :class="{'batch-active': isBatchMode}">
					{{ isBatchMode ? '完成' : '批量操作' }}
				</text>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			sortOptions: ['默认排序','最近使用', '最久未用', '从大到小', '从小到大'],
			currentSort: '默认排序',
			fileOptions: ['所有文件', '图片', '文件', '文件夹', '视频', '音频'],
			currentFile: '所有文件',
			isBatchMode: false,
		}
	},
	methods: {
		handleSortChange(e) {
			this.currentSort = this.sortOptions[e.detail.value]
			uni.$emit('sortedEvent',e)
		},

		handleFileChange(e) {
			this.currentFile = this.fileOptions[e.detail.value]
		},

		toggleBatchMode() {
			this.isBatchMode = !this.isBatchMode
			uni.$emit('toggleBatchModes', this.isBatchMode)
		}
	}
}
</script>

<style>
/* 导航栏样式 */
.custom-navbar {
	display: flex;
	flex-direction: row;
	align-items: center;
	height: 120rpx;
	background-color: #fff;
	border-bottom: 1px solid #f0f0f0;
}

.nav-item {
	flex: 1;
	text-align: center;
	padding: 0 15px;
}

.nav-item-text {
	text-align: center;
	font-size: 14px;
	color: #333;
}

/* 批量操作状态样式 */
.batch-active {
	color: #007AFF;
}

</style>