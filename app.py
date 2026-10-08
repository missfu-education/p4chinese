import streamlit as st
from openai import OpenAI
import base64

# 1. 網頁頁面標題與佈局設定
st.set_page_config(page_title="小四中文寫作 AI 評改助手", page_icon="✏️", layout="centered")

st.title("✏️ 小四中文寫作 AI 評改助手")
st.caption("記敍文《我拯救了________（一種動物）》專用評改系統（香港適用版）")

# 2. 側邊欄設定：輸入 OpenRouter API Key
st.sidebar.header("⚙️ 系統設定")
api_key = st.sidebar.text_input("請輸入 OpenRouter API Key", type="password")

# 3. 主介面：相片上傳區
st.markdown("### 📸 拍照 / 上傳學生作文相片")
uploaded_file = st.file_uploader("請確保相片字跡清晰、光線充足：", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 預覽上傳的相片
    st.image(uploaded_file, caption="已上傳的作文相片", use_container_width=True)
    
    # 開始評改按鈕
    if st.button("🚀 開始評改作文", type="primary"):
        if not api_key:
            st.error("⚠️ 請先在左側邊欄輸入你的 OpenRouter API Key！")
        else:
            with st.spinner("AI 老師正在認真批閱作文中，請稍候..."):
                try:
                    # 將相片轉為 Base64 格式
                    bytes_data = uploaded_file.getvalue()
                    base64_image = base64.b64encode(bytes_data).decode('utf-8')

                    # 初始化 OpenRouter 用戶端 (香港順暢連線)
                    client = OpenAI(
                        base_url="https://openrouter.ai/api/v1",
                        api_key=api_key,
                    )

                    # 評語系統 Prompt (包含香港評分標準)
                    system_prompt = """
你是一位經驗豐富、眼光獨到且語氣嚴厲但有耐心的香港小學四年級中文科老師。
請根據《我拯救了______（一種動物）》評分表評改學生作文。

【評改要求與原則】
1. 使用繁體中文，語言直截了當，讓小四學生完全理解。
2. 評語風格【尖銳、直擊痛點】，指出好處點到即止，指摘缺點一針見血。
3. 必須輸出詳細細項得分。

【評分細則（總分100分）】
- 內容（29分）：一等(0-7)、二等(8-14)、三等(15-21)、四等(22-29)
- 重點一（起承轉合佈局）：下等(0-1)、中等(2-3)、上等(4-5)
- 重點二（人物神情描寫）：下等(0-1)、中等(2-3)、上等(4-5)
- 重點三（人物動作描寫）：下等(0-1)、中等(2-3)、上等(4-5)
- 結構（16分）：一等(0-4)、二等(5-8)、三等(9-12)、四等(13-16)
- 文句（16分）：一等(0-4)、二等(5-8)、三等(9-12)、四等(13-16)
- 詞語運用（16分）：一等(0-4)、二等(5-8)、三等(9-12)、四等(13-16)
- 錯別字及標點符號（8分）：錯別字最高4分、標點最高4分

【請嚴格按以下 Markdown 格式輸出結果】：

### 📝 作文評改報告

#### 【一、 總體成績單】
**總分： [X] / 100 分**

| 評核項目 | 滿分 | 學生得分 | 等級 |
| :--- | :--- | :--- | :--- |
| 1. 內容 (故事細節與主題) | 29 分 | [X] 分 | [等級] |
| 2. 重點一: 起承轉合 | 5 分 | [X] 分 | [等級] |
| 3. 重點二: 人物神情描寫 | 5 分 | [X] 分 | [等級] |
| 4. 重點三: 人物動作描寫 | 5 分 | [X] 分 | [等級] |
| 5. 結構 (分段與條理) | 16 分 | [X] 分 | [等級] |
| 6. 文句 (通順與修辭) | 16 分 | [X] 分 | [等級] |
| 7. 詞語運用 (書面語/詞彙) | 16 分 | [X] 分 | [等級] |
| 8. 錯別字及標點符號 | 8 分 | [X] 分 | [等級] |

#### 【二、 亮點（好的地方）】
* [簡潔肯定1個做得好的地方]

#### 【三、 致命傷（最需要改進的地方）】
* [尖銳指出最嚴重的問題，直擊痛點！]

#### 【四、 答問式思考（引導你自己提升）】
1. [問題 1？]
2. [問題 2？]

#### 【五、 謄文/重寫指示】
🎯 **最需要重寫的段落**：[明確指出第 X 段]  
💡 **重寫建議**：[具體的改寫指引與詞語建議]
"""

                    # 呼叫 Gemini 1.5 Flash 圖像模型
                    # 呼叫 OpenRouter 免費圖像模型
                    response = client.chat.completions.create(
                        model="google/gemini-2.0-flash-exp:free",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "請根據評分標準評改這篇作文圖片："},
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                                    }
                                ]
                            }
                        ]
                    )

                    # 呈現評改結果
                    st.markdown(response.choices[0].message.content)

                except Exception as e:
                    st.error(f"評改失敗：{str(e)}")
                                ]
                            }
                        ]
                    )

                    # 呈現評改結果
                    st.markdown(response.choices[0].message.content)

                except Exception as e:
                    st.error(f"評改失敗：{str(e)}")
