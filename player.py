class Player():
  def __init__(self, name, number, team, positions=[]):
    self.name = name 
    self.number = number 
    self.team = team
    self.positions = positions
    self.at_bat = 0 
    self.hit = 0 
    self.bb = 0
    self.so = 0
    self.hr = 0
    self.rbi = 0
    self.runs = 0
    self.singles = 0
    self.doubles = 0
    self.triples = 0
    self.sac_fly = 0
    self.BABIP = 0
    self.SLG = 0
    self.AVG = 0
    self.ISO = 0

  def __str__(self):
    ret = f'Name: {self.name}\nNumber: {self.number}\nPrimary Position: {self.positions[0]}\n'
    ret += f'At Bats: {self.at_bat}\nHits: {self.hit}\nWalks: {self.bb}\nSO: {self.so}\nHR: {self.hr}\n'
    ret += f'Runs: {self.runs}\nRBI: {self.rbi}\nBABIP: {self.BABIP}\nSLG: {self.SLG}\nAVG: {self.AVG}\nISO: {self.ISO}\n' 
    return ret
  
  def format_player(self, raw_lst):
    team = raw_lst[0]
    name, number = raw_lst [1::2]
    positions = raw_lst[3:]
    #print(raw_lst)
    #print('team', team)
    #print('name', name)
    #print('number', number)
    new_player = Player(name, number, team, positions)
    return new_player

  def format_decimal(self, num):
    return "{:.3f}".format(num)
  
  def set_at_bat(self, val, flag=True):
    if flag:
      self.at_bat += val
    else:
      self.at_bat = val
  
  def set_hit(self, val, flag=True):
    if flag:
      self.hit += val
    else:
      self.hit = val
    #print('at bat:',self.at_bat)
  
  def set_bb(self, val, flag=True):
    if flag:
      self.bb += val
    else:
      self.bb = val
  
  def set_so(self, val, flag=True):
    if flag:
      self.so += val
    else:
      self.so = val
  
  def set_hr(self, val, flag=True):
    if flag:
      self.hr += val
    else:
      self.hr = val

  def set_rbi(self, val, flag=True):
    if flag:
      self.hit += val
    else:
      self.hit = val
  
  def set_runs(self, val, flag=True):
    if flag:
      self.runs += val
    else:
      self.runs = val

  def set_sac_fly(self, val, flag=True):
    if flag:
      self.sac_fly += val
    else:
      self.sac_fly = val

  def set_singles(self, val, flag=True):
    self.singles += val 

  def set_doubles(self, val, flag=True):
    self.doubles += val 
  
  def set_triples(self, val, flag=True):
    self.triples += val 
  
  def set_AVG(self):
    self.AVG = self.calc_AVG()
  
  def set_BABIP(self):
    self.BABIP = self.calc_BABIP()

  def set_SLG(self):
    self.SLG = self.calc_SLG()
  
  def set_ISO(self):
    self.ISO = self.calc_ISO()

  def get_at_bat(self):
    return self.at_bat 
  
  def get_BABIP(self):
    return self.BABIP
  
  def get_SLG(self):
    return self.SLG
  
  def get_AVG(self):
    return self.AVG

  def get_ISO(self):
    return self.ISO 

  def calc_BABIP(self):
    #(H - HR)/(AB - K - HR + SF)
    ret = (self.hit - self.hr)/(self.at_bat - self.so - self.hr + self.sac_fly)
    return self.format_decimal(ret)
    
  def calc_SLG(self):
    #(1B + 2Bx2 + 3Bx3 + HRx4)/AB
    ret = ( self.singles + (2 * self.doubles) + (3 * self.triples) + (4 * self.hr) ) / self.at_bat 
    return self.format_decimal(ret)
  
  def calc_AVG(self):
    ret = 0
    if self.at_bat > 0:
      ret = self.hit / self.at_bat
      #print(self.at_bat, self.hit)
    return self.format_decimal(ret)
  
  def calc_ISO(self):
    #(1x2B + 2x3B + 3xHR) / At-bats OR Slugging percentage - Batting average
    ret = ( (1 * self.doubles) + (2 * self.triples) + (3 * self.hr ) ) / self.SLG - self.AVG
    return self.format_decimal(ret)
  
'''
test = Player('Nick', 18, 'Beef', ['shortstop', 'pitcher'])
#print(test)

test.set_at_bat(4)
test.set_hit(2)
test.set_walk(1)
test.set_so(1)
test.set_singles(1)
test.set_doubles(1)

avg = test.calc_AVG()
#print(avg)

babip = test.calc_BABIP()
#print(babip)

slg = test.calc_SLG()
#print(slg)

iso = test.calc_ISO()
#print(iso)

#print(test.get_AVG())
'''
