import random
import copy
from itertools import permutations, combinations

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
        # List of versions for each component (Deprecated?)
        self._permutationList = []*(len(self.components) +1)
        self._permutationsUsed = [[]]*(len(self.components) + 1)

        for idx in range(len(components)+1):
            self._permutationList.append(self.generatePermutation(idx))
        
        self._scenarioList = [False]*(len(self.components) +1)
        # Predefined scenarios
        self._endPredefined = 0
        self.scenarios = self.generateScenarios()

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


    def generateNextScenario(self, nBadVersions):
        scenario = []
        try:
            for iterator in self._permutationList[nBadVersions]:
                scenario += list(iterator.next())

            stable_list = [self.good_version] * (len(self.components) - nBadVersions)
            total_versions = scenario + stable_list
            self._scenarioList[nBadVersions] = permutations(list(total_versions), len(self.components))

        # Si no hay mas permutaciones se vuelven a generar
        except StopIteration:
            self._permutationList[nBadVersions] = self.generatePermutation(nBadVersions)
            for iterator in self._permutationList[nBadVersions]:
                scenario += list(iterator.next())
            
            stable_list = [self.good_version] * (len(self.components) - nBadVersions)
            total_versions = scenario + stable_list
            self._permutationsUsed[nBadVersions] = []
            # El iterador de versiones con n malas se guarda en _scenarioList
            self._scenarioList[nBadVersions] = permutations(list(total_versions), len(self.components))


    def getCompleteScenario(self, nBadVersions):
        if (not self._scenarioList[nBadVersions]):
            self.generateNextScenario(nBadVersions)
        scenario = None
        while scenario == None or scenario in self._permutationsUsed[nBadVersions]:
            try:
                scenario = self._scenarioList[nBadVersions].next()
        
            except StopIteration:
                self.generateNextScenario(nBadVersions)

        self._permutationsUsed[nBadVersions].append(scenario)            
        return scenario
    # Generate a new scenerarios
    def generateScenarios(self):
        scenarios = []
        nComponents = len(self.components)

        # times iterated
        times_iterated = 0
        while nComponents > times_iterated:
            # number of the bad/good versions required (n componentes - n times iterated)
            # 7 good 0 bad #### 7 bad 0 good
            # 6 good 1 bad #### 6 bad 1 good
            # 5 good 2 bad #### 5 bad 2 good
            # ....
            count = nComponents - times_iterated

            # Good scenarios
            good_versions = [None]*nComponents
            bad_versions = [None]*nComponents
            
            good_versions = self.getCompleteScenario(times_iterated)
            bad_versions = self.getCompleteScenario(count)

            scenarios.append(good_versions)
            scenarios.append(bad_versions)

            times_iterated += 1
          
        return scenarios

    def getNewVersions(self):
        lng = len(self.scenarios)
        versions = None
        if (self.times_called < lng):
            versions = self.scenarios[self.times_called]
        else:
            self.scenarios += self.generateScenarios()
            versions = self.scenarios[self.times_called]

        self.times_called += 1

        return versions
if __name__ == "__main__":
    components = ["twitter-timeline", "facebook-wall", "pinterest-timeline", "googleplus-timeline", "traffic-incidents", "finance-search", "open-weather"]
    versions = ["stable", "latency", "accuracy", "maintenance", "complexity", "structural"]

    bva = BVA(components, versions)
    scenarios = []
    
    for i in range(2500):
        scenarios.append(bva.getNewVersions())
    #     scenario = bva.getNewVersions()
    #     good = list(scenario).count('stable')
    #     if good == 6:
    #         print scenario

    for idx, scenario in enumerate(scenarios):
        repetidos = 0
        if scenario.count('stable') != 7 and scenario.count('stable') != 6:
            repetidos = (scenarios.count(scenario))

        if repetidos > 1:
            print idx, scenario