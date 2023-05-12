import json

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
                           placeholder="【用户故事描述】：作为___，我希望___，以便___。", key="input")
prompt_userstory = "我希望你作为一个软件产品经理，负责生成验收标准，用来验证软件是否符合用户故事中指定的功能要求。验收标准应该是具体的、可衡量的、可实现的、相关的。此外，你应该确保验收标准涵盖所有可能的情况和边缘案例。通过定义清晰而全面的验收标准，你可以帮助确保软件符合必要的标准，并确保用户的需求得到满足。按照描述的格式，就下面的主题写出3条专业而详细的验收标准。请尽你最大的努力。用中文回答。只返回验收标准的内容。不要返回其他内容。" \
                   "\n主题: " + user_story

prompt_testcase1 = "您是软件测试和软件质量保证方面的专家，专门从事测试用例编写。您帮助我之前的许多人，生成了满足特定需求的功能测试用例。您生成的测试用例能涵盖正常场景、异常场景和边界场景。" \
                  "测试用例格式请参考:" \
                  "\n用例名称:这是一个测试用例" \
                  "\n优先级:可选值：P0、P1、P2" \
                  "\n前置条件:这是一个测试用例的前置条件" \
                  "\n步骤描述:" \
                  "\n#第一个步骤" \
                  "\n#第二个步骤" \
                  "\n#第三个步骤" \
                  "\n预期结果:" \
                  "\n#第一个预期结果" \
                  "\n#第二个预期结果" \
                  "\n#第三个预期结果" \
                  "\n请用中文回答，请勿返回测试用例以外的其他任何内容。" \
                  "\n请根据我输入的主题编写2个详细、符合要求的测试用例。"

prompt_testcase = "您是软件测试和软件质量保证方面的专家,专门从事功能测试,您帮助我之前的许多人生成了满足特定要求的功能测试用例。\n" \
                  "您生成的测试用例能涵盖正常场景、异常场景、边界场景。\n" \
                  "您生成的测试用例优先级包括 P0、P1、P2，P0为最高优先级，P2代表最低优先级。\n" \
                  "以所述测试用例格式，至少编写两条关于以下主题的专业和详细测试用例。尽你最大的努力。请使用中文回答, 请勿返回除测试用例内容以外的其他内容。不要用引号包装响应。\n" \
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
    # 先对文本按照换行符进行分割
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        # 如果是空行，空字符串，单个字符串，直接丢弃
        if len(line) < 2:
            continue
        new_lines.append(re.sub(r'^(\d+).', '📝 ', line))

    text = "\n".join(new_lines)
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
                                         temperature=0.7
                                         ):
        openai_resp.append(resp.choices[0].text)
        generate_criteria = "".join(openai_resp).strip()
        formatted_text = f"<p style='white-space: pre-wrap; font-size: 16px; text-align: left;'>{clean_criteria(generate_criteria)}</p>"
        criteria_box.markdown(formatted_text, unsafe_allow_html=True)
    return generate_criteria


def output_testcase(case_title):
    formatted_text = ""
    openai_resp = []
    prompt = prompt_testcase + case_title
    for resp in openai.Completion.create(model="text-davinci-003", prompt=prompt, stream=True,
                                         max_tokens=3072,
                                         temperature=0.7):
        openai_resp.append(resp.choices[0].text)
        generate_testcase = "".join(openai_resp).strip()
        formatted_text = clean_testcase(generate_testcase)
        markdown_text = f"<p style='white-space: pre-wrap; font-size: 16px; text-align: left;'>{formatted_text}</p>"
        case_box.markdown(markdown_text, unsafe_allow_html=True)
    return formatted_text


def export_testcase(InputCase):
    # 定义正则表达式
    # regex = r"用例编号：(\S+) 用例名称：(\S+) 用例类型：(\S+) 优先级：(\S+) 前置条件：(.+) 步骤描述：(.+) 预期结果：(.+)"
    regex = r"用例编号(.+) 用例名称(.+) 用例类型(.+) 优先级(.+) 前置条件(.+) 步骤描述(.+) 预期结果(.+)"
    TestCaseLines = re.findall(regex, InputCase)
    CaseIds = []
    Names = []
    CaseTypes = []
    Priorities = []
    Preconditions = []
    Steps = []
    ExpectedResults = []
    for line in TestCaseLines:
        # 删除开头的中英文冒号和空格
        CaseId = line[0]
        CaseId = re.sub(r'^:', '', CaseId)
        CaseId = re.sub(r'^：', '', CaseId).strip()
        CaseIds.append(CaseId)

        # 删除开头的中英文冒号和空格
        Name = line[1]
        Name = re.sub(r'^:', '', Name)
        Name = re.sub(r'^：', '', Name).strip()
        Names.append(Name)

        # 删除开头的中英文冒号和空格
        CaseType = line[2]
        CaseType = re.sub(r'^:', '', CaseType)
        CaseType = re.sub(r'^：', '', CaseType).strip()
        CaseTypes.append(CaseType)

        # 删除开头的中英文冒号和空格
        Priority = line[3]
        Priority = re.sub(r'^:', '', Priority)
        Priority = re.sub(r'^：', '', Priority).strip()
        Priorities.append(Priority)

        # 删除开头的中英文冒号和空格
        Precondition = line[4]
        Precondition = re.sub(r'^:', '', Precondition)
        Precondition = re.sub(r'^：', '', Precondition).strip()
        Preconditions.append(Precondition)

        # 删除开头的中英文冒号和空格
        Step = line[5]
        Step = re.sub(r'^:', '', Step)
        Step = re.sub(r'^：', '', Step).strip()
        Steps.append(Step)

        # 删除开头的中英文冒号和空格
        ExpectedResult = line[6]
        ExpectedResult = re.sub(r'^:', '', ExpectedResult)
        ExpectedResult = re.sub(r'^：', '', ExpectedResult).strip()
        ExpectedResults.append(ExpectedResult)

    test_case_data = {'用例名称': Names, '用例类型': CaseTypes, '优先级': Priorities,
                      '前置条件': Preconditions,
                      '步骤描述': Steps, '预期结果': ExpectedResults}
    data = pd.DataFrame(test_case_data)
    st.dataframe(data)


if st.button("一键生成测试用例", type="primary"):
    print(user_story)
    user_story.replace("\n", "")
    criteria_box = st.expander(label="测试点拆分", expanded=True)
    with criteria_box:
        criteria_box = st.empty()
        print(prompt_userstory)
        criteria = output_criteria(prompt_userstory)
    testcase_box = st.expander(label="测试用例生成", expanded=True)
    with testcase_box:
        case_box = st.empty()
        print("Criteria Str:")
        print(criteria)
        all_case = re.split(r"\n", criteria)
        print("Criteria List:")
        print(criteria)
        case_list = []
        for case in all_case:
            print("before sub")
            print(case)
            case = re.sub(r'^(\d+).', '', case)
            case = case.lstrip()
            print("after sub")
            print(case)
            if len(case) < 2:
                continue
            case_list.append(case)
        print(case_list)
    testcase = output_testcase(case_list[0])
    export_testcase(testcase)
