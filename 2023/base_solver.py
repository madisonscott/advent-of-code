from abc import ABC, abstractmethod

class BaseSolver(ABC):
  @abstractmethod
  def solve_part_one(self, input):
    pass

  @abstractmethod
  def solve_part_two(self, input):
    pass

  @property
  @abstractmethod
  def test_input_one(self):
    pass

  def test_input_two(self):
    return self.test_input_one()