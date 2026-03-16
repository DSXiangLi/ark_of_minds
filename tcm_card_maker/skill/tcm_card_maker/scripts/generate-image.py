#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中医方剂卡片图像生成脚本 (Nano Banana Pro API)
使用Google原生格式API，支持4K分辨率和多种纵横比
"""

import os
import sys
import json
import requests
import base64
from jinja2 import Template
from dotenv import load_dotenv

def load_config():
    """加载环境配置"""
    # 从技能目录的.env文件加载
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(skill_dir, '.env')
    load_dotenv(env_path)
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("缺少API配置，请检查.env文件中的GEMINI_API_KEY")
    
    # 使用Google原生格式的API端点
    google_api_url = "https://api.laozhang.ai/v1beta/models/gemini-3-pro-image-preview:generateContent"
    
    return google_api_url, api_key

def load_template():
    """加载Jinja模板"""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(skill_dir, 'assets', 'image-prompt.j2')
    
    with open(template_path, 'r', encoding='utf-8') as f:
        return Template(f.read())

def render_prompt(json_data):
    """使用模板渲染完整的绘图指令"""
    template = load_template()
    base_prompt = template.render(**json_data)
    
    # 优化提示，使其更适合图像生成
    enhanced_prompt = f"""请生成一张中医方剂卡片图像：{json_data.get('formula_name', '')}

{base_prompt}

图像要求：
1. 整体风格：中式美学，水墨元素，传统中医风格
2. 布局：三列并排，用中医元素的云纹图案分割
3. 色彩：柔和自然，符合中医文化
4. 文字：所有文字清晰可读
5. 图像质量：药物手绘准确，场景生动
6. 专业准确：符合中医理论

请生成高质量的中医方剂卡片图像。"""
    
    return enhanced_prompt

def call_nano_banana_pro_api(api_url, api_key, prompt, aspect_ratio="16:9", image_size="2K"):
    """调用Nano Banana Pro API (Google原生格式)"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": aspect_ratio,
                "imageSize": image_size
            }
        }
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=180)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API调用失败: {str(e)}")
    except json.JSONDecodeError as e:
        raise Exception(f"API响应解析失败: {str(e)}")

def save_image_from_response(result, formula_name):
    """从API响应中保存图像"""
    try:
        # 解析Google原生格式的响应
        if "candidates" in result and len(result["candidates"]) > 0:
            candidate = result["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"] and len(candidate["content"]["parts"]) > 0:
                part = candidate["content"]["parts"][0]
                
                if "inlineData" in part and "data" in part["inlineData"]:
                    image_data_base64 = part["inlineData"]["data"]
                    
                    # 解码base64
                    image_data = base64.b64decode(image_data_base64)
                    
                    # 生成文件名
                    safe_name = "".join(c for c in formula_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    output_file = f"{safe_name}_中医方剂卡片.png"
                    
                    with open(output_file, 'wb') as f:
                        f.write(image_data)
                    
                    return output_file, len(image_data)
                    
    except Exception as e:
        raise Exception(f"解析响应时出错: {str(e)}")
    
    raise Exception("响应中没有找到有效的图像数据")

def save_prompt_text(prompt, formula_name):
    """保存提示文本"""
    safe_name = "".join(c for c in formula_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    output_file = f"{safe_name}_图像提示.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    return output_file

def test_configuration():
    """测试配置是否正常"""
    try:
        api_url, api_key = load_config()
        print("✓ 配置加载成功")
        print(f"  API端点: {api_url}")
        api_key_status = '已配置' if api_key and api_key != '请在此处填写您的Gemini_API密钥' else '未配置或为默认值'
        print(f"  API密钥: {api_key_status}")
        return True
    except Exception as e:
        print(f"✗ 配置加载失败: {str(e)}")
        return False

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python generate-image-new.py <JSON文件> [纵横比] [分辨率]")
        print("       python generate-image-new.py --test-config")
        print("示例: python generate-image-new.py 理中丸.json")
        print("       python generate-image-new.py 理中丸.json 16:9 2K")
        print("       python generate-image-new.py --test-config")
        print("\n纵横比选项: 1:1, 16:9, 9:16, 4:3, 3:4, 21:9, 3:2, 2:3, 5:4, 4:5")
        print("分辨率选项: 1K, 2K, 4K")
        print("默认值: 16:9 (宽屏), 2K (高质量)")
        sys.exit(1)
    
    # 检查是否测试配置
    if sys.argv[1] == "--test-config":
        print("测试配置...")
        if test_configuration():
            print("✓ 配置测试通过")
            sys.exit(0)
        else:
            print("✗ 配置测试失败")
            sys.exit(1)
    
    json_file = sys.argv[1]
    aspect_ratio = sys.argv[2] if len(sys.argv) > 2 else "16:9"
    image_size = sys.argv[3] if len(sys.argv) > 3 else "2K"
    
    try:
        # 加载JSON数据
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        formula_name = data.get('formula_name', '未知方剂')
        print(f"正在为 {formula_name} 生成图像...")
        
        # 加载配置
        api_url, api_key = load_config()
        print("✓ 配置加载成功")
        
        # 渲染完整prompt
        prompt = render_prompt(data)
        print("✓ 绘图指令生成成功")
        
        # 保存提示文本
        prompt_file = save_prompt_text(prompt, formula_name)
        print(f"✓ 提示保存到: {prompt_file}")
        
        # 调用API
        print(f"正在调用Nano Banana Pro API...")
        print(f"  纵横比: {aspect_ratio}")
        print(f"  分辨率: {image_size}")
        print("  注意: 这可能会消耗API额度 ($0.05/张)")
        
        result = call_nano_banana_pro_api(api_url, api_key, prompt, aspect_ratio, image_size)
        
        # 保存生成的图像
        image_file, image_size_bytes = save_image_from_response(result, formula_name)
        file_size_kb = image_size_bytes / 1024
        
        print(f"✓ 图像生成成功!")
        print(f"  保存到: {image_file}")
        print(f"  文件大小: {file_size_kb:.1f} KB")
        
        # 生成报告
        report = f"""中医方剂卡片图像生成成功！

方剂: {formula_name}
生成时间: 2026-03-14 10:10 GMT+8

生成详情:
- 模型: Nano Banana Pro (Gemini 3 Pro Image Preview)
- 纵横比: {aspect_ratio}
- 分辨率: {image_size}
- 提示长度: {len(prompt)} 字符

生成文件:
1. {image_file} - 中医方剂卡片图像
2. {prompt_file} - 图像生成提示

使用说明:
1. 查看生成的图像: 打开 {image_file}
2. 如需修改: 编辑 {prompt_file} 后重新运行
3. 分享: 可将图像用于中医教育、学习资料等

恭喜！中医方剂卡片图像已成功生成！"""
        
        report_file = f"{formula_name}_生成报告.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✓ 报告保存到: {report_file}")
        
        # 显示提示预览
        print("\n图像生成提示预览:")
        print("=" * 60)
        print(prompt[:300] + "...")
        print("=" * 60)
        
        print(f"\n🎉 图像生成完成！")
        print(f"✅ 图像文件: {image_file}")
        print(f"📝 提示文件: {prompt_file}")
        print(f"📊 报告文件: {report_file}")
            
    except FileNotFoundError as e:
        print(f"❌ 文件未找到: {str(e)}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析失败: {str(e)}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ 配置错误: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()