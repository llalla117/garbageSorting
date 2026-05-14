<template>
	<div class="garbage-education-container">
		<div class="hero-section">
			<div class="carousel-container">
				<el-carousel height="400px" indicator-position="bottom" :autoplay="true" :interval="4000" arrow="hover">
					<el-carousel-item v-for="(item, index) in carouselImages" :key="index">
						<div class="carousel-item">
							<img :src="item.url" :alt="item.title" class="carousel-image" />
							<div class="carousel-overlay">
								<h2 class="carousel-title">{{ item.title }}</h2>
								<p class="carousel-subtitle">{{ item.subtitle }}</p>
							</div>
						</div>
					</el-carousel-item>
				</el-carousel>
			</div>
		</div>

		<div class="modules-section">
			<div class="container">
				<h2 class="section-title">垃圾分类知识</h2>
				<p class="section-subtitle">了解更多垃圾分类知识，从身边小事做起</p>
				
				<el-row :gutter="20" class="modules-row">
					<el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
						<el-card class="module-card" shadow="hover" @click="scrollToSection('harm-section')">
							<div class="module-icon-wrapper harm-icon">
								<el-icon :size="48"><Warning /></el-icon>
							</div>
							<h3 class="module-title">垃圾的危害</h3>
							<p class="module-description">了解垃圾对环境和健康的危害，增强环保意识</p>
							<el-button type="primary" class="module-btn">查看详情</el-button>
						</el-card>
					</el-col>
					
					<el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
						<el-card class="module-card" shadow="hover" @click="scrollToSection('treatment-section')">
							<div class="module-icon-wrapper treatment-icon">
								<el-icon :size="48"><Tools /></el-icon>
							</div>
							<h3 class="module-title">处理方式</h3>
							<p class="module-description">了解常见的垃圾处理方法，选择环保方式</p>
							<el-button type="primary" class="module-btn">查看详情</el-button>
						</el-card>
					</el-col>
					
					<el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
						<el-card class="module-card" shadow="hover" @click="scrollToSection('tips-section')">
							<div class="module-icon-wrapper tips-icon">
								<el-icon :size="48"><Lightbulb /></el-icon>
							</div>
							<h3 class="module-title">分类贴士</h3>
							<p class="module-description">掌握垃圾分类小技巧，轻松做好分类</p>
							<el-button type="primary" class="module-btn">查看详情</el-button>
						</el-card>
					</el-col>
				</el-row>
			</div>
		</div>

		<div id="harm-section" class="content-section">
			<div class="container">
				<el-card shadow="hover" class="content-card">
					<template #header>
						<div class="card-header">
							<el-icon class="header-icon harm-header-icon"><Warning /></el-icon>
							<span class="header-title">垃圾的危害</span>
						</div>
					</template>
					<div class="harm-content">
						<el-row :gutter="20">
							<el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" v-for="harm in harms" :key="harm.title">
								<div class="harm-item">
									<div class="harm-icon-wrapper">
										<el-icon :size="32">
											<component :is="iconComponents[harm.icon]" />
										</el-icon>
									</div>
									<h3>{{ harm.title }}</h3>
									<p>{{ harm.description }}</p>
									<ul class="harm-details">
										<li v-for="(detail, index) in harm.details" :key="index">{{ detail }}</li>
									</ul>
								</div>
							</el-col>
						</el-row>
					</div>
				</el-card>
			</div>
		</div>

		<div id="treatment-section" class="content-section">
			<div class="container">
				<el-card shadow="hover" class="content-card">
					<template #header>
						<div class="card-header">
							<el-icon class="header-icon treatment-header-icon"><Tools /></el-icon>
							<span class="header-title">常见垃圾处理方式</span>
						</div>
					</template>
					<div class="treatment-content">
						<el-timeline>
							<el-timeline-item v-for="treatment in treatments" :key="treatment.title" :timestamp="treatment.title" placement="top" :color="treatment.color">
								<el-card shadow="hover" class="treatment-item">
									<h4>{{ treatment.title }}</h4>
									<p>{{ treatment.description }}</p>
									<div class="treatment-advantages">
										<el-tag v-for="(advantage, index) in treatment.advantages" :key="index" type="success" size="small" class="advantage-tag">{{ advantage }}</el-tag>
									</div>
									<div class="treatment-applications">
										<span class="application-label">适用范围：</span>
										<span v-for="(app, index) in treatment.applications" :key="index" class="application-item">{{ app }}</span>
									</div>
								</el-card>
							</el-timeline-item>
						</el-timeline>
					</div>
				</el-card>
			</div>
		</div>

		<div id="tips-section" class="content-section">
			<div class="container">
				<el-card shadow="hover" class="content-card">
					<template #header>
						<div class="card-header">
							<el-icon class="header-icon tips-header-icon"><Lightbulb /></el-icon>
							<span class="header-title">垃圾分类小贴士</span>
						</div>
					</template>
					<div class="tips-content">
						<el-row :gutter="15">
							<el-col :xs="24" :sm="12" :md="8" :lg="8" :xl="8" v-for="(tip, index) in tips" :key="index">
								<div class="tip-item">
									<div class="tip-number">{{ index + 1 }}</div>
									<p>{{ tip }}</p>
								</div>
							</el-col>
						</el-row>
					</div>
				</el-card>
			</div>
		</div>

		<div class="footer-section">
			<div class="container">
				<p class="footer-text">© 2024 垃圾分类识别系统 - 保护环境，人人有责</p>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts" name="garbageEducation">
