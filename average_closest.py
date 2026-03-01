import random as rd

list_num = []

def list_generator():
    """
    Gera 50 numeros inteiros aleatorios entre 1 a 100 e armazena
    esses valores na lista global 'lista_num'. 
    Ao final, Imprime a lista gerada.
    """
    for i in range(50):
        number = rd.randint(1, 100)
        list_num.append(number)
    print("LIST:", list_num)

def media():
    """
    Calcula e retorna a media aritmetica dos valores armazenados
    na lista global 'lista_num'.
    """
    return sum(list_num) / len(list_num)

def search_closest():
    """
    Encontra e retorna o valor da lista global 'list_num'
    que esta mais proximo da media da propria lista.
    """
    avg = media()
    closest = list_num[0]
    
    for x in list_num:
        diff_current = abs(x - avg)
        diff_closest = abs(closest - avg)
        
        if diff_current < diff_closest:
            closest = x
            
    return closest

def show_closests():
    """
    Exibe na tela todos os valores da lista global 'list_num'
    cuja diferença para o valor mais próximo da média seja
    menor ou igual a 3.
    """
    closest = search_closest()
    for i in range(len(list_num)):
        if abs(list_num[i] - closest) <= 3:
            print(list_num[i])

list_generator()
print("MEDIA:", media())
print("CLOSESTS:")
show_closests()
