import openai
import dotenv

config = dotenv.dotenv_values(".env")
openai.api_key = config['OPENAI_API_KEY']

prompt_user_story1 = f"I want you to act as a software project manager responsible for generate acceptance criteria that can be used to validate that the software meets the functional requirements specified in the user stories." \
                     "\nThe acceptance criteria should be specific, measurable, achievable, relevant, and time-bound. " \
                     "\nAdditionally, you should ensure that the acceptance criteria cover all possible scenarios and edge cases." \
                     "\nBy defining clear and comprehensive acceptance criteria, you can help ensure that the software meets the necessary standards and that the user's needs have been fulfilled." \
                     "\nWrite at least 10 professional and detailed acceptance criteria about the topic below in the described format. Make your best effort." \
                     "\nAnswer in Chinese.Only return acceptance criteria content" \
                     "\nDo not return anything else.Do not wrap responses in quotes" \
                     "\nTopic: " + "作为用户，我希望能够在网上购买商品，以便不用去实体店"
prompt_testcase = "您是软件测试和软件质量保证方面的专家，专门从事功能测试，您帮助我之前的许多人生成了满足特定要求的功能测试用例。您生成的测试用例能涵盖正常场景、异常场景、边界场景。" \
                  "\n测试用例格式请参考：" \
                  "\n用例名称：这是一个测试用例" \
                  "\n用例类型：可选值：功能测试" \
                  "\n优先级：可选值：P0、P1、P2" \
                  "\n前置条件：这是一个测试用例的前置条件" \
                  "\n步骤描述：" \
                  "\n#第一个步骤" \
                  "\n#第二个步骤" \
                  "\n#第三个步骤\n" \
                  "\n预期结果：" \
                  "\n#第一个预期结果" \
                  "\n#第二个预期结果" \
                  "\n#第三个预期结果" \
                  "\n请此测试用例格式，用中文编写5个关于以下主题的专业和详细测试用例，请勿返回除测试用例内容以外的其他内容，不要用数字、点符号、引号包装响应，当我输入主题时，再返回响应"
report = []


def print_result():
    for resp in openai.Completion.create(model='text-davinci-003',
                                         prompt=prompt_user_story1,
                                         max_tokens=3000,
                                         temperature=0.5,
                                         stream=True):
        # join method to concatenate the elements of the list
        # into a single string,
        # then strip out any empty strings
        report.append(resp.choices[0].text)
        result = "".join(report).strip()
        return result


# res_box.markdown(f'*{result}*')
# print_result()
# print(print_result)
print(prompt_testcase)