import { reactive } from 'vue';
import { Warning, Tools, Lightbulb, DeleteFilled } from '@element-plus/icons-vue';

const iconComponents: Record<string, any> = {
	Warning,
	Tools,
	Lightbulb,
	DeleteFilled
};

const carouselImages = reactive([
	{
		url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=beautiful%20green%20city%20with%20recycling%20bins%20environmental%20protection&image_size=landscape_16_9',
		title: '共建美丽城市',
		subtitle: '垃圾分类，从我做起'
	},
	{
		url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=green%20forest%20nature%20environmental%20protection%20sustainable%20living&image_size=landscape_16_9',
		title: '守护绿色家园',
		subtitle: '让天更蓝，水更清'
	},
	{
		url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=happy%20family%20recycling%20garbage%20sorting%20eco%20friendly%20lifestyle&image_size=landscape_16_9',
		title: '践行垃圾分类',
		subtitle: '共创美好未来'
	}
]);

const harms = reactive([
	{
		title: '环境污染',
		icon: 'Warning',
		description: '垃圾对环境造成的污染是多方面的，严重影响生态平衡',
		details: ['土壤污染：有害物质渗透土壤，破坏土壤结构', '水体污染：垃圾渗滤液污染地下水和地表水', '空气污染：垃圾分解产生有害气体，影响空气质量']
	},
	{
		title: '资源浪费',
		icon: 'DeleteFilled',
		description: '未分类的垃圾导致大量可回收资源被浪费',
		details: ['可回收物混入其他垃圾，无法再利用', '资源循环利用率低，增加原材料开采', '能源消耗增加，加重环境负担']
	},
	{
		title: '健康危害',
		icon: 'Warning',
		description: '垃圾处理不当对人体健康造成严重威胁',
		details: ['滋生细菌病毒，传播疾病', '有害物质通过食物链进入人体', '空气污染引发呼吸系统疾病']
	},
	{
		title: '经济损失',
		icon: 'DeleteFilled',
		description: '垃圾处理不当造成巨大的经济损失',
		details: ['垃圾处理成本高昂', '环境污染治理费用巨大', '资源浪费导致经济损失']
	}
]);

