# Graham's Scan #
# Finding the convex hull of a finite set of points in the plane #
# Colby Timm #
# This script was written to demonstrate the Graham's scan in Python #

from collections import namedtuple  
import matplotlib.pyplot as plt  
import random
import math
import time

class grahams_scan(object):
	_points = []
	_graham_points = []
	Point = namedtuple('Point', 'x y slope length')

	def __init__(self):
		pass

	def add(self, point):
		self._points.append(point)
  
	def generate_points(self,num):
		for _ in range(num):
			x = random.uniform(1, 100)
			y = random.uniform(1, 100)
			slope = y/x
			length = math.sqrt(x**2+y**2)
			self.add(self.Point(x,y,slope,length))
		self._points.append(self._points[0])
		return self._points
    
	def ccw(self, p1, p2, p3):
	#Returns the orientation of the set of points. >0 if p1,p2,p3 are clockwise, <0 if counterclockwise, 0 if co-linear.
		return (p2.y - p1.y)*(p3.x - p1.x) - (p2.x - p1.x)*(p3.y - p1.y)

	def sort_points(self,points):
		def slope(y):
			x = points[0]
			return (x.y - y.y) / (x.x - y.x)

		points.sort() 
		points = points[:1] + sorted(points[1:], key=slope)
		return points

	def compute_grahams(self,num):
	# Compute the points for the Graham's Scan #
		points = self.generate_points(num)
		points = self.swap_y(points)
		N = len(points)
		start = points[0]
		end = points[N-1]
		sorted_points = self.sort_points(self._points)
		#self._graham_points.append(sorted_points[0])
		for p in sorted_points:
			while len(self._graham_points) > 1 and self.ccw(self._graham_points[-2], self._graham_points[-1], p) >= 0:
				self._graham_points.pop()
			self._graham_points.append(p)
		self._graham_points.append(sorted_points[0])
		return self._graham_points

	def swap_y(self,points):
		test = []
		for i in range(len(points)):
			test.append(points[i].length)

		min_index = test.index(min(test))
  
		if min_index != 0:
			temp = points[0]
			points[0] = points[min_index]
			points[min_index] = temp
		return points

	def x_y_coordinates(self,points):
		x_points = []
		y_points = []
		for i in range(len(points)):
			x_points.append(points[i].x)
			y_points.append(points[i].y)
		return x_points,y_points

	def plot(self,points,graham_points):
		if len(points) > 0 and len(graham_points) > 0:
			x_points,y_points = self.x_y_coordinates(points)
			x_points_g,y_points_g = self.x_y_coordinates(graham_points)
			plt.scatter(x_points,y_points,color='b')
			plt.scatter(x_points_g,y_points_g,color='r')
			plt.plot(x_points_g,y_points_g,color='r')
			plt.show()
		elif len(points) > 0:
			print('Error: Points Array is Empty.')
		elif len(graham_points) > 0:
			print('Error: Graham Points Array is Empty.')

	def length(self,points):
		length = 0
		for i in range(len(points)):
			length += math.sqrt(points[i].x**2+points[i].y**2)
		return length

def welcome():
	print('Welcome user. This simple script takes a set amount of random points and computes the Grahams Scan of them.')
	print('To learn more about the method of a Grahams Scan visit: https://en.wikipedia.org/wiki/Graham_scan')


def main():
	
	welcome()
	num = int(input('How many random points would you like to generate? --> '))
	start = time.time()
	gs = grahams_scan()
	graham_points = gs.compute_grahams(num)
	end = time.time()
	#print(end - start)

	length = int(gs.length(graham_points))
	print('The length of the perimeter is: %d' %length)
	points = gs._points
	gs.plot(points,graham_points)

if __name__ == '__main__':  
    main()



