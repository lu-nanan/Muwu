<template>
	<view>
		<view class="file-list-container">
			<scroll-view scroll-y="true" class="file-scroll-view">
				<view v-for="(file, index) in files" :key="index">
					<view :class="{'file-item-container' : file.selected && isBatchModes}" @click="selected(file)" @longpress="">
						<historyListItem class="file-item" :file="file" />
					</view>
				</view>
			</scroll-view>
		</view>
	</view>
</template>

<script>
	import historyListItem from '@/components/historyListItem.vue'

	export default {
		props: {
		    files: {
		      type: Array,
		      default: () => [], // 默认空数组
		    }
		  },
		data() {
			return {
				// 示例文件数据
				
			}
		},
		methods:{
			selected(file){
				uni.$emit('shareTap',file);
			}
		},
		components: {
			historyListItem,
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