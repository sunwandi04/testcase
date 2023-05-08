import streamlit as st
import openai
import re
from datetime import datetime
from streamlit.components.v1 import html
from streamlit_lottie import st_lottie
from utils import load_lottie_url
import pandas as pd
import csv

pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)

# 设置OpenAI API密钥
openai.api_key = "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"
# 设置 prompt
prompt_user_story = f"I want you to act as a software project manager responsible for generate acceptance criteria that can be used to validate that the software meets the functional requirements specified in the user stories." \
                    "\nThe acceptance criteria should be specific, measurable, achievable, relevant, and time-bound. " \
                    "\nAdditionally, you should ensure that the acceptance criteria cover all possible scenarios and edge cases." \
                    "\nBy defining clear and comprehensive acceptance criteria, you can help ensure that the software meets the necessary standards and that the user's needs have been fulfilled." \
                    "\nWrite at least 10 professional and detailed acceptance criteria about the topic below in the described format. Make your best effort." \
                    "\nOnly Answer in Chinese. Do not return anything other than acceptance criteria content. Do not wrap responses in quotes."
prompt_test_case = f"您是软件测试和软件质量保证方面的专家,专门从事功能测试,您帮助我之前的许多人生成了满足特定要求的功能测试用例。" \
                   "\n您生成的测试用例能涵盖正常场景、异常场景、边界场景。" \
                   "\n您生成的测试用例优先级包括 P0、P1、P2，P0为最高优先级，P2代表最低优先级" \
                   "\n以所述测试用例格式编写至少5个关于以下主题的专业和详细测试用例。尽你最大的努力。" \
                   "\n测试用例格式：" \
                   "\n1." \
                   "\n-用例名称<用例名称>" \
                   "\n-用例类型<功能测试>" \
                   "\n-优先级<优先级>" \
                   "\n-前置条件<前置条件>" \
                   "\n-步骤描述<步骤描述>" \
                   "\n-预期结果<预期结果>" \
                   "\n2." \
                   "\n-用例名称<用例名称>" \
                   "\n-用例类型<功能测试>" \
                   "\n-优先级<优先级>" \
                   "\n-前置条件<前置条件>" \
                   "\n-步骤描述<步骤描述>" \
                   "\n-预期结果<预期结果>" \
                   "\n3." \
                   "\n-用例名称<用例名称>" \
                   "\n-用例类型<功能测试>" \
                   "\n-优先级<优先级>" \
                   "\n-前置条件<前置条件>" \
                   "\n-步骤描述<步骤描述>" \
                   "\n-预期结果<预期结果>" \
                   "\n请使用中文回答, 请勿返回除测试用例内容以外的任何内容。不要用引号包装响应。"

st.set_page_config(page_title="TestCaseGPT", page_icon="🤖", layout="wide")
with st.sidebar:
    lottie_image1 = load_lottie_url('https://lottie.host/466b9539-3305-4b03-874a-f816c81cff14/bVKY16a7as.json')
    st_lottie(lottie_image1)

st.markdown(
    """
    <h1 style='text-align: center;'>TestCaseGPT，测试流程加速器 🚀️</h1>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div style='text-align: center;'>
        <h3>将用户故事转化为测试用例，只需一步 ！🛠</h3>
    </div>
    """,
    unsafe_allow_html=True,
)
user_story = st.text_area(label="🤖", label_visibility="hidden",
                          placeholder="请输入用户故事：" + "作为___，我希望___，以便___。")

# 处理用户输入并生成验收标准和测试用例
if st.button("一键生成测试用例"):
    class Chat:
        def __init__(self, prompt) -> None:
            # 初始化对话列表，可以加入一个key为system的字典，有助于形成更加个性化的回答
            self.conversation_list = [{'role': 'system', 'content': prompt}]

        # 提示chatgpt
        def ask(self, topic):
            self.conversation_list.append({"role": "user", "content": "\nTopic: " + topic})
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.conversation_list)
            answer = response.choices[0].message['content']
            return answer


    criteria = Chat(prompt_user_story).ask(user_story)


    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    local_css("style.css")
    expander = st.expander(label="🤖 测试点拆分")
    expander.write(criteria)
    all_case = re.split(r'\n', criteria)


    def export_testcase(testcase):
        name = re.findall('用例名称：(.+)', testcase)[0].strip()
        case_type = re.findall('用例类型：(.+)', testcase)[0].strip()
        priority = re.findall('优先级：(.+)', testcase)[0].strip()
        precondition = re.findall('前置条件：(.+)', testcase)[0].strip()
        steps = re.findall('步骤描述：(.+)', testcase, re.DOTALL)[0].strip()
        expected_result = re.findall('-预期结果：(.+)', testcase)[0].strip()
        test_case_data = {'用例名称': name, '用例类型': case_type, '优先级': priority, '前置条件': precondition,
                          '步骤描述': steps, '预期结果': expected_result}
        # 将测试用例数据转换为 Pandas 数据框
        test_case_df = pd.DataFrame(test_case_data)

        # 显示测试用例数据
        st.dataframe(test_case_df)


    for case_title in all_case:
        case_title = re.split(r'\d+\.\s+', case_title)[1]
        test_case = Chat(prompt_test_case).ask(case_title)
        st.write( test_case)
        #export_testcase(test_case)
