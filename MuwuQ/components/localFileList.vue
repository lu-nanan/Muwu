<template>
	<view>
		<view class="file-list-container" >
			<scroll-view scroll-y="true" class="file-scroll-view">
				<view v-for="(file, index) in sortedFiles" :key="index">
					<view :class="{'file-item-container' : file.selected && isBatchModes}" @click="selected(file.name)">
						<localFileListItem class="file-item" :file="file" :checked="isBatchModes" />
					</view>
				</view>
				<button @click="readPublicDirectory()"></button>
			</scroll-view>
		</view>
	</view>
</template>

<script>
	import localFileListItem from '@/components/localFileListItem.vue'

	export default {
		data() {
			return {
				isBatchModes: false,
				files: [
					{
						name: '文件夹1',
						date: '2024-12-01',
						size: '1.22G',
						type: '文件夹',
						selected: false
					},
					{
						name: '文件夹2',
						date: '2024-12-01',
						size: '1.22G',
						type: '文件夹',
						selected: false
					},
					{
						name: '旅行照片',
						date: '2024-11-28',
						size: '5.6M',
						type: '图片',
						selected: false
					},
					{
						name: '工作报告',
						date: '2024-11-25',
						size: '2.3M',
						type: '文档',
						selected: false
					},
					{
						name: '会议视频',
						date: '2024-11-20',
						size: '156M',
						type: '视频',
						selected: false
					},
					{
						name: '语音备忘录',
						date: '2024-11-18',
						size: '3.2M',
						type: '音频',
						selected: false
					},
					{
						name: '项目计划书',
						date: '2024-11-15',
						size: '1.8M',
						type: '文档',
						selected: false
					},
					{
						name: '家庭视频',
						date: '2024-11-10',
						size: '230M',
						type: '视频',
						selected: true
					},
					{
						name: '工作文件夹',
						date: '2024-11-05',
						size: '1.22G',
						type: '文件夹',
						selected: false
					},
					{
						name: '系统备份',
						date: '2024-11-01',
						size: '4.5G',
						type: '文件夹',
						selected: false
					}
				],
				
            sortedFiles: []
			}
		},
		components: {
			localFileListItem,
		},
		created() {
			this.getFilesList();
			this.sortedFiles = this.files;
			
			uni.$on('sortedEvent',function(e){
				console.log('aminoac:   ' + e.detail.value);
				if( e.detail.value === 3){
					this.sortedFiles = [...this.files].sort((b, a) => {
					    const sizeA = this.getSizeInMB(a.size);
					    const sizeB = this.getSizeInMB(b.size);
					    return sizeA - sizeB;
					});
				}
				if( e.detail.value === 4){
					this.sortedFiles = [...this.files].sort((a, b) => {
					    const sizeA = this.getSizeInMB(a.size);
					    const sizeB = this.getSizeInMB(b.size);
					    return sizeA - sizeB;
					});
				}
			}.bind(this));
			
			uni.$on('toggleBatchModes', function(e) {
				console.log('监听到事件，携带参数为1：' + e);

				// 如果从 true 变为 false，输出被选中的文件并重置背景色
				if (this.isBatchModes === true && e === false) {
					const selectedFiles = this.files.filter(function(file) {
						return file.selected;
					});
					
					for (let i = 0; i < selectedFiles.length; i++) {
						console.log(selectedFiles[i].name);
					}
					
					for (let i = 0; i < this.files.length; i++) {
						this.files[i].selected = false;
					}
				}

				this.isBatchModes = e;
			}.bind(this));
		},
		methods: {
			
			
			selected(name) {
				if (this.isBatchModes === true) {
					for (let i = 0; i < this.files.length; i++) {
						if (this.files[i].name === name) {
							this.files[i].selected = !this.files[i].selected;
							break;
						}
					}
				}
				
				for (let i = 0; i < this.files.length; i++) {
					if (this.files[i].name === name) {
						console.log(this.files[i].name, this.files[i].selected);
						break;
					}
				}
			},
		        getSizeInMB(sizeStr) {
		            const value = parseFloat(sizeStr.slice(0, -1));
		            const unit = sizeStr.slice(-1).toUpperCase();
		            if (unit === 'G') {
		                return value * 1024;
		            } else if (unit === 'M') {
		                return value;
		            } else {
		                return 0;
		            }
		        },
				 handleFileSelect(event) {
				      const file = event.target.files[0];
				      if (file) {
				        this.selectedFile = file;
				        this.fileName = `已选择文件：${file.name}`;
				      }
				    },
				   
				
		    }
		};
</script>

<style>
	.file-item {
		width: 90%;
		background-color: #fff;
	}
	
	.file-item-container {
		background-color: #FFD700;
	}
	
	.file-list-container {
		flex: 1;
		margin: 0 15px;
		background-color: #fff;
		border-radius: 12px;
		overflow: hidden;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
	}

	.file-scroll-view {
		height: 100%;
	}
</style>