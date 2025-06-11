<template>
  <view class="file-item">
    <view class="file-icon">
      <uni-icons type="folder-add" size="30"></uni-icons>
    </view>
    
    <view class="file-divider"></view>
    
    <view class="file-info">
      <view class="file-nametag">
        <text class="file-name">{{ file.name }}</text>
      </view>
      <view class="file-datesize">
        <text class="file-date">{{ file.date }}</text>
        <text class="file-size">{{ file.size }}</text>
      </view>
    </view>
  </view>
</template>

<script>
	export default {
		props:["file"]
	}
</script>

<style>
.file-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 12px 15px;
  border-bottom: 1px solid #f5f5f5;
}

.file-icon {
  width: 60rpx;
  height: 40rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 12px;
}

.file-divider {
  width: 1px;
  height: 40px;
  background-color: #e0e0e0;
  margin-right: 15px;
}

.file-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.file-nametag {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.file-name { 
	font-size: 16px;
  font-weight: bold;
  color: #333;
  white-space: nowrap;      /* 禁止换行 */
  overflow: hidden;         /* 超出部分隐藏 */
  text-overflow: ellipsis;  /* 显示省略号 */
  max-width: 250px;         /* 设置最大宽度，根据需要调整 */
}

.file-tag {
  padding: 2px 15px;
  background-color: #4285f4;
  border-radius: 20px;
  color: white;
  font-size: 14px;
  text-align: center;
}

.file-datesize {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.file-date {
  font-size: 14px;
  color: #666;
}

.file-size {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  padding-right: 20rpx;
}
</style>