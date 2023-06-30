# 将train.xlsx 文件中Question字符串中的number# (#表示用数字区分的变量)按序替换为Numbes中的数
import pandas as pd
def replace_numbers(question, numbers):
    numbers = numbers.split(" ")
    for i, number in enumerate(numbers):
        question = question.replace(f"number{i}", str(number))
    return question
if __name__ == '__main__':
    df = pd.read_excel("train.xlsx")
    # df.loc[i, "Numbers"]设置为字符串读入
    df["Numbers"] = df["Numbers"].astype(str)
    for i in range(len(df)):
        df.loc[i, "Question"] = replace_numbers(df.loc[i, "Question"], df.loc[i, "Numbers"])
    # 将df转换为json 并添加一个值为null的unit字段,设置好json的输出格式为每个键值对为一行
    df["unit"] = None
    df["option"] = None
    df.to_json("svamp_train.json", orient="records", force_ascii=False)