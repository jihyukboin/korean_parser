sent = '안녕하세요너의이름은무엇입니까내이름은파이썬입니다           파이썬좋아      하시나요.'

new_sent = sent.replace(" ", '')

from pykospacing import Spacing
spacing = Spacing()
kospacing_sent = spacing(new_sent) 

print(sent)
print(kospacing_sent)