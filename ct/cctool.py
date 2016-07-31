# -*- coding: utf-8 -*-
"""
Created on Sun Apr 03 10:41:17 2016

@author: User
"""

import doctest
import itertools 
import unittest


class ct():
  """
  ct is tool class!
  """
  
  def __init__(self):  
    pass  
      
  @staticmethod
  def list2str(lst1D):
      """
      这个函数将传入的�?维列表合并成字符串，并去掉两边空格后添加[]并返回�??
      
      >>> ct.list2str(123)
      ''
      
      >>> ct.list2str(['1','2','3'])
      '[123]'
      
      >>> ct.list2str(False)
      ''
    
      如果是一个非@staticmethod函数，那么直�?'>>> func1()',无需'>>> ct.func1()'
      
      """
      if isinstance(lst1D, list):
        return  "[" + "".join(itertools.chain(*lst1D)).strip() + "]"
      else:
        return ''   



      
class ctTest(unittest.TestCase):
    """
    test case for class 'ct'
    """

    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_list2str_iptlist(self):
        text = ['1', '2', '3']
        result = ct.list2str(text)
        self.assertEqual(result, '[123]')
        
    def test_list2str_iptint(self):
        i = 123
        result = ct.list2str(i)
        self.assertEqual(result, '')

       
#Below line MUST BE START AT FIRST COL!!!!!!!!!!!!!!!!!!!!!!!!!  
def main():
    print 'Run to ctTest.main()'
    pass


#Below line MUST BE START AT FIRST COL!!!!!!!!!!!!!!!!!!!!!!!!!    
if __name__ == '__main__':  
  main()


  print '###Use unittest### ----- ENTER'
  # unittest.main()  #执行后会�?出，�?以必须放在最后！！！
  
  # Below 2 lines instead of "unittest.main()", and OUTPUT DETAIL TEST CASE INFO!
  suite = unittest.TestLoader().loadTestsFromTestCase(ctTest)
  unittest.TextTestRunner(verbosity=2).run(suite)
  print '###Use unittest### ----- LEAVE'
  
  print '###Use doctest### ----- ENTER'
  # import doctest
  doctest.testmod(verbose=True)
  print '###Use doctest### ----- LEAVE'


  
      
        
