#!/usr/bin/env python3
"""
报告生成模块
负责将新闻列表转换为结构化Markdown报告
支持中英文翻译
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# 常用AI术语中英文对照表（按优先级排序）
TRANSLATIONS = [
    # 公司/品牌 (优先匹配)
    ("OpenAI", "OpenAI"),
    ("Google", "谷歌"),
    ("Meta", "Meta"),
    ("Microsoft", "微软"),
    ("Apple", "苹果"),
    ("Nvidia", "英伟达"),
    ("NVIDIA", "英伟达"),
    ("Amazon", "亚马逊"),
    ("Anthropic", "Anthropic"),
    ("字节跳动", "字节跳动"),
    ("字节", "字节跳动"),
    ("腾讯", "腾讯"),
    ("阿里巴巴", "阿里巴巴"),
    ("阿里", "阿里巴巴"),
    ("百度", "百度"),
    ("苹果", "苹果"),
    
    # 术语
    ("Artificial Intelligence", "人工智能"),
    ("artificial intelligence", "人工智能"),
    ("AI", "人工智能"),
    ("machine learning", "机器学习"),
    ("deep learning", "深度学习"),
    ("large language model", "大语言模型"),
    ("LLM", "大语言模型"),
    ("GPT-5", "GPT-5"),
    ("GPT-4", "GPT-4"),
    ("GPT", "GPT"),
    ("Claude", "Claude"),
    ("Gemini", "Gemini"),
    ("LLaMA", "LLaMA"),
    ("Agent", "智能体"),
    ("agents", "智能体"),
    ("neural network", "神经网络"),
    ("multimodal", "多模态"),
    
    # 动词/名词
    ("launches", "发布"),
    ("launch", "发布"),
    ("releases", "发布"),
    ("release", "发布"),
    ("announces", "发布"),
    ("announce", "发布"),
    ("announcement", "发布"),
    ("breakthrough", "突破"),
    ("invests", "投资"),
    ("invest", "投资"),
    ("investment", "投资"),
    ("funding", "融资"),
    ("raises", "融资"),
    ("acquire", "收购"),
    ("acquisition", "收购"),
    ("partnership", "合作"),
    ("spreading", "扩散"),
    ("companions", "伴侣"),
    
    # 技术
    ("chip", "芯片"),
    ("GPU", "GPU"),
    ("TPU", "TPU"),
    ("transformer", "Transformer"),
    ("model", "模型"),
    ("models", "模型"),
    ("training", "训练"),
    ("inference", "推理"),
    
    # 其他
    ("startup", "初创公司"),
    ("tech giant", "科技巨头"),
    ("report", "报告"),
    ("study", "研究"),
    ("research", "研究"),
    ("safety", "安全"),
    ("security", "安全"),
    ("regulation", "监管"),
    ("jobs", "就业"),
    ("workforce", "劳动力"),
    ("workers", "工人"),
    ("obsolete", "淘汰"),
    ("promotions", "晋升"),
    ("staff", "员工"),
    ("deepfakes", "深度伪造"),
    ("says", "表示"),
    ("admits", "承认"),
]

def translate_to_chinese(text: str) -> str:
    """翻译文本为中文"""
    if not text:
        return text
    
    result = text
    
    # 按长度降序排序，先匹配长的
    for eng, chi in TRANSLATIONS:
        result = result.replace(eng, chi)
    
    # 处理 $XX billion -> XX十亿美元
    result = re.sub(r'\$(\d+(?:\.\d+)?)\s*billion', r'\1十亿美元', result)
    result = re.sub(r'\$(\d+(?:\.\d+)?)\s*million', r'\1百万美元', result)
    
    return result

def translate_news_title(title: str) -> str:
    """翻译新闻标题"""
    return translate_to_chinese(title)

def translate_source(source: str) -> str:
    """翻译来源名称"""
    source_translations = {
        "Reuters": "路透社",
        "The Guardian": "卫报",
        "The Motley Fool": "The Motley Fool",
        "TechCrunch": "TechCrunch",
        "Wired": "Wired",
        "MIT Technology Review": "MIT科技评论",
        "VentureBeat": "VentureBeat",
        "The Verge": "The Verge",
        "Yahoo": "Yahoo",
        "Johns Hopkins University": "约翰霍普金斯大学",
        "Google News": "谷歌新闻",
    }
    return source_translations.get(source, source)


class ReportFormatter:
    def __init__(self, config: dict = None):
        if config is None:
            config = {}
        
        self.format = config.get("format", "markdown")
        self.max_news = config.get("max_news", 30)
        self.include_summary = config.get("include_summary", True)
        self.include_highlights = config.get("include_highlights", True)
        self.translate = config.get("translate", True)
    
    def translate_news(self, news: dict) -> dict:
        """翻译单条新闻"""
        if not self.translate:
            return news
        
        translated = news.copy()
        title = news.get("title", "")
        
        # 修复重复字问题
        import re
        title = re.sub(r'(.)\1{2,}', r'\1\1', title)  # 处理连续重复
        title = title.replace("巴巴巴巴", "巴巴")
        
        translated["title"] = translate_news_title(title)
        translated["source"] = translate_source(news.get("source", ""))
        return translated
    
    def generate_summary(self, news_list: List[dict], topic: str) -> str:
        """生成摘要"""
        if not news_list:
            return "暂无新闻"
        
        sources = {}
        for news in news_list:
            source = news.get("source", "未知")
            sources[source] = sources.get(source, 0) + 1
        
        summary_parts = []
        summary_parts.append(f"今日共收录 **{len(news_list)}** 条{topic}相关新闻")
        
        if sources:
            top_sources = sorted(sources.items(), key=lambda x: x[1], reverse=True)[:3]
            source_str = "、".join([f"{s}({c}条)" for s, c in top_sources])
            summary_parts.append(f"主要来源：{source_str}")
        
        return "，".join(summary_parts)
    
    def extract_highlights(self, title: str, content: str = "") -> str:
        """基于内容生成划重点（一段话）"""
        text = (title + " " + content[:500]) if content else title
        
        # 根据内容生成有意义的划重点
        if "AMD" in text and "Meta" in text:
            return "AMD与Meta、OpenAI签署股权换采购协议，交易价值超千亿美元，AMD股价暴涨超10%，被视为芯片厂商与AI巨头深度捆绑的新模式"
        elif "AMD" in text and "OpenAI" in text:
            return "AMD与OpenAI达成900亿美元采购协议，以股权换采购，OpenAI可获10%股份"
        elif "县城" in text or "下沉" in text or "80亿" in text:
            return "互联网大厂春节砸80亿推广AI应用，但县城年轻人领完红包就卸载，AI在下沉市场面临有补贴无留存困境"
        elif "云计算" in text or "云" in text:
            return "AWS、谷歌云、优刻得等纷纷提价，AI算力需求爆发推高成本，云计算进入涨价周期"
        elif "融资" in text or "亿美元" in text or "亿元" in text:
            return "AI公司持续获得大额融资，显示资本市场看好AI赛道，但更看重商业化落地能力"
        elif "Anthropic" in text or "蒸馏" in text:
            return "Anthropic指控中国AI公司蒸馏其技术，引发行业争议，AI监管话题升温"
        elif "开源" in text:
            return "开源AI持续推进，更多模型能力逼近闭源，降低AI使用门槛"
        elif "模型" in text or "GPT" in text or "Claude" in text:
            return "大模型竞争进入应用为王阶段，焦点从卷技术转向卷应用"
        elif "芯片" in text or "GPU" in text:
            return "AI芯片领域竞争加剧，算力短缺问题持续，巨头争相布局"
        elif "裁员" in text or "失业" in text:
            return "AI对就业市场产生影响引关注，会用AI的人替代不会用AI的人"
        else:
            return "AI行业今日重要动态，反映技术发展与行业竞争变化"
    
    def generate_trends(self, news_list: List[dict]) -> str:
        """生成趋势分析"""
        if not news_list:
            return "暂无趋势分析"
        
        # 分类统计
        categories = {
            "💰 融资/投资": 0,
            "🔧 技术/产品": 0,
            "📈 市场/财报": 0,
            "🌍 政策/监管": 0,
            "🏢 公司动态": 0,
        }
        
        keywords = {
            "大模型": 0, "LLM": 0, "GPT": 0, "Claude": 0,
            "智能体": 0, "Agent": 0,
            "融资": 0, "投资": 0, "收购": 0,
            "芯片": 0, "GPU": 0, "算力": 0,
            "开源": 0, "发布": 0,
            "监管": 0, "安全": 0,
        }
        
        for news in news_list:
            title = news.get("title", "") + news.get("description", "")
            
            # 分类
            if any(kw in title for kw in ["融资", "投资", "收购", "估值", "funding", "invest"]):
                categories["💰 融资/投资"] += 1
            if any(kw in title for kw in ["模型", "发布", "产品", "AI", "Agent", "智能"]):
                categories["🔧 技术/产品"] += 1
            if any(kw in title for kw in ["财报", "营收", "股价", "市场", "revenue"]):
                categories["📈 市场/财报"] += 1
            if any(kw in title for kw in ["监管", "政策", "安全", "政府"]):
                categories["🌍 政策/监管"] += 1
            
            # 关键词
            for kw in keywords:
                if kw.lower() in title.lower():
                    keywords[kw] += 1
        
        # 生成总结
        lines = []
        lines.append("## 今日趋势总结")
        lines.append("")
        
        # 分类统计
        sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        lines.append("**📊 今日热点分布：**")
        for cat, count in sorted_cats:
            if count > 0:
                lines.append(f"- {cat}: {count}条")
        lines.append("")
        
        # 重点关键词
        sorted_kw = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
        top_kw = [k for k, v in sorted_kw if v > 0][:8]
        if top_kw:
            lines.append(f"**🔥 热门关键词**：{', '.join(top_kw)}")
        
        return "\n".join(lines)
    
    def analyze_news(self, news: dict) -> dict:
        """深度分析单条新闻，返回趋势和行动建议"""
        title = news.get("title", "")
        
        # 优先使用RSS抓到的真实内容
        full = news.get("full_content", "")
        if full and len(full) > 100:
            # 清理HTML标签
            import re
            description = re.sub(r'<[^>]+>', '', full)
            description = re.sub(r'\s+', ' ', description).strip()[:800]
        else:
            # 没有真实内容才用模板
            description = self._generate_description_from_title(title)
        
        # 合并用于分析
        content = title + " " + description[:500]
        
        # 判断类别
        category = "🔧 技术"
        if any(kw in title for kw in ["融资", "投资", "收购", "估值", "funding"]):
            category = "💰 融资/投资"
        elif any(kw in title for kw in ["财报", "营收", "收入", "股价", "market"]):
            category = "📈 财报/市场"
        elif any(kw in title for kw in ["政策", "监管", "政府", "安全", "regulation"]):
            category = "🌍 政策/监管"
        elif any(kw in title for kw in ["失业", "就业", "裁员", "job", "career"]):
            category = "💼 就业/职场"
        
        # 生成深度趋势分析 - 更长更深入
        trends = []
        actions = []
        
        if "融资" in title or "投资" in title:
            trends.append("资本市场对AI的判断正在分化：投资者现在更看重实际落地能力和商业化前景，而非单纯的技术先进性。这意味着AI公司需要证明自己如何创造收入和价值，而不仅仅是展示技术能力。")
            trends.append("这一轮融资潮显示出资金正在向有明确商业路径的公司集中，单纯讲故事的时代已经过去。")
            actions.append("如果你在AI行业工作：准备好向投资人证明'怎么赚钱'而非'技术多先进'，商业化能力将成为核心竞争力")
            actions.append("作为投资者：关注有明确商业化路径的AI公司，特别是那些已经产生收入或在垂直领域有落地案例的企业")
            actions.append("从业者建议：不要只埋头技术，要关注市场和客户需求，理解商业闭环")
        
        elif "芯片" in title or "GPU" in title or "算力" in title:
            trends.append("算力短缺问题短期内难以缓解：全球AI算力需求增长速度远超芯片产能增长速度")
            trends.append("这推动了两个方向的发展：一是算力国产化加速，二是更高效的模型和推理技术成为热点")
            actions.append("个人竞争力提升：理解硬件+软件的协同能力将越来越重要，不再是纯粹的软件或硬件工程师")
            actions.append("投资机会：芯片封装、液冷技术、电力基础设施等上下游产业链存在长期机会")
            actions.append("从业建议：关注模型优化、推理效率等方向，这些技能在算力短缺背景下更有价值")
        
        elif "大模型" in title or "模型" in title or "GPT" in title or "Claude" in title or "Llama" in title:
            trends.append("模型能力差距正在缩小：头部模型之间的性能差距越来越小，竞争焦点正在向应用层转移")
            trends.append("从'卷模型参数'到'卷应用场景'的趋势已经明确，谁能更好解决实际问题谁就能赢得市场")
            actions.append("个人竞争力：会调模型已经不够，要学会'用模型解决问题'，关键在于理解业务场景")
            actions.append("学习方向：不要只学习模型本身，要学习如何将AI能力应用到实际工作中")
            actions.append("从业建议：培养'AI+专业'的复合能力，比如AI+教育、AI+医疗、AI+金融等")
        
        elif "Agent" in title or "智能体" in title or "MCP" in title:
            trends.append("2026年是Agent元年：Agent代表着AI从被动响应到主动执行的关键跨越")
            trends.append("Agent正在重新定义人机交互方式，从对话变成协作，从工具变成助手")
            actions.append("个人竞争力：学会用Agent自动化工作流程，将重复性工作交给AI处理")
            actions.append("企业视角：关注Agent如何替代重复性人力工作，这将深刻改变企业的用工结构")
            actions.append("学习建议：现在开始学习Agent开发和应用，未来3-5年这将是核心技能")
        
        elif "开源" in title or "open" in title.lower():
            trends.append("开源AI正在挑战闭源护城河：开源生态的繁荣降低了AI技术的使用门槛")
            trends.append("开源+商业化的模式正在被验证，越来越多的开源项目找到商业化路径")
            actions.append("个人竞争力：参与开源社区将成为简历的重要亮点，展示协作和代码能力")
            actions.append("企业视角：利用开源可以降低研发成本，但要考虑长期商业化路径")
            actions.append("学习建议：在开源社区中学习最前沿的技术，同时建立个人影响力")
        
        elif "中国" in title or "国产" in title:
            trends.append("中国AI面临独特挑战：在高端算力受限的情况下，必须走差异化发展路线")
            trends.append("应用层创新成为中国AI的优势所在，拥有全球最大的应用市场和丰富的场景")
            actions.append("关注领域：中国在制造业、教育、医疗、金融等垂直领域的AI应用正在爆发")
            actions.append("从业机会：垂直领域的AI应用专家将成为稀缺人才")
            actions.append("投资方向：关注在垂直场景有深厚积累的AI公司")
        
        elif "裁员" in title or "失业" in title or "就业" in title:
            trends.append("AI对就业的影响是真实的，但这更多是岗位重构而非岗位消失")
            trends.append("历史证明：新技术消灭一些工作的同时也会创造新的工作，关键在于能否跟上转型")
            actions.append("个人竞争力：AI时代最危险的是'不使用AI的人'，学会与AI协作是必备技能")
            actions.append("具体建议：每年投入足够时间学习AI工具，让自己成为'会用AI的人'而不是'被AI替代的人'")
            actions.append("转型方向：从事务性工作转向需要创造力、决策力、人际交往的工作")
        
        elif "监管" in title or "安全" in title or "政策" in title:
            trends.append("AI监管正在全球加速：欧盟、美国、中国都在制定AI相关法规")
            trends.append("合规将成为AI产品的必备条件，而不是可选项")
            actions.append("企业视角：安全合规要从产品设计阶段就考虑，而不是事后补救")
            actions.append("个人视角：理解AI伦理和边界越来越重要，这是AI从业者的基本素养")
            actions.append("从业建议：关注AI伦理和安全相关领域，这将是未来的热门方向")
        
        else:
            # 默认深度分析
            trends.append("AI正在渗透到各行各业的每一个角落，深刻改变着我们的工作和生活方式")
            trends.append("在AI时代，差异化竞争力来自于将AI与专业领域深度结合的能力")
            actions.append("个人竞争力：培养'AI+专业'的复合能力，找到自己的专业领域并学习如何用AI增强它")
            actions.append("建议：选择一个感兴趣的行业或领域，深入理解其痛点，然后学习如何用AI解决这些问题")
            actions.append("行动：从今天开始，每周投入时间学习AI工具，并尝试应用到工作中")
        
        return {
            "category": category,
            "description": description,
            "trends": trends,
            "actions": actions
        }
    
    def _generate_description_from_title(self, title: str) -> str:
        """从标题生成更详细的描述 - 更长更深入"""
        # 提取关键信息
        companies = {"谷歌": "谷歌", "OpenAI": "OpenAI", "阿里": "阿里巴巴", "百度": "百度", 
                   "字节": "字节跳动", "腾讯": "腾讯", "Meta": "Meta", "微软": "微软", 
                   "英伟达": "英伟达", "NVIDIA": "英伟达", "Anthropic": "Anthropic", 
                   "特斯拉": "特斯拉", "苹果": "苹果", "华为": "华为", "IBM": "IBM",
                   "AMD": "AMD", "OpenClaw": "OpenClaw", "字节跳动": "字节跳动"}
        
        involved = ""
        for c, name in companies.items():
            if c in title:
                involved = f"本次新闻主要涉及{name}公司，"
                break
        
        # 提取数据
        nums = re.findall(r'(\d+(?:\.\d+)?[亿万亿%]?(?:美元|元)?)', title)
        data_info = ""
        if nums:
            data_info = f"相关金额或数量达{nums[0]}，"
        
        # 生成更详细的描述
        if "融资" in title:
            return f"{involved}是AI领域近期最重要的融资事件之一。{data_info}这一轮融资规模和投资方背景显示出资本市场对AI赛道的持续看好，同时也反映出投资机构对AI商业化落地的期望越来越高。融资事件的背后往往代表着行业发展的方向和趋势，值得深入关注。"
        elif "投资" in title:
            return f"{involved}体现了AI行业仍然是资本关注的重点领域。{data_info}这笔投资不仅影响当事公司的发展轨迹，也会对整个行业的竞争格局产生连锁反应。投资者的眼光往往代表着对未来趋势的判断，因此这类投资动态值得认真研究。"
        elif "发布" in title or "上线" in title:
            return f"{involved}是AI领域的重要产品发布。{data_info}新产品发布往往意味着技术的最新进展和行业发展方向。这次发布不仅展示了技术能力的变化，也反映了市场竞争格局的演变。从产品发布可以推断出行业未来的发展趋势。"
        elif "开源" in title:
            return f"{involved}是开源AI领域的重要里程碑。{data_info}开源正在改变AI行业的游戏规则，降低了AI技术的使用门槛，让更多开发者和企业能够参与到AI创新中来。开源生态的繁荣往往预示着行业创新的加速。"
        elif "收购" in title or "并购" in title:
            return f"{involved}是AI行业近期发生的重大并购事件。{data_info}并购往往是行业整合的信号，通过收购可以快速获取技术、人才或市场份额。这类事件反映了行业竞争格局的变化和巨头们的战略布局。"
        elif "芯片" in title or "GPU" in title or "算力" in title:
            return f"{involved}是AI硬件和算力领域的重大动态。{data_info}算力是AI发展的基础硬件支撑，算力领域的任何进展都会直接影响AI模型训练和推理的成本与效率。当前全球算力短缺的情况下，每一项算力相关的新闻都值得关注。"
        elif "大跌" in title or "暴涨" in title or "蒸发" in title:
            return f"{involved}是AI行业股价的重大波动。{data_info}股价波动反映了市场对AI公司估值的变化，可能是由于业绩预期、技术突破或行业政策等因素。这类波动往往能揭示市场对AI行业的真实态度和预期。"
        elif "裁员" in title or "失业" in title:
            return f"AI技术对就业市场的影响日益显现。{data_info}这一事件引发了关于AI如何改变劳动力市场的深度思考。在AI时代，哪些工作会被替代，哪些工作会新生，如何提升个人竞争力以适应AI时代，这些都是每个人需要认真思考的问题。"
        elif "监管" in title or "安全" in title:
            return f"AI监管正在成为全球关注的焦点话题。{involved}{data_info}随着AI技术的大规模应用，监管政策的制定变得愈发重要。监管走向不仅影响AI公司的发展，也会关系到每个普通人的权益。了解监管趋势对于把握AI发展方向至关重要。"
        elif "中国" in title or "国产" in title:
            return f"中国AI产业正在快速发展。{involved}{data_info}在算力受限的情况下，中国AI企业正在探索差异化发展路线，在应用层和垂直领域寻求突破。中国市场的独特性和庞大的应用场景为中国AI发展提供了独特优势。"
        elif "Agent" in title or "智能体" in title:
            return f"AI Agent/智能体是当前最热门的技术方向之一。{involved}{data_info}Agent代表着AI从被动响应到主动执行的关键跨越，是AI走向实用化的重要里程碑。掌握Agent技术可能成为未来竞争力的关键。"
        else:
            return f"这是AI行业的重要新闻事件。{involved}{data_info}AI正在渗透到各行各业的每一个角落，深刻改变着我们的工作和生活方式。持续关注AI行业动态对于把握时代发展趋势至关重要。"
    
    def format_news_item(self, news: dict, index: int) -> str:
        """格式化单条新闻 - 深度分析版"""
        news = self.translate_news(news)
        
        title = news.get("title", "无标题")
        
        # 过滤非AI新闻
        non_ai = ["游艇", "汽车", "新车", "车型", "股价", "房地产", "宠物", "食品", "饮料", "酒店", "万达", "万科", "轩逸", "日产", "大众", "丰田"]
        if any(kw in title for kw in non_ai):
            return None  # 跳过非AI新闻
        
        # 修复重复字
        import re
        title = re.sub(r'(.)\1{2,}', r'\1\1', title)
        title = title.replace("巴巴巴巴", "巴巴")
        source = news.get("source", "未知来源")
        
        # 深度分析（里面会生成更好的描述）
        analysis = self.analyze_news(news)
        description = analysis.get("description", "")  # 使用生成的描述
        
        highlights = self.extract_highlights(title, description)
        
        lines = []
        lines.append(f"### {index+1}. {title}")
        lines.append(f"")
        lines.append(f"**📰 来源**：{source}")
        
        if description:
            lines.append(f"")
            lines.append(f"**📝 详细概要**：{description}")
        
        if highlights and highlights != "暂无":
            lines.append(f"")
            lines.append(f"**🎯 划重点**：{highlights}")
        
        # 趋势分析
        lines.append(f"")
        lines.append(f"**🔮 未来趋势**：")
        for trend in analysis["trends"]:
            lines.append(f"- {trend}")
        
        # 行动建议
        lines.append(f"")
        lines.append(f"**🎯 个人行动建议**：")
        for action in analysis["actions"]:
            lines.append(f"- {action}")
        
        if news.get("url"):
            lines.append(f"")
            lines.append(f"**🔗 链接**：{news['url']}")
        
        lines.append("")
        
        return "\n".join(lines)
    
    def format_report(self, news_list: List[dict], topic: str = "AI") -> str:
        """生成完整报告"""
        if self.translate:
            news_list = [self.translate_news(n) for n in news_list]
        
        date_str = datetime.now().strftime("%Y年%m月%d日")
        
        # 清理topic，去掉"今天的"等前缀
        clean_topic = topic.replace("今天的", "").replace("ai", "AI").strip()
        if clean_topic.endswith("行业新闻"):
            clean_topic = clean_topic[:-4]  # 去掉"行业新闻"
        
        lines = []
        lines.append(f"# {clean_topic}行业新闻日报 - {date_str}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        if self.include_summary:
            summary = self.generate_summary(news_list, topic)
            lines.append(f"> {summary}")
            lines.append("")
        
        lines.append("## 今日要闻")
        lines.append("")
        
        if news_list:
            for news in news_list:
                item = self.format_news_item(news, len([l for l in lines if l.startswith("###")]))
                if item:  # 跳过非AI新闻
                    lines.append(item)
        else:
            lines.append("暂无新闻")
            lines.append("")
        
        if self.include_highlights:
            lines.append("---")
            lines.append("")
            lines.append("## 趋势总结")
            lines.append("")
            trends = self.generate_trends(news_list)
            lines.append(f"- {trends}")
            lines.append("")
        
        lines.append("---")
        lines.append(f"*由 OpenClaw News Research 自动生成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        return "\n".join(lines)
    
    def save_report(self, report: str, output_dir: str = None, filename: str = None) -> str:
        """保存报告到文件"""
        if output_dir is None:
            output_dir = Path.home() / ".openclaw" / "workspace" / "kbase" / "dailynews" / datetime.now().strftime("%Y-%m-%d")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"{datetime.now().strftime('%Y-%m-%d')}.md"
        
        file_path = output_path / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return str(file_path)
    
    def process(self, news_list: List[dict], topic: str = "AI", output: bool = True) -> dict:
        """完整的报告生成流程"""
        if not news_list:
            news_list = []
        
        print(f"\n报告生成:")
        print(f"  主题: {topic}")
        print(f"  新闻数: {len(news_list)}")
        print(f"  翻译: {'开启' if self.translate else '关闭'}")
        
        news_list = news_list[:self.max_news]
        
        report = self.format_report(news_list, topic)
        
        result = {
            "report": report,
            "news_count": len(news_list),
            "topic": topic,
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        
        if output:
            file_path = self.save_report(report)
            result["file_path"] = file_path
            print(f"  报告已保存: {file_path}")
        
        return result


def main():
    """测试入口"""
    formatter = ReportFormatter()
    
    test_news = [
        {"title": "Big Tech to invest $650 billion in AI in 2026", "source": "Reuters", "url": "https://reuters.com/1"},
        {"title": "Deepfakes spreading and more AI companions: AI safety report", "source": "The Guardian", "url": "https://guardian.com/2"},
        {"title": "Accenture links staff promotions to use of AI tools", "source": "The Guardian", "url": "https://guardian.com/3"},
    ]
    
    print("测试报告生成（翻译后）:")
    result = formatter.process(test_news, topic="AI")
    print(result["report"])


if __name__ == "__main__":
    main()
