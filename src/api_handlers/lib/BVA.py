import random
import copy
from itertools import permutations

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
        for idx in range(len(components)+1):
            self._permutationList.append(self.generatePermutation(idx))
        self._countUsed = [0]* (len(self.components) + 1)

        self._scenarioList = [False]*(len(self.components) +1)
        # Predefined scenarios
        self._endPredefined = 0
        self.scenarios = self.generateScenarios()

    # Reset the times called without reset list of scenarios generated
    def restartValues(self):
        self.times_called = 0
    
    def generatePermutation(self, number):
        _versions = self.bad_versions
        if number > len(self.bad_versions):
            _versions = self.bad_versions + self.bad_versions
        return permutations(_versions, number)


    # Genera iterador para coger scenarios con n versiones malas. Si se acaban vuelve a coger mas
    def generateNextScenario(self, nBadVersions):
        try:
            scenario = ()
            if nBadVersions !=0:
                scenario = self._permutationList[nBadVersions].next()
            stable_list = [self.good_version] * (len(self.components) - nBadVersions)
            total_versions = list(scenario) + stable_list
            self._scenarioList[nBadVersions] = permutations(list(total_versions), len(self.components))

        # Si no hay mas permutaciones se vuelven a generar
        except StopIteration:
            self._permutationList[nBadVersions] = self.generatePermutation(nBadVersions)
            stable_list = [self.good_version] * (len(self.components) - nBadVersions)
            total_versions = list(scenario) + stable_list
            # El iterador de versiones con n malas se guarda en _scenarioList
            self._scenarioList[nBadVersions] = permutations(list(total_versions), len(self.components))


    def getCompleteScenario(self, nBadVersions):
        if (not self._scenarioList[nBadVersions]):
            self.generateNextScenario(nBadVersions)
        try:
            return self._scenarioList[nBadVersions].next()
        except StopIteration:
            self.generateNextScenario(nBadVersions)
            return self._scenarioList[nBadVersions].next()

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
            self.scenarios += self.generateScenarios()[1:]
            versions = self.scenarios[self.times_called]

        self.times_called += 1

        return versions
if __name__ == "__main__":
    components = ["twitter-timeline", "facebook-wall", "pinterest-timeline", "googleplus-timeline", "traffic-incidents", "finance-search", "open-weather"]
    versions = ["stable", "latency", "accuracy", "maintenance", "complexity", "structural"]

    bva = BVA(components, versions)
    scenarios = []
    
    for i in range(10):
        scenarios.append(bva.getNewVersions())

    for idx, scenario in enumerate(scenarios):
        repetidos = (scenarios.count(scenario))

        if repetidos > 1:
            print idx, scenario