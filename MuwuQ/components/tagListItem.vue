<template>
  <view class="file-item">
    <view class="file-icon">
      <uni-icons type="folder-add" size="30"></uni-icons>
    </view>
    
    <view class="file-divider"></view>
    
    <view class="file-info">
      <view class="file-nametag">
        <text class="file-name">{{ file.name }}</text>
        <view class="file-tag">{{  file.tag? file.tag : '文件夹'}}</view>
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
    props:{
		 file: {
		      type: Object,
		    },
		    // 新增 prop：标签颜色
		    flagTagColor: {
		      type: String,   // 类型为字符串
		      default: '#333' // 默认值
		    },
		},
		
    data() {
      return {
		  // name: "文件夹1",
		  // date: "2024-12-1",
		  // size: "123G",
		  // tag: "工作"
	  };
    }
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