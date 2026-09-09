"""
Shape & Volume Hierarchy (Single Inheritance in Python)
Author: Shaurya Bhatia (Bennett University)
--------------------------------------------------------------------------------
Demonstrates:
- Base class (Shape) with length and width
- Derived class (ChildShape / 3D Prism) inheriting Shape attributes and methods
- Volume calculation leveraging base class area calculation
"""

class Shape:
    """Base class representing a 2D rectangular shape."""
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def showData(self):
        print('Length is:', self.length)
        print('Width is:', self.width)

    def getArea(self):
        """Calculates and returns base area (length * width)."""
        return self.length * self.width

    # Kept for backward compatibility with classroom method name
    def getCal(self):
        return self.getArea()


class ChildShape(Shape):
    """Derived 3D shape class extending Shape with height and volume."""
    def __init__(self, length, width, height):
        # Initialize base class attributes using super()
        super().__init__(length, width)
        self.height = height
        self.volume = 0

    def calVolume(self):
        """Computes volume by multiplying base area by height."""
        self.volume = self.getArea() * self.height
        return self.volume

    def displayData(self):
        """Displays dimension data and calculated 3D volume."""
        self.showData()
        print("Height is:", self.height)
        print("Volume is:", self.volume)
        print('=' * 50)


if __name__ == "__main__":
    print("--- 3D Shape Inheritance Demonstration ---")
    prism = ChildShape(2, 3, 4)
    prism.calVolume()
    prism.displayData()
