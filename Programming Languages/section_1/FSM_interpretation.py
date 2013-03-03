# FSM Interpretation 1

# Define edges and accepting to encode r"q*". Name your start state 1.

edges = {(1, 'q'): 1}

accepting = [1]


def fsmsim(string, current, edges, accepting):
	if string == "":
		return current in accepting
	else:
		letter = string[0]
		if (current, letter) in edges:
			destination = edges[(current, letter)]
			remaining_string = string[1:]
			return fsmsim(remaining_string, destination, edges, accepting)
		else:
			return False


print fsmsim("",1,edges,accepting)
# >>> True

print fsmsim("q",1,edges,accepting)
# >>> True

print fsmsim("qq",1,edges,accepting)
# >>> True

print fsmsim("p",1,edges,accepting)
# >>> False

# FSM Interpretation 2

# Define edges and accepting to encode r"[a-b][c-d]?". Name your start state 1.

edges = {(1, 'a'): 2,
		 (1, 'b'): 2,
		 (2, 'c'): 3,
		 (2, 'd'): 3}

accepting = [2, 3]


def fsmsim(string, current, edges, accepting):
	if string == "":
		return current in accepting
	else:
		letter = string[0]
		if (current, letter) in edges:
			destination = edges[(current, letter)]
			remaining_string = string[1:]
			return fsmsim(remaining_string, destination, edges, accepting)
		else:
			return False


print fsmsim("a",1,edges,accepting)
# >>> True

print fsmsim("b",1,edges,accepting)
# >>> True

print fsmsim("ad",1,edges,accepting)
# >>> True

print fsmsim("e",1,edges,accepting)
# >>> False


# FSM Interpretation 3

# Provide s1 and s2 that are both accepted, but s1 != s2.

s1 = "bdf"

s2 = "bdgbdf"


edges = {(1,'a') : 2,
		 (1,'b') : 3,
		 (2,'c') : 4,
		 (3,'d') : 5,
		 (5,'c') : 2,
		 (5,'f') : 6,
		 (5,'g') : 1}

accepting = [6]


def fsmsim(string, current, edges, accepting):
	if string == "":
		return current in accepting
	else:
		letter = string[0]
		if (current, letter) in edges:
			destination = edges[(current, letter)]
			remaining_string = string[1:]
			return fsmsim(remaining_string, destination, edges, accepting)
		else:
			return False


print fsmsim(s1,1,edges,accepting)
# >>> True

print fsmsim(s2,1,edges,accepting)
# >>> True

print s1 != s2
# >>> True
