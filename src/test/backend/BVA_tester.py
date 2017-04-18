import unittest
import sys
import copy
import pprint

BVA_FOLDER = '../../api_handlers/lib/'
sys.path.insert(1, BVA_FOLDER)
import BVA

class BVA_tester(unittest.TestCase):
    def setUp(self):
        self.components = ["twitter-timeline", "facebook-wall", "pinterest-timeline", "googleplus-timeline", "traffic-incidents", "finance-search", "open-weather"]
        self.versions = ["stable", "latency", "accuracy", "maintenance", "complexity", "structural"]


    def testInit(self):
        bva = BVA.BVA(self.components, self.versions)
        self.assertIsNotNone(bva, 'BVA is empty')
        self.assertEquals(bva.components, self.components,'Components are not stored correctly')
        self.assertEquals(bva.versions, self.versions,'Components are not stored correctly')
        self.assertEquals(bva.times_called, 0, 'Times called must be 0')
        self.assertIsNotNone(bva.combinations,'Combinations are empty')
  
    def testCombinations(self):
        bva = BVA.BVA(self.components, self.versions)

        total = len(self.components)
        current=0

        while(current<total):
          
            # Check good versions
            goodVersions = bva.getNewVersions()

            #print goodVersions
            good = goodVersions.count('stable')
            self.assertEquals(good, total-current, 'Stable versions must be ' + str(total-current) + ' and there are ' + str(good) + ' on good test' )
            # Check bad versions
            badVersions = bva.getNewVersions()
            #print badVersions
            bad = badVersions.count('stable')
            self.assertEquals(bad, current, 'Stable versions must be ' + str(current) + ' and there are ' + str(bad) + ' on bad test')
            current+=1
  
    def testResetCount(self):
        bva = BVA.BVA(self.components, self.versions)
        bva.getNewVersions()
        self.assertEquals(bva.times_called, 1, 'Times_called is not 1')

        bva.restartValues()
        self.assertEquals(bva.times_called,0,'Times_called is not 0')
    
    def checkDistribution(self):
        times= 30
        bva = BVA.BVA(self.components, self.versions)
        # Test no repeat versions
        base={}
        count_versions=[]
        for el in self.versions:
            base[el] = 0
        for _ in self.components:
          count_versions.append(copy.copy(base))

        for _ in range(times):
            versions = bva.getNewVersions()
            for idx, version in enumerate(versions):
              count_versions[idx][version] +=1
        
        # Check distribution
        for element in count_versions:
            del element[self.versions[0]]
            distribution = [element[version] for version in element]
            minimum = min(distribution)
            maximum = max(distribution)
            self.assertTrue(abs(maximum-1)<2, 'Wrong distribution of "bad" versions')

if __name__ == '__main__':
    unittest.main()