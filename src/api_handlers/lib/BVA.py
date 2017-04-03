import random
import copy


class BVA(object):
    def __init__(self, components, versions, times_called=None):
        # INIT DEFAULT VALUES (Default values == [] is dangerous)
        self.components = components
        self.versions = versions
        self.times_called = 0
        self.v_component = []
        for _ in components:
          self.v_component.append(copy.copy(versions))
        self.combinations = self.generateCombinations()
        self.times_called = times_called or self.tiemes_called
    def restartValues(self):
        self.tiemes_called = 0
    
    def randomVersion(self, component):
        if len(self.v_component[component]) ==0:
            self.v_component[component] = copy.copy(self.versions)

        versions_component = self.v_component[component]
        version = random.choice(versions_component)
        self.v_component[component].remove(version)

        return version
    def generateCombinations(self):
        combinations = []
        nComponents = len(self.components)
        goodVersion = self.versions[0]
        nonGoodVersions = self.versions[1:]

        def randomBadVersions(component):
            versions_component = self.v_component[component]
            if "stable" in versions_component:
                versions_component.remove('stable')

            if len(versions_component) == 0:
              self.v_component[component] = copy.copy(self.versions)
              versions_component = self.v_component[component]


            version = random.choice(versions_component)
            self.v_component[component].remove(version)
            return version

        # times iterated
        times_iterated = 0
        while nComponents - times_iterated > 0:
            count = nComponents - times_iterated

            # Good combinations
            versions_position = list(range(nComponents))
            good_versions = [None]*nComponents
            bad_versions = [None]*nComponents

            for idx in range(nComponents):
                position = random.choice(versions_position)
                versions_position.remove(position)

                if idx < count:
                    good_versions[position] = goodVersion
                    bad_versions[position] = randomBadVersions(position)
                else:
                    good_versions[position] = randomBadVersions(position)
                    bad_versions[position] = goodVersion
            combinations.append(good_versions)
            combinations.append(bad_versions)

            times_iterated += 1
          
        return combinations

    def getNewVersions(self):
        lng = len(self.combinations)
        versions = None
        if (self.times_called < lng):
            versions = self.combinations[self.times_called]
        else:
            l = list(range(len(self.components)))
            versions = [self.randomVersion(i) for i in l]
        self.times_called += 1
        return versions