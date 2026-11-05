import heapq
heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 2)
print("最小值:", heapq.heappop(heap))
