<template>
	<view>
		<view class="file-list-container">
			<scroll-view scroll-y="true" class="file-scroll-view">
				<view v-for="(file, index) in sortedFiles" :key="index">
					<view :class="{'file-item-container' : file.selected && isBatchModes}" @click="selected(file)" @longpress="">
						<cloudFileListItem class="file-item" :file="file" />
					</view>
				</view>
			</scroll-view>
		</view>
	</view>
</template>

<script>
	import { watch } from 'vue';
import cloudFileListItem from '@/components/cloudFileListItem.vue';

	export default {
		props: {
		    files: {
		      type: Array,
		      default: () => [], // 默认空数组
		    }
		  },
		data() {
			return {
				isBatchModes: false,
				sortedFiles: []
			}
		},
		components: {
			cloudFileListItem,
		},
		watch: {
		    files(newValue, oldValue) {
		      this.sortedFiles=newValue;
		    }
		},
		created() {
				
					
			
			uni.$on('sortedEvent',function(e){
				console.log('aminoac:   ' + e.detail.value);
				if (e.detail.value === 3) {
				  // 降序：无size的元素排在最后
				  this.sortedFiles = [...this.files].sort((b, a) => {
				    // 先判断是否有size属性
				    if (a.size === undefined && b.size !== undefined) return -1;
				    if (b.size === undefined && a.size !== undefined) return 1;
				    if (a.size === undefined && b.size === undefined) return 0;
				    // 都有size属性时，按大小降序
				    return a.trueSize - b.trueSize;
				  });
				}
				
				if (e.detail.value === 4) {
				  // 升序：无size的元素排在最前
				  this.sortedFiles = [...this.files].sort((a, b) => {
				    // 先判断是否有size属性
				    if (a.size === undefined && b.size !== undefined) return 1;
				    if (b.size === undefined && a.size !== undefined) return -1;
				    if (a.size === undefined && b.size === undefined) return 0;
				    // 都有size属性时，按大小升序
				    return a.trueSize - b.trueSize;
				  });
				  
  console.log('升序排序后的数组:', JSON.stringify(this.sortedFiles, null, 2));
				}
			}.bind(this));
			uni.$on('toggleBatchModes', function(e) {
				console.log('监听到事件，携带参数为：' + e);

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
			selected(file) {
				uni.$emit('jump',file);
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
			}
		}
	}
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
	.dropdown {
	  position: absolute;
	  top: 100%;
	  left: 0;
	  background-color: #fff;
	  border: 1px solid #ccc;
	  border-radius: 4px;
	  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}
	
	.dropdown-item {
	  padding: 10px 20px;
	  cursor: pointer;
	}
	
	.dropdown-item:hover {
	  background-color: #f0f0f0;
	}
</style>