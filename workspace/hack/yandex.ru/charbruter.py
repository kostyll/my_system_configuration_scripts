GENERAL_VOCABULARY = """.0123456789abcdefghijklmnopqrstuvdxyz,@~[]()"""
def getpasswords(deepth=6, vocabulary=GENERAL_VOCABULARY):
    result = []
    for char in vocabulary:
         result.append(char+getpasswords(deepth-1,vocabulary))
    return result

def getpasswords(deepth=6,vocabulary=GENERAL_VOCABULARY):
    result = []
    iter_pattern = "{}for char{} in '{}' :\n{}"
    iter_expression = iter_pattern
    for i in range(deepth) :
        iter_expression = iter_expression.format('\t'*i,i,vocabulary,iter_pattern)
    iter_expression = iter_expression.format('\t'*(i+1),i,vocabulary,'\t'*(i+2)+"result.append({})")
    iter_expression = iter_expression.format("char0"+" ".join("+char{}".format(sym+1) for sym in range(i)))
    iter_expression = iter_expression+'\n'+'\t'*(i+2)+"print char0"+"".join("+char{}".format(sym+1) for sym in range(i))
    print iter_expression
    exec(iter_expression)
    return result
    
    

print getpasswords(deepth=4)
