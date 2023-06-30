formula = "((a+b)*c)"
# formula = "(a*b)+(a*c)"
import re
# 正则匹配出formula 中的最外围括号内的内容
formula = re.findall(r"(\([a-z\+\-*\/()]+\))",formula)[0]
# formula =re.search(r"\(([a-z\+\-*\/()]+)\)",formula)
# formula = formula.group(1)

print(formula)