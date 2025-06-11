<template>
	<view class="content">
		<upload
		      :path="path"    
		      :tag="tag"      
		    />
		<ss-upload ref="ssUpload" width="260rpx" height="100rpx" @getFile="getFile" @uploadSuccess="uploadSuccess"
			:uploadOptions="uploadOptions" :isUploadServer="isUploadServer" :webviewStyle="webviewStyle"
			:fileInput="fileInput">
			<image class="background-image" src="/static/7_E}6DMMKB]MN90($703355_tmb.png" mode="heightFix" @click="uploadFile" :style="{ zIndex: show }"></image>
		</ss-upload>
		 
	</view>

</template>

	<script>
		import upload from '@/components/upload.vue'
		export default {
			data() {
				return {
					show:1,
					path:'',
					tag: '',
					message: '',
					fileLists: null,
					files: [],
					filesApp: '',
					isUploadServer: true,
					uploadOptions: {
						// 上传服务器地址，此地址需要替换为你的接口地址
						//不能用全局变量不然会炸
						url: 'https://6c15e199.r21.cpolar.top/file/upload', //仅为示例，非真实的接口地址,
						//请求方式，get,post
						type: 'post',
						// 上传附件的key
						name: 'file',
						// 根据你接口需求自定义请求头
						header: {
							'Accept': 'application/json'
						},
						// 根据你接口需求自定义body参数
						formData: {
							userId: getApp().globalData.userInfo.id
						}
					},
					webviewStyle: {
						height: '50px',
						width: '130px',
						position: 'static',
						background: 'transparent',
						top: '50px',
						left: '24px',
					},
					fileInput: { //设置app端html里面input样式与内容
						fileStyle: {
							borderRadius: '10px',
							backgroundColor: '#1975F7',
							color: '#fff',
							fontSize: '20px',
						},
						fileTitle: '上传附件'
					},
					result: ''
				};
			},
			components:{
				upload,
			},
			created(){
				uni.$on('uploadend' ,function(e){
					this.show=1;
				}.bind(this));
			},
			methods: {
				scrolltolower() {
					console.log(145623)
					this.$refs.ssUpload.hide();
					setTimeout(() => {
						this.$refs.ssUpload.show();
					})
				},
				uploadFile() {
					console.log(getApp().globalData.userInfo.id)
					//#ifdef H5 || MP-WEIXIN
					setTimeout(() => {
						this.$refs.ssUpload.uploadFile()
					})
					// #endif
					
						uni.showToast({
						  title: '加载中...',
						  icon: 'loading',
						  duration: 30000, // 防止长时间请求导致提示自动消失
						  mask: true // 显示遮罩层，防止用户操作
						});
				},
				//获取文件
				getFile(result) {
					console.log('结果结果结果', result)
					//#ifdef H5 || MP-WEIXIN
					this.files = result.tempFiles
					// #endif
					// #ifdef APP-PLUS
					this.filesApp = result
					// #endif
				},
				uploadSuccess(result) {
					uni.hideToast();
					console.log('上传服务器后端返回结果', result) //后期取值可以在这里做操作
					this.result = JSON.stringify(result)
					const fileInfo = result[0]; // 获取数组中的对象
					this.show=-1;
					this.path=fileInfo.filePath;
					this.tag= fileInfo.tag || '工作';
					console.log(this.path);
					console.log(this.tag);
					
				}
			}
		};
	</script>


<style>
.content {
	display: flex;
	flex-direction: column;
  background-color: #8D8DC1;
  width: 100%;
  height: 100%;
}
.background-image {
		position: fixed;
		width: 100%;
		height: 100%;
		top: 0;
		left: 0;
		z-index: -1;
	}
</style>