"""
Part of an excercise to learn about dynamic programming
I wanted to see if I could beat the recursion limit by replacing recursion with manageing my own stack.

Based on these 2 articles
http://stupidpythonideas.blogspot.com/2014/10/how-do-i-make-recursive-function.html
https://blog.moertel.com/posts/2013-05-11-recursive-to-iterative.html

It's possible but not very practical.

Future project: 
Could we write a decorator to do this transform automatically?
Or maybe this is better handled at the interpreter level (e.g. stackless python)
"""

from functools import lru_cache
from collections import namedtuple
import enum

denom = [1, 3, 4]

# recursion
# highest: 30
def coins(n):
	ans = float("inf")
	if n <= 0:
		return 0
	for coin in denom:
		ans = min(ans, 1 + coins(n-coin))
	return ans

# cache
# highest: 550
# recusion limit -- possibly half of recursion limit due to function from decorator
@lru_cache
def coins(n):
	ans = float("inf")
	if n <= 0:
		return 0
	for coin in denom:
		ans = min(ans, 1 + coins(n-coin))
	return ans

# dynamic programming
# use list instead of dict
# highest: 995 -- recursion limit is 1000
# increasing recursion limit causes segfault somewhere between 1e4 - 1e5
def coins(n):
	dp = [None] * (n+1)
	return coins_(n, dp)

def coins_(n, dp):
	ans = float("inf")
	if dp[n] is not None:
		return dp[n]
	if n <= 0:
		return 0
	for coin in denom:
		ans = min(ans, 1 + coins_(n-coin, dp))
	dp[n] = ans
	return ans

# iterative
# start by creating a state machine
# ask yourself: where am I popping, where am I pushing?
# max: 30
class Locals:
	__slot__ = ['n', 'ans', 'idx']
	def __init__(self, n, ans=float('inf'), idx=0):
		self.n = n
		self.ans = ans
		self.idx = idx
	
	def __repr__(self):
		return f"Locals(n={self.n}, ans={self.ans}, idx={self.idx})"


State = enum.Enum('State', 'start loop checkmin')
def coins(n):
	stack = []
	state = State.start
	
	stack.append(Locals(n))
	
	# registers
	retval = None
	
	while stack:
		#input()
		#print(f"{state : <15}{stack[-1]}")
		locals = stack[-1]
		if state == State.start:
			if locals.n <= 0:
				stack.pop()
				retval = 0
				state = state.checkmin
				continue
			state = State.loop
			continue
		elif state == State.loop:
			if locals.idx == len(denom):
				stack.pop()
				retval = locals.ans
				state = State.checkmin
				continue
			stack.append(Locals(locals.n-denom[locals.idx]))
			state = State.start
			continue
		elif state == State.checkmin:
			locals = stack[-1]
			locals.ans = min(locals.ans, retval+1)
			locals.idx += 1
			state = State.loop
			continue
	return retval

# iterative + dp
# max 1e6, 1e7 slow but do-able
# 1e7 uses about 2GB of memory
def coins(n):
	dp = [-1] * (n+1)
	dp[0] = 0
	stack = []
	state = State.start
	
	stack.append(Locals(n))
	
	# registers
	retval = None
	
	while stack:
		#input()
		#print(f"{state : <15}{stack[-1]}")
		locals = stack[-1]
		if state == State.start:
			if dp[locals.n] != -1:
				stack.pop()
				retval = dp[locals.n]
				state = state.checkmin
				continue
			if locals.n <= 0:
				stack.pop()
				retval = 0
				state = state.checkmin
				continue
			state = State.loop
			continue
		elif state == State.loop:
			if locals.idx == len(denom):
				stack.pop()
				retval = locals.ans
				state = State.checkmin
				dp[locals.n] = retval
				continue
			stack.append(Locals(locals.n-denom[locals.idx]))
			state = State.start
			continue
		elif state == State.checkmin:
			locals = stack[-1]
			locals.ans = min(locals.ans, retval+1)
			locals.idx += 1
			state = State.loop
			continue
	return retval

assert coins(10) == 3
