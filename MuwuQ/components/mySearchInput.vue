<template>
	<view>
		<uni-search-bar class="searchbar" @confirm="search" :focus="false" @blur="blur" @focus="focus" placeholder="请输入文字"></uni-search-bar>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				
			};
		},
		methods:{
			search(res) {
				uni.showToast({
					title: '搜索：' + res.value,
					icon: 'none'
				})
			},
			blur(res) {
				uni.showToast({
					title: 'blur事件，输入值为：' + res.value,
					icon: 'none'
				})
			},
			focus(e) {
				uni.showToast({
					title: 'focus事件，输出值为：' + e.value,
					icon: 'none'
				})
			},
			change(e) {
				console.log('e:', e);
			}
		}
	}
</script>

<style>
.searchbar{
}
</style>