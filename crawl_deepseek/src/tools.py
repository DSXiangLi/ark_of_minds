import json
import os
import logging
from pathlib import Path
from typing import Any, Union

from browser_use import ActionResult, Tools, BrowserSession

logger = logging.getLogger(__name__)

tools = Tools()


def sanitize_filename(query: str) -> str:
    invalid_chars = '<>:"/\\|?*'
    filename = query
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    filename = filename.replace("\n", " ").replace("\r", "").strip()
    filename = filename[:100].rstrip(".")
    return filename if filename else "query"


@tools.action("Save DeepSeek response to JSON file")
async def save_deepseek_result(browser_session: BrowserSession, query: str) -> ActionResult:
    """提取DeepSeek回答和引用并保存为JSON"""
    try:
        page = await browser_session.get_current_page()
        if not page:
            return ActionResult(extracted_content="ERROR: No page", success=False)

        import asyncio

        # 等待并检查"本回答由 AI 生成"是否出现
        max_wait = 20  # 最多等待20秒
        wait_interval = 2  # 每2秒检查一次
        completion_found = False

        for i in range(max_wait // wait_interval):
            await asyncio.sleep(wait_interval)

            # 检查页面是否包含完成标志
            body_text = await page.evaluate("() => document.body.innerText")
            if "本回答由 AI 生成" in body_text or "内容由 AI 生成" in body_text:
                completion_found = True
                break

            # 也检查是否有加载中的标志消失
            if "深度思考" in body_text and "已思考" not in body_text:
                # 还在思考中，继续等待
                continue

        if not completion_found:
            # 如果没有明确完成标志，再等待2秒确保内容加载完成
            await asyncio.sleep(2)

        # 提取内容
        js_code = """(query) => {
    var result = {answer: '', references: []};
    
    var bodyText = document.body.innerText || '';
    
    // 优先使用"本回答由 AI 生成"作为完成标志（这是最终完成标志）
    var completionMarker = '本回答由 AI 生成';
    var altMarker = '内容由 AI 生成';
    
    // 查找最终完成标志的位置
    var markerIdx = bodyText.lastIndexOf(completionMarker);
    if (markerIdx < 0) {
        markerIdx = bodyText.lastIndexOf(altMarker);
    }
    
    // 如果找到了完成标志，从开始到标志位置提取
    if (markerIdx >= 0) {
        result.answer = bodyText.substring(0, markerIdx + completionMarker.length);
    } else {
        // 兜底：查找用户问题之后的所有内容
        var qIdx = bodyText.lastIndexOf(query);
        if (qIdx >= 0) {
            result.answer = bodyText.substring(qIdx);
        } else {
            result.answer = bodyText;
        }
    }
    
    // 清理回答内容
    // 1. 去除"开启新对话"
    var newChatIdx = result.answer.indexOf('开启新对话');
    if (newChatIdx > 0) {
        result.answer = result.answer.substring(0, newChatIdx);
    }
    
    // 2. 确保从用户问题开始
    var queryStart = result.answer.lastIndexOf(query);
    if (queryStart >= 0) {
        result.answer = result.answer.substring(queryStart);
    }
    
    // 提取引用 - 基于页面中显示的引用数量
    // 1. 解析"已阅读 X 个网页"获取期望的引用数量
    var refCountMatch = bodyText.match(/已阅读[\\s]*(\\d+)[\\s]*个网页/);
    var expectedRefCount = refCountMatch ? parseInt(refCountMatch[1]) : 10;
    
    // 2. 收集所有外部链接
    var refLinks = [];
    var allLinks = document.querySelectorAll('a[href]');
    
    allLinks.forEach(function(link) {
        try {
            var href = link.href;
            var text = (link.innerText || '').trim();
            
            if (!href || href.indexOf('http') !== 0) return;
            if (href.indexOf('deepseek.com') >= 0) return;
            if (href.indexOf('chat.deepseek') >= 0) return;
            
            var cleanTitle = text.replace(/^[\\s\\d\\-\\.\\[\]]+/, '').trim();
            if (!cleanTitle || cleanTitle.length < 2) {
                try { 
                    cleanTitle = new URL(href).hostname.replace('www.', ''); 
                } catch(e) { 
                    cleanTitle = 'Reference'; 
                }
            }
            
            refLinks.push({
                title: cleanTitle.substring(0, 100), 
                url: href
            });
        } catch(e) {}
    });
    
    // 3. 去重
    var seen = {};
    var uniqueRefs = [];
    refLinks.forEach(function(r) {
        if (!seen[r.url]) {
            seen[r.url] = true;
            uniqueRefs.push(r);
        }
    });
    
    // 4. 返回期望数量的引用
    result.references = uniqueRefs.slice(0, Math.max(expectedRefCount, uniqueRefs.length));
    
    return JSON.stringify(result);
}"""

        result_str = await page.evaluate(js_code, query)

        try:
            data = (
                json.loads(result_str)
                if isinstance(result_str, str)
                else {"answer": str(result_str), "references": []}
            )
        except:
            data = {"answer": result_str, "references": []}

        answer = (data.get("answer") or "")[:1500]
        references = data.get("references", [])[:20]

        logger.info(f"Extracted: answer_len={len(answer)}, refs={len(references)}")

        filename = sanitize_filename(query) + ".json"
        filepath = Path(".") / filename

        result = {"answer": answer, "references": references}

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved to {filepath}")

        return ActionResult(
            extracted_content=f"Saved to {filename} - answer length: {len(answer)}, references: {len(references)}",
            is_done=True,
        )

    except Exception as e:
        return ActionResult(extracted_content=f"ERROR: {str(e)}", error=str(e), success=False)
