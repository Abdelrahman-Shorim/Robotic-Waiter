import pygame
from queue import PriorityQueue
from spots import *



def BFS(draw, start, end):
	open_set = []
	open_set.append(start)
	came_from={}
	visited = {start}
	while open_set:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.pop(0)
		visited.add(current)
		if current == end:
			reconstruct_path(came_from,start, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			if neighbor not in came_from:
				came_from[neighbor]=current
			if neighbor not in visited:
					visited.add(neighbor)
					open_set.append(neighbor)
					neighbor.make_open()

		draw()

		if current != start :
			current.make_closed()

	return False


def Astar(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}
	while open_set.qsize()>0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from,start, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1
			
			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

def UCS(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0


	open_set_hash = {start}
	while open_set.qsize()>0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from,start, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((g_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

def GBFS(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())


	open_set_hash = {start}
	while open_set.qsize()>0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from,start, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = h(neighbor.get_pos(), end.get_pos())

			if temp_g_score < f_score[neighbor]:
				came_from[neighbor] = current
				f_score[neighbor] = temp_g_score
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

def DFS(draw, start, end):
	visited=[]
	parent = {}
	stack=[]
	stack.append(start)
	while stack:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		current=stack.pop()
		if current==end:
			reconstruct_path(parent,start, end, draw)
			end.make_end()
			return True
		if current not in visited:
			visited.append(current)
			for neighbor in current.neighbors:
				if neighbor not in visited:
					parent[neighbor]=current
					stack.append(neighbor)
					neighbor.make_open()

		draw()
		if current!=start:
			current.make_closed()
	return False
