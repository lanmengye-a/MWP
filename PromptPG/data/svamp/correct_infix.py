import json
def restore_variate(expression):
    for i in range(10):
        expression = expression.replace(chr(97 + i), f"{i}")
    for i in range(10):
        expression = expression.replace(f"{i}", f"number{i}")
    return expression

with open("svampformula_train.jsonl") as reader:
    with open("svampformula_train.jsonl", "a+", encoding="utf-8") as writer:
        try:
            for line in reader:
                line=json.loads(line)
                print(line.keys())
                infixFormulaAlpha = line["infixEquation"]
                infixFormula = restore_variate(line["infixEquation"])
                line["infixEquation"] = infixFormula
                line["infixEquationAlpha"] = infixFormulaAlpha
                writer.write(json.dumps(line, ensure_ascii=False) + "\n")
        except Exception as e:
            print(e)
