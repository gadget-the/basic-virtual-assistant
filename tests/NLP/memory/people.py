import json

class Person:
	def __init__(self, typ, firstname, attr=None, value=None):
		self.typ = typ
		self.firstname = firstname
		self.attr = attr
		self.value = value
		with open('memory.json', 'r') as fp:
			self.people = json.load(fp)

		if value:
			print(self.change())
		else:
			print(self.check())

	def change(self):
		if self.firstname in self.people:
			if self.attr and self.value:
				if self.attr in self.people[self.firstname]:
					if type(self.people[self.firstname][self.attr]) == list:
						if type(self.value) == list:
							self.people[self.firstname][self.attr] += self.value
						else:
							self.people[self.firstname][self.attr].append(self.value)
					else:
						self.people[self.firstname][self.attr] = self.value
				else:
					self.people[self.firstname][self.attr] = self.value
		else:
			self.people[self.firstname] = {
				"type": self.typ,
				"firstname": self.firstname,
			}
			if self.attr and self.value:
				self.people[self.firstname][self.attr] = self.value

		with open("memory.json", "w") as fp:
			json.dump(self.people, fp)

		return self.attr, self.value

	def check(self):
		if self.people[self.firstname][self.attr]:
			return self.people[self.firstname][self.attr]

if __name__ == "__main__":
	# pers = Person("person", "Jamie", "pets")
	# pers = Person("person", "Jamie", "pets", "Mikey")
	# pers = Person("person", "Jamie", "nicknames")
	# pers = Person("person", "Jamie", "firstname")
	# pers = Person("person", "Jamie", "relationships", {"sister": "Edna"})
    print("toot")