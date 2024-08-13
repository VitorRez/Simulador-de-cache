class Cache:
  def __init__(self):
    self.cache = []
    a = [-1 for i in range(256)]
    b = [-1 for i in range(256)]
    c = [-1 for i in range(256)]
    d = [-1 for i in range(256)]
    self.cache.append(a)
    self.cache.append(b)
    self.cache.append(c)
    self.cache.append(d)


  def divideLinha(self, linha):
    v = linha.split()

    return v


  def ReadWrite(self, linha):
    v = self.divideLinha(linha)
    nuc = int(v[0]) #nucleo q será acessado
    rw = v[1] #leitura ou escrita
    endB = v[2] #endereço de acesso

    bits = self.separaBits(endB)
    iEnd = int(self.mapeamento(endB, bits[2]))

    rh = 0
    if rw == "r":
      i = str(self.cache[nuc][iEnd])
      if i != "-1":
        if i[3:6] == bits[1]: #cache hit / Acho q n ta certo n considerar o bit de validade
          rh = 1
        else: #cache miss
          self.cache[nuc][iEnd] = "00" + str(bits[0]) + str(bits[1]) #bit Val e tag

      else: #cache miss
        self.cache[nuc][iEnd] = "00" + str(bits[0]) + str(bits[1]) #bit Val e tag
    
    elif rw == "w":
      self.cache[nuc][iEnd] = "00" + str(bits[0]) + str(bits[1]) #bit Val e tag
  

    t = self.transicao(iEnd, nuc, rw, int(bits[1], 2))
    self.transicao_outras(iEnd, nuc, t)
    print("cache:", nuc, "Transição:", t, "Hit ou Miss", rh, "Estados", self.cache[0][iEnd], self.cache[1][iEnd], self.cache[2][iEnd], self.cache[3][iEnd])
    return rh #se 0 deu miss, se 1 deu hit
  

  def mapeamento(self, endB, ind): #retorna o endereço a ser acessado
    #numDec = float(int(endB, 2))
    numDec = int(ind, 2) #teste
    end = numDec % 256

    return end


  def separaBits(self, endB): #separa o endereço de acesso em bit de Val., tag, indice, offBloco, offByte
    bitV = endB[0]
    tag = endB[1:4]
    indice = endB[4:12]
    offBloco = endB[12:14]
    offByte = endB[14:16]

    return bitV, tag, indice, offBloco, offByte


  def transicao(self, end, cache, rw, tag):
    #end -> endereço do bloco = índice
    #cache -> cache que está lendo/escrevendo
    #rw -> se está lendo, ou escrevendo

    t = '001' #read miss, sem copia em outras caches
    if rw == "r": #caso leitura
      for i in self.cache:
        for j in i:
          if j != -1:
            if j[2] == '1' and j[3:6] == tag:
              t = '010' #read miss com copia em outras caches
          
    if rw == "w": #caso escrita
      t = '110'
    

    self.attEstado(cache, end, t)

    return t


  def attEstado(self, cache, end, t):
    i = self.cache[cache][end]
    if t == "001":
        self.cache[cache][end] = i.replace(i[0:2], "10")

    elif t == "010":
      self.cache[cache][end] = i.replace(i[0:2], "01")

    elif t == "110":
      self.cache[cache][end] = i.replace(i[0:2], "11")


    #tratamento pra um erro q n soube resolver
    j = self.cache[cache][end]
    if j[2:6] != i[2:6]:
      self.cache[cache][end] = j.replace(j[2:6], i[2:6])

  def transicao_outras(self, end, cache, t):
    for i in self.cache:
      if i != self.cache[cache]:
        if i[end] != -1:
          if i[end][0:2] == '11':
            if t == "110":
              i[end] = i[end].replace(i[end][0:2], "00")
            if t == "010":
              i[end] = i[end].replace(i[end][0:2], "01")
          if i[end][0:2] == '10':
            if t == "110":
              i[end] = i[end].replace(i[end][0:2], "00")
            if t == "010":
              i[end] = i[end].replace(i[end][0:2], "01")
          if i[end][0:2] == '01':
            if t == "110":
              i[end] = i[end].replace(i[end][0:2], "00")
          
          
           