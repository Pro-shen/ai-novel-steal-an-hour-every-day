#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《每天偷一小时》自动写作助手
用于定时任务自动创作小说章节
"""

import json
import os
from datetime import datetime

# 文件路径
BASE_DIR = "/app/working/workspaces/default/novels/每天偷一小时"
PROGRESS_FILE = os.path.join(BASE_DIR, "写作进度.json")
OUTLINE_FILE = os.path.join(BASE_DIR, "完整大纲.md")
MEMORY_FILE = "/app/working/workspaces/default/MEMORY.md"

def load_progress():
    """加载写作进度"""
    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_progress(progress):
    """保存写作进度"""
    progress['last_updated'] = datetime.now().strftime("%Y-%m-%d")
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def get_next_chapter_info(progress):
    """获取下一章信息"""
    current = progress['current_chapter']
    chapter_key = str(current)
    
    # 从进度中获取章节信息
    if chapter_key in progress.get('chapters_status', {}):
        chapter_data = progress['chapters_status'][chapter_key]
        return {
            'chapter': current,
            'title': chapter_data.get('title', '未知'),
            'status': chapter_data.get('status', 'pending'),
            'file': chapter_data.get('file', f'第{current}章.md')
        }
    
    # 从 next_chapter_info 获取
    if 'next_chapter_info' in progress:
        return progress['next_chapter_info']
    
    return None

def mark_chapter_completed(progress, chapter_num, word_count):
    """标记章节完成"""
    chapter_key = str(chapter_num)
    
    if 'chapters_status' not in progress:
        progress['chapters_status'] = {}
    
    progress['chapters_status'][chapter_key] = {
        'title': progress.get('next_chapter_info', {}).get('title', '未知'),
        'status': 'completed',
        'word_count': word_count,
        'file': f'第{chapter_key}章.md',
        'completed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 更新已完成章节数
    progress['completed_chapters'] = chapter_num
    
    # 准备下一章信息
    next_chapter = chapter_num + 1
    progress['current_chapter'] = next_chapter
    
    # 更新下一章信息（需要根据大纲填充）
    progress['next_chapter_info'] = {
        'chapter': next_chapter,
        'title': f'第{next_chapter}章',
        'status': 'pending'
    }
    
    return progress

def get_chapter_outline(chapter_num):
    """从大纲中获取章节概要"""
    # 这里应该解析完整大纲.md 文件
    # 简化版本：返回基本信息
    volume = "第一卷：觉醒"
    if chapter_num > 50:
        volume = "第二卷：入局"
    if chapter_num > 100:
        volume = "第三卷：深入"
    if chapter_num > 150:
        volume = "第四卷：真相"
    if chapter_num > 200:
        volume = "第五卷：对抗"
    if chapter_num > 250:
        volume = "第六卷：决战"
    
    return {
        'volume': volume,
        'chapter': chapter_num,
        'note': '请参考完整大纲.md 和 MEMORY.md 获取详细章节信息'
    }

def main():
    """主函数"""
    print(f"=== 《每天偷一小时》自动写作助手 ===")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 加载进度
    progress = load_progress()
    print(f"当前进度：已完成 {progress['completed_chapters']}/{progress['total_chapters']} 章")
    print(f"即将创作：第 {progress['current_chapter']} 章")
    print()
    
    # 获取下一章信息
    next_chapter = get_next_chapter_info(progress)
    if next_chapter:
        print(f"章节标题：{next_chapter.get('title', '未知')}")
        print(f"所在卷数：{next_chapter.get('volume', '未知')}")
        print(f"主要人物：{next_chapter.get('main_characters', [])}")
        print(f"核心事件：{next_chapter.get('core_event', '未知')}")
        print(f"悬念钩子：{next_chapter.get('suspense', '未知')}")
        print()
    
    print("请 AI 根据以下要求创作：")
    print("1. 读取 MEMORY.md 中的完整大纲")
    print("2. 根据上述章节信息创作")
    print("3. 字数要求：5000 字以上")
    print("4. 保存文件到对应章节")
    print("5. 更新写作进度.json")
    print()
    
    # 输出创作提示
    chapter_num = progress['current_chapter']
    outline = get_chapter_outline(chapter_num)
    
    print("=" * 60)
    print("创作提示：")
    print("=" * 60)
    print(f"请写《每天偷一小时》第{chapter_num}章")
    print(f"卷数：{outline['volume']}")
    print(f"标题：{next_chapter.get('title', '未知') if next_chapter else '未知'}")
    print()
    print("写作要点（5000 字分配）：")
    print("- 场景描写：1000 字（环境、氛围、细节）")
    print("- 对话扩展：1500 字（人物交流、心理活动）")
    print("- 动作戏：1500 字（战斗、追逐、紧张场面）")
    print("- 情感线：500 字（人物关系、内心挣扎）")
    print("- 悬念设置：500 字（章末钩子，吸引读者）")
    print("=" * 60)

if __name__ == "__main__":
    main()
