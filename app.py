import dotenv
import numpy as np
import openai
import re
import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_extras.let_it_rain import rain
from utils import load_lottie_url

st.set_page_config(page_title="TestCaseGPT", page_icon="🤖", layout="wide")
config = dotenv.dotenv_values(".env")
openai.api_key = config['OPENAI_API_KEY']

with st.sidebar:
    lottie_image1 = load_lottie_url('https://assets1.lottiefiles.com/packages/lf20_ofa3xwo7.json')
    st_lottie(lottie_image1)

st.markdown(
    """
    <h1 style='text-align: center;'>TestCaseGPT，测试流程加速器 🚀️</h1>
    <h3 style='text-align: center;'>将用户故事转化为测试用例，只需一步 ！</h3>
    """,
    unsafe_allow_html=True
)


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style.css")
user_story = st.text_input(label="📖 用户故事", label_visibility="hidden",
                           placeholder="用户故事描述：" + "作为___，我希望___，以便___。", key="input")
prompt_userstory = f"I want you to act as a software project manager responsible for generate acceptance criteria that can be used to validate that the software meets the functional requirements specified in the user stories." \
                   "\nThe acceptance criteria should be specific, measurable, achievable, relevant, and time-bound." \
                   "\nAdditionally, you should ensure that the acceptance criteria cover all possible scenarios and edge cases." \
                   "\nBy defining clear and comprehensive acceptance criteria, you can help ensure that the software meets the necessary standards and that the user's needs have been fulfilled." \
                   "\nWrite at least 10 professional and detailed acceptance criteria about the topic below in the described format. Make your best effort." \
                   "\nAnswer in Chinese.Only return acceptance criteria content" \
                   "\nDo not return anything else.Do not wrap responses in quotes" \
                   "\nTopic: " + user_story
prompt_testcase = f"您是软件测试和软件质量保证方面的专家,专门从事功能测试,您帮助我之前的许多人生成了满足特定要求的功能测试用例。\n" \
                  "您生成的测试用例能涵盖正常场景、异常场景、边界场景。\n" \
                  "您生成的测试用例优先级包括 P0、P1、P2，P0为最高优先级，P2代表最低优先级。\n" \
                  "以所述测试用例格式，至少编写五条关于以下主题的专业和详细测试用例。尽你最大的努力。请使用中文回答, 请勿返回除测试用例内容以外的其他内容。不要用引号包装响应。\n" \
                  "测试用例格式:\n" \
                  "用例编号:\n" \
                  "用例名称:\n" \
                  "用例类型:\n" \
                  "优先级:\n" \
                  "前置条件:\n" \
                  "步骤描述:\n" \
                  "预期结果:\n" \
                  "主题: "


def clean_criteria(text):
    # 使用正则表达式替换特殊字符
    text = re.sub(r'[；。]', '', text)
    text = re.sub(r'(\d+)\.', '📝 ', text)
    return text


def clean_testcase(text):
    # 先对文本按照换行符进行分割，如果有连续的换行符，那么分割出来的元素会是空字符串
    lines = text.split("\n")
    new_lines = ""
    for line in lines:
        # 如果不是空字符串，那么就是正常的文本，需要进行处理
        if line != "":
            # 先把正常文本开头的数字和点给去掉
            line = re.sub(r'^(\d+)\. ', '', line)
            # 继续去除末尾的空字符串
            line = line.rstrip()
            # 把处理好的文本拼接起来
            new_lines += line + " "
        # 如果是空字符串，那么就是连续的换行符
        else:
            # 先把新字符串末尾的
            new_lines.rstrip(" ")
            # 再添加一个换行符，用来分隔不同的测试用例
            new_lines += "\n"

    return new_lines

def output_criteria(prompt):
    # 输出验收标准
    generate_criteria = ""
    openai_resp = []
    for resp in openai.Completion.create(model="text-davinci-003", prompt=prompt, stream=True,
                                         max_tokens=1024,
                                         temperature=0.7):
        openai_resp.append(resp.choices[0].text)
        generate_criteria = "".join(openai_resp).strip()
        formatted_text = f"<p style='white-space: pre-wrap; font-size: 16px; text-align: left;'>{clean_criteria(generate_criteria)}</p>"
        criteria_box.markdown(formatted_text, unsafe_allow_html=True)
    return generate_criteria


def output_testcase(case_title):
    # 输出测试用例
    formatted_text = ""
    openai_resp = []
    prompt = prompt_testcase + case_title
    for resp in openai.Completion.create(model="text-davinci-003", prompt=prompt, stream=True,
                                         max_tokens=3072,
                                         temperature=0.7):
        openai_resp.append(resp.choices[0].text)
        generate_testcase = "".join(openai_resp).strip()
        formatted_text = clean_testcase(generate_testcase)
        case_box.markdown(formatted_text, unsafe_allow_html=True)
    print(formatted_text)
    return formatted_text


def export_testcase(InputCase):
    # 定义正则表达式
    regex = r"用例编号：(\S+) 用例名称：(\S+) 用例类型：(\S+) 优先级：(\S+) 前置条件：(.+) 步骤描述：(.+) 预期结果：(.+)"
    TestCaseLines = re.findall(regex, InputCase)

    CaseIds = []
    Names = []
    CaseTypes = []
    Priority = []
    Preconditions = []
    Steps = []
    ExpectedResults = []
    for line in TestCaseLines:
        CaseIds.append(line[0])
        Names.append(line[1])
        CaseTypes.append(line[2])
        Priority.append(line[3])
        Preconditions.append(line[4])
        Steps.append(line[5])
        ExpectedResults.append(line[6])

    test_case_data = {'用例编号': CaseIds, '用例名称': Names, '用例类型': CaseTypes, '优先级': Priority,
                      '前置条件': Preconditions,
                      '步骤描述': Steps, '预期结果': ExpectedResults}
    data = pd.DataFrame(test_case_data)
    st.dataframe(data)


if st.button("一键生成测试用例", type="primary"):
    criteria_box = st.expander(label="测试点拆分", expanded=True)
    with criteria_box:
        criteria_box = st.empty()
        criteria = output_criteria(prompt_userstory)

    testcase_box = st.expander(label="测试用例生成", expanded=True)
    with testcase_box:
        case_box = st.empty()
        all_case = re.split(r"\n", criteria)
        case_list = []
        for case in all_case:
            print("before sub")
            print(case)
            case = re.sub(r"(^\d+).", "", case).strip()
            print("after sub")
            print(case)
            case_list.append(case)
        testcase = output_testcase(case_list[0])

        export_testcase(testcase)

