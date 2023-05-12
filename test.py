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
print_result()
print(print_result)
