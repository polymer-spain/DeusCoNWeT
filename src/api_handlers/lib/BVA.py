import random
from itertools import permutations, combinations, tee, chain

class BVA(object):
    def __init__(self, components, versions, times_called=0):
        
        # List of components
        self.components = components
        # List of versiones
        self.versions = versions
        
        # Times that a new scenario is required 
        self.times_called = times_called
        self.good_version = versions[0]
        self.bad_versions = versions[1:]

        # Puntero al inicio
        self.init = 0
        self.end = len(self.components)

        # Already created
        self.list_assigned = {}
        self._generateRepeted = [False] * (len(self.components) +1)
        # Iterador de las versiones
        self._versionIterator = []
        # Iterador inicial para resetear los iteradores
        self._initialIterator = []

        self._permutationsUsed = [[]]*(len(self.components) + 1)

        # iterador real de cada version mala
        self.iterators = []
        self.nextVersion = []
        # Cogemos los iteradores necesarios para generar las versiones
        # desde 0 versiones malas a todas
        for idx in range(len(components)+1):
          if idx == 0:
            self.iterators.append([self.good_version]* len(self.versions))
            self._versionIterator.append([])
            self._initialIterator.append([])
            self.nextVersion.append([])
          else:
            permutations = self.generatePermutation(idx)
            ## Inicializamos los punteros
            its_initial = []
            its_version = []
            for perm in permutations:
              first_it, second_it = tee(perm)
              its_initial.append(first_it)
              its_version.append(second_it)
            self._versionIterator.append(its_initial)
            self._initialIterator.append(its_version)
            
            # Cogemos el primer vector de versiones --> [ [[x,y,z],[y,z]],...]
            self.nextVersion.append(self.getInitialVersion(idx))

            # Cogemos un iterador a esa version
            self.iterators.append(self.getVersionIterator(idx))

    # Reset the times called without reset list of scenarios generated
    def restartValues(self):
        self.times_called = 0
    
    # Mira el numero de elementos que necesita y hace combinaciones con el `number`.
    # Si ese `number` es mayor a la lista de versiones, pasa tantos generadores como sean requeridos
    # Devuelve un array de iteradores
    # Ej: si tenemos 7 versiones y `number` es 9, devuelve un iterador de 7 vecesiones y otro de 2.
    def generatePermutation(self, number):
        _versions = self.bad_versions
        _combinations = []
        _versions_len = len(_versions)
        
        if number <= _versions_len:
            _combinations.append(combinations(_versions, number))
        else:
            next_value = _versions_len
            remaining = number
            while  next_value > 0:
                _combinations.append(combinations(_versions, next_value))
                remaining -= next_value
                next_value = min([_versions_len, remaining])
        return _combinations

    def getInitialVersion(self, nBad):
      listVersions = [ iterator.next() for iterator in self._versionIterator[nBad]]

      return listVersions
    
    def getNextVersion(self, nBad):
      next = None
      pos = len(self._versionIterator[nBad])-1
      # Buscamos hasta encontrar uno nuevo

      while not next:
        # Intentamos coger uno del ultimo iterador
        try:
          next = self._versionIterator[nBad][pos].next()
          self.nextVersion[nBad][pos] = next
        except StopIteration:
          # Si no tiene, lo reiniciamos y lo ponemos al primer elemento
          first_it, second_it = tee(self._initialIterator[nBad][pos])
          self._initialIterator[nBad][pos] = first_it
          self._versionIterator[nBad][pos] = second_it
          self._generateRepeted[nBad] = True
          # Avanzamos el puntero para comprobar el segundo iterador
          pos-=1
          # Si era el ultimo, volvemos al principio
          if pos < 0:
            pos = len(self._versionIterator[nBad])-1

    def getVersionIterator(self, nBad):
      # Si es 0 no creamos iterador
      # Cogemos el resto de versiones a buenas
      vectorGood = [self.good_version] * (len(self.components) - nBad)
      # unimos las versiones malas en un array (tendremos [["a"],["b"],..])
      badVersion = [version for version in reduce(lambda x,y: x+y, self.nextVersion[nBad])]
      
      
        
      # avanzamos el puntero de las versiones malas
      self.getNextVersion(nBad)

      return permutations(vectorGood + badVersion, len(self.components))

    def getVersion(self, nBad):
      version = None
      name = None
      if nBad == 0:
        version= [self.good_version] * len(self.components)
      else:
        while not version:
          try:
            version = self.iterators[nBad].next()
            name = str(version)
            if name in self.list_assigned and not self._generateRepeted[nBad]:
              version = None
          except StopIteration:
            self.iterators[nBad] = self.getVersionIterator(nBad)
      self.list_assigned[name] = True
      return version


    def getSceneario(self):
      versions = []
      
      # Las versiones pares por un lado y las impares por otro
      if self.times_called % 2 ==0:
        # Cogemos la version correspondiente al puntero
        versions = self.getVersion(self.init)
        # Si el puntero inicial llega a su fin, volvemos al principio
        self.init+=1
        if self.init > len(self.versions):
          self.init = 0
      else:
        versions = self.getVersion(self.end)
        self.end-=1
        # Si el puntero llega al inicio, volvemos al fin
        if self.end < 0:
          self.end = len(self.versions)
      
      self.times_called+=1

      return versions
      
if __name__ == "__main__":
    components = ["twitter-timeline","facebook-wall","pinterest-timeline","googleplus-timeline","traffic-incidents","finance-search","open-weather","spotify-component","reddit-timeline"]
    versions = ["stable","latency","security","structural","usability","maintenance","accuracy","complexity"]
    times = 100
    import sys
    if len(sys.argv) > 1:
      times = int(sys.argv[1])
    
    bva = BVA(components, versions)
    scenarios = []
    for i in range(times):
        scenario = bva.getSceneario()
        scenarios.append(scenario)
    # print len(scenarios)
    repetidos = 0
    # for idx, sc in enumerate(scenarios):
    #     if sc.count('stable') < 5:
    #       if scenarios.count(sc) > 1:
    #         repetidos += 1
    #         print idx, sc
