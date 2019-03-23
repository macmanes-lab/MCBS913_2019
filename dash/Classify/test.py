
num = 5
class test:

     def __init__(self):
          print("this is init func")
          global num
          num += 10
          #print ("global num ",num)
          #test.num += 1
          #print("Class num ",test.num)
          self.num = 1

     def func(self):
          return self.num

     def add(self):
          self.num += 1


if __name__ == '__main__':
     t1 = test()
     t2 = test()

     print(t1.func())

     print(t2.func())