const treatments = reactive([
	{
		title: '填埋处理',
		description: '将垃圾填入坑洼地中，通过微生物分解达到无害化处理',
		color: '#409EFF',
		advantages: ['技术简单', '处理量大', '成本较低'],
		applications: ['无机垃圾', '建筑垃圾', '最终处置']
	},
	{
		title: '焚烧处理',
		description: '通过高温燃烧将垃圾转化为灰渣、气体和热量',
		color: '#67C23A',
		advantages: ['减量化显著', '无害化彻底', '可回收能源'],
		applications: ['可燃垃圾', '医疗垃圾', '高热值垃圾']
	},
	{
		title: '堆肥处理',
		description: '利用微生物分解有机垃圾，生产有机肥料',
		color: '#E6A23C',
		advantages: ['资源化利用', '改善土壤', '减少污染'],
		applications: ['厨余垃圾', '园林废弃物', '农业废弃物']
	},
	{
		title: '回收利用',
		description: '将可回收物进行分类、加工，重新利用',
		color: '#F56C6C',
		advantages: ['节约资源', '减少污染', '经济效益好'],
		applications: ['纸张', '塑料', '金属', '玻璃']
	}
]);

const tips = reactive([
	'投放前请沥干水分，特别是厨余垃圾',
	'有尖锐边角的垃圾请用纸包裹后再投放',
	'玻璃制品请轻放，避免破碎伤人',
	'电池等有害垃圾请单独投放，不要混入其他垃圾',
	'大件垃圾请预约回收，不要随意丢弃',
	'不确定分类时，请查询分类指南或询问工作人员'
]);

const scrollToSection = (sectionId: string) => {
	const element = document.getElementById(sectionId);
	if (element) {
		element.scrollIntoView({ behavior: 'smooth' });
	}
};
</script>

<style scoped lang="scss">
.garbage-education-container {
	min-height: 100vh;
	background: #f5f7fa;
}

.hero-section {
	width: 100%;
	position: relative;
	margin-bottom: 40px;
}

.carousel-container {
	max-width: 1400px;
	margin: 0 auto;
	padding: 20px;
}

.carousel-item {
	position: relative;
	height: 100%;
	border-radius: 12px;
	overflow: hidden;
}

.carousel-image {
	width: 100%;
	height: 100%;
	object-fit: cover;
}

.carousel-overlay {
	position: absolute;
	bottom: 0;
	left: 0;
	right: 0;
	background: linear-gradient(to top, rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0));
	padding: 60px 40px 40px;
	color: white;
}

