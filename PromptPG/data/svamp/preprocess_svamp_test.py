# 将train.xlsx 文件中Question字符串中的number# (#表示用数字区分的变量)按序替换为Numbes中的数
import pandas as pd
def replace_numbers(question, numbers):
    numbers = numbers.split(" ")
    for i, number in enumerate(numbers):
        question = question.replace(f"number{i}", str(number))
    return question
if __name__ == '__main__':
    # 修改svamp_test.json中每条数据的Question字段
    df = pd.read_json("svamp_test_pre.json")
    for i in range(len(df)):
        df.loc[i, "Question"] = df.loc[i,"Body"]+df.loc[i, "Question"]
    # 将df转换为json 并添加一个值为null的unit字段,设置好json的输出格式为每个键值对为一行
    df["unit"] = None
    df["option"] = None
    df.to_json("svamp_test.json", orient="records", force_ascii=False)