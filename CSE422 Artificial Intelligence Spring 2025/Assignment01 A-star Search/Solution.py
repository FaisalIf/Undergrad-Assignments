import heapq as hq


def take_input(inp):

   city_list = []
   city = inp.readline()

   while city:
      city_list.append(city.split())
      city = inp.readline()

   return city_list


def create_graph(city_list):

   graph = {}

   for city in city_list:
      graph[city[0]] = [int(city[1]), []]

      for i in range(2, len(city), 2):
         neighbor = city[i]
         cost = int(city[i+1])
         graph[city[0]][1].append((neighbor, cost))

   return graph


def set_values(graph):

   f_n = {}
   dist = {}
   visited = {}
   parent = {}

   for i in graph.keys():
      f_n[i] = float('inf')
      dist[i] = float('inf')
      visited[i] = 0
      parent[i] = None

   return f_n, dist, visited, parent


def a_star(graph, source, dest, f_n, dist, visited, parent):

   f_n[source] = graph[source][0]
   dist[source] = 0
   pq = [(graph[source][0], source)]

   while pq:
      f, u = hq.heappop(pq)

      if u == dest:
         break

      if visited[u] == 1:
         continue
      visited[u] = 1

      for v, cost in graph[u][1]:

         if dist[v] > dist[u] + cost:
            parent[v] = u
            dist[v] = dist[u] + cost
            f_n[v] = dist[v] + graph[v][0]
            hq.heappush(pq, (f_n[v], v))
      
   return f_n, dist, visited, parent


def print_values(dist, parent, dest):

   if parent[dest] == None:
      print('NO PATH FOUND')
      return

   path = ''
   current_city = dest

   while current_city != None:
      path = ' -> ' + current_city + path
      current_city = parent[current_city]
   path = path[4::]
   
   print(f'Path: {path}\n'
         f'Total distance: {dist[dest]} km')



inp = open('Input file.txt','r')
graph = create_graph(take_input(inp))
f_n, dist, visited, parent = set_values(graph)
f_n, dist, visited, parent = a_star(graph, 'Arad', 'Bucharest', f_n, dist, visited, parent)
print_values(dist, parent, 'Bucharest')