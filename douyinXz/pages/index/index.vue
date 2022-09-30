<template>
	<view class="content">
		<view class="text-area">
			<textarea placeholder="请输入url链接" @input="inputUrl" :value="jqurl">
				
			</textarea>
			
		</view>
		<view class="btn"  @click="reqUrl">
			点击解析视频,支持快手抖音
		</view>
		<view class="showBox"  v-if="boxShow">
			<view class="textBox">
				<text>视频标题:{{signature}}</text>
				<text>用户名:{{nickname}}</text>
			</view>
			<view class="img">
				
				<image :src="imgurl" mode="scaleToFill"></image>
			</view>
			<view class="btn" @click="saveVideo">
				点击下载
			</view>
		</view>
		
	</view>
</template>

<script>
	// import popup from '../../uni_modules/uni-popup/uni-popup.vue'
	export default {
		data() {
			return {
				url:'',
				imgurl:'',
				signature:'',
				nickname:'',
				videourl:'',
				boxShow:false,
				jqurl:'',
				type:'',
			}
		},
		onLoad() {
			
		},
		methods: {
			inputUrl(e){
				
				this.url = e.detail.value
			},
			reqUrl(){
				// uni.vibrate({
					
				// });
				let index = this.url.indexOf('http');
				if(this.url.indexOf('kuaishou')> -1){
					this.type = 'ks'
				}else if(this.url.indexOf('douyin')> -1){
					this.type = 'dy'
				}
				this.jqurl = this.url.slice(index,this.url.length);
				if(this.jqurl.length==0){
					uni.showToast({
						icon:'none',
						'title':'请输入链接'
					});
					return;
				}
				uni.showLoading({ mask: true, title: '解析中' })
				uni.request({
				    url: '', //仅为示例，并非真实接口地址。
				    data: {
				        url:this.jqurl,
						type:this.type
				    },
					method:"GET",
					timeout:15000,
				    header: {
				        
				    },
				    success: (res) => {
						uni.hideLoading();
						uni.showToast({
							icon:'none',
							'title':'解析成功'
						})
						this.boxShow = true;
				        this.imgurl =  res.data.data.coverurl;
						this.signature =  res.data.data.signature
						this.nickname =  res.data.data.nickname
						this.videourl = res.data.data.videourl
				    },
					fail: () => {
						uni.hideLoading();
					},
					
				});
			},
			saveVideo(){
				 uni.showLoading({ mask: true, title: '加载中' })
				      // 先下载视频
				      uni.downloadFile({
				        url:encodeURI(this.videourl),
				        success: (res) => {
				          const that = this
				 
				          if (res.statusCode === 200) {
				            // 关闭loading
				            uni.hideLoading()
				 
				            // 保存视频到手机相册
				            uni.saveVideoToPhotosAlbum({
				              filePath: res.tempFilePath,
				              success: function() {
				               uni.showToast({
				               	icon:"success",
								title: '保存成功',
				               })
				              }
				            })
				          }
				 
				        },
						fail: (err) => {
							console.log(err)
						}
				      })
			}
		}
	}
</script>

<style lang="scss">
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}
	.btn{
		width: 60%;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100rpx;
		border-radius: 20rpx;
		font-size: 36rpx;
		background:#00aaff;
		color: #fff;
	}
	.showBox{
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}
	.textBox{
		margin-top:100rpx;
	}
	.img{
		height: 400rpx;
		width: 400rpx;
		margin: 100rpx 0;
		>image{
			height: 400rpx;
			width: 400rpx;
		}
	}
	.xzbox{}
</style>