.carousel-title {
	font-size: 36px;
	font-weight: bold;
	margin-bottom: 10px;
	text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.carousel-subtitle {
	font-size: 18px;
	opacity: 0.9;
}

.modules-section {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	padding: 40px 0;
}

.container {
	max-width: 1400px;
	margin: 0 auto;
	padding: 0 20px;
}

.section-title {
	text-align: center;
	font-size: 32px;
	font-weight: bold;
	color: white;
	margin-bottom: 10px;
}

.section-subtitle {
	text-align: center;
	font-size: 16px;
	color: rgba(255, 255, 255, 0.8);
	margin-bottom: 30px;
}

.modules-row {
	margin-bottom: 0;
}

.module-card {
	height: 100%;
	text-align: center;
	padding: 30px 20px;
	background: white;
	border-radius: 16px;
	cursor: pointer;
	transition: all 0.3s ease;
	
	&:hover {
		transform: translateY(-10px);
		box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
	}
}

.module-icon-wrapper {
	width: 80px;
	height: 80px;
	border-radius: 50%;
	display: flex;
	align-items: center;
	justify-content: center;
	margin: 0 auto 20px;
	
	&.harm-icon {
		background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
		color: white;
	}
	
	&.treatment-icon {
		background: linear-gradient(135deg, #42e695 0%, #3bb2b8 100%);
		color: white;
	}
	
	&.tips-icon {
		background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
		color: white;
	}
}

.module-title {
	font-size: 22px;
	font-weight: bold;
	color: #333;
	margin-bottom: 10px;
}

.module-description {
	font-size: 14px;
	color: #666;
	margin-bottom: 20px;
	line-height: 1.6;
}

.module-btn {
	border-radius: 20px;
	padding: 8px 24px;
}

.content-section {
	padding: 40px 0;
}

.content-card {
	border-radius: 16px;
	overflow: hidden;
	
	:deep(.el-card__header) {
		background: white;
		border-bottom: 1px solid #eee;
		padding: 20px;
	}
}

.card-header {
	display: flex;
	align-items: center;
	
	.header-icon {
		margin-right: 12px;
		font-size: 28px;
		
		&.harm-header-icon {
			color: #ff6b6b;
		}
		
		&.treatment-header-icon {
			color: #42e695;
		}
		
		&.tips-header-icon {
			color: #f093fb;
		}
	}
	
	.header-title {
		font-size: 22px;
		font-weight: bold;
		color: #333;
	}
}

.harm-content {
	padding: 20px;
}

.harm-item {
	background: #f8f9fa;
	padding: 25px;
	border-radius: 12px;
	margin-bottom: 20px;
	transition: all 0.3s ease;
	
	&:hover {
		background: #e9ecef;
		transform: translateX(5px);
	}
	
	.harm-icon-wrapper {
		color: #667eea;
		margin-bottom: 15px;
	}
	
	h3 {
		font-size: 18px;
		margin-bottom: 12px;
		color: #333;
	}
	
	p {
		font-size: 14px;
		color: #666;
		margin-bottom: 15px;
		line-height: 1.6;
	}
	
	.harm-details {
		list-style: none;
		padding: 0;
		margin: 0;
		
		li {
			padding: 10px 0;
			padding-left: 25px;
			position: relative;
			font-size: 13px;
			color: #555;
			border-bottom: 1px dashed #ddd;
			
			&:last-child {
				border-bottom: none;
			}
			
			&::before {
				content: '✓';
				position: absolute;
				left: 5px;
				color: #67C23A;
				font-weight: bold;
			}
		}
	}
}

.treatment-content {
	padding: 20px;
}

.treatment-item {
	margin-bottom: 15px;
	padding: 20px;
	
	h4 {
		font-size: 18px;
		color: #333;
		margin-bottom: 12px;
		font-weight: bold;
	}
	
	p {
		font-size: 14px;
		color: #666;
		margin-bottom: 15px;
		line-height: 1.6;
	}
	
	.treatment-advantages {
		margin-bottom: 15px;
		
		.advantage-tag {
			margin-right: 10px;
			margin-bottom: 8px;
		}
	}
	
	.treatment-applications {
		.application-label {
			font-weight: bold;
			color: #333;
			margin-right: 10px;
		}
		
		.application-item {
			display: inline-block;
			background: #f0f2f5;
			padding: 5px 14px;
			border-radius: 18px;
			font-size: 13px;
			margin-right: 10px;
			margin-bottom: 8px;
			color: #666;
		}
	}
}

.tips-content {
	padding: 20px;
}

.tip-item {
	display: flex;
	align-items: flex-start;
	padding: 20px;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	border-radius: 12px;
	margin-bottom: 15px;
	color: white;
	transition: all 0.3s ease;
	
	&:hover {
		transform: translateY(-5px);
		box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
	}
	
	.tip-number {
		flex-shrink: 0;
		width: 36px;
		height: 36px;
		background: rgba(255, 255, 255, 0.3);
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: bold;
		font-size: 16px;
		margin-right: 15px;
	}
	
	p {
		flex: 1;
		font-size: 14px;
		line-height: 1.6;
		margin: 0;
	}
}

.footer-section {
	background: #333;
	padding: 30px 0;
	margin-top: 40px;
	
	.footer-text {
		text-align: center;
		color: #aaa;
		font-size: 14px;
	}
}

@media (max-width: 768px) {
	.carousel-title {
		font-size: 24px;
	}
	
	.carousel-subtitle {
		font-size: 14px;
	}
	
	.section-title {
		font-size: 24px;
	}
	
	.module-card {
		padding: 20px;
	}
	
	.module-title {
		font-size: 18px;
	}
	
	.module-description {
		font-size: 13px;
	}
}
</style>
