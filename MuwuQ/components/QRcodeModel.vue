<template>
  <view class="qrcode-modal" v-show="isShow">
    <!-- 背景遮罩 -->
    <view class="mask" @click="closeModal"></view>
    
    <!-- 弹窗内容 -->
    <view class="modal-content">
      <view class="header">
        <text class="title">二维码信息</text>
        <text class="close-btn" @click="closeModal()">×</text>
      </view>
      
      <!-- 二维码展示区域 -->
      <view class="qrcode-container">
        <image 
          :src="qrcodeUrl" 
          mode="widthFix" 
          class="qrcode-image"
          placeholder-class="qrcode-placeholder"
        />
      </view>
      
      <!-- 提示文本（可选） -->
      <text v-if="tipText" class="tip">{{ tipText }}</text>
    </view>
  </view>
</template>

<script>
export default {
  props: {
    isShow: {
      type: Boolean,
      default: false
    },
    qrcodeUrl: {
      type: String,
      required: true
    },
    tipText: {
      type: String,
      default: '长按保存二维码'
    }
  },
  methods: {
    closeModal() {
      this.$emit('close'); // 触发关闭事件
    }
  }
};
</script>

<style scoped>
.qrcode-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mask {
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: rgba(253, 253, 253, 0.5);
}

.modal-content {
  background-color: white;
  border-radius: 16rpx;
  padding: 32rpx;
  max-width: 600rpx;
  width: 80%;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
}

.title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
}

.close-btn {
  font-size: 32rpx;
  color: #666;
  cursor: pointer;
}

.qrcode-container {
  width: 100%;
  height: 400rpx;
  margin: 24rpx 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f8f8f8;
  border-radius: 12rpx;
}

.qrcode-image {
  max-width: 100%;
  max-height: 100%;
}

.tip {
  font-size: 24rpx;
  color: #666;
  text-align: center;
  
}
</style>