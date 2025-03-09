import random
import time
from functools import lru_cache


N = 100_000
array = [random.randint(1, 1000) for _ in range(N)]

Q = 50_000
queries = []
for _ in range(Q):
    if random.random() < 0.7:
        L, R = sorted(random.sample(range(N), 2))
        queries.append(("Range", L, R))
    else:
        index = random.randint(0, N - 1)
        value = random.randint(1, 1000)
        queries.append(("Update", index, value))


def range_sum_no_cache(array, L, R):
    return sum(array[L : R + 1])


def update_no_cache(array, index, value):
    array[index] = value


CACHE_SIZE = 1000


@lru_cache(maxsize=CACHE_SIZE)
def range_sum_with_cache(L, R):
    return sum(array[L : R + 1])


def update_with_cache(array, index, value):
    array[index] = value
    range_sum_with_cache.cache_clear()


print("Запуск тестування без кешу...")
start = time.time()
for query in queries:
    if query[0] == "Range":
        range_sum_no_cache(array, query[1], query[2])
    else:
        update_no_cache(array, query[1], query[2])
end = time.time()
time_no_cache = end - start
print(f"Час виконання без кешування: {time_no_cache:.2f} секунд")

print("Запуск тестування з LRU-кешем...")
start = time.time()
for query in queries:
    if query[0] == "Range":
        range_sum_with_cache(query[1], query[2])
    else:
        update_with_cache(array, query[1], query[2])
end = time.time()
time_with_cache = end - start
print(f"Час виконання з LRU-кешем: {time_with_cache:.2f} секунд")

if time_with_cache < time_no_cache:
    speed_up = time_no_cache / time_with_cache
    print(f"Кеш працює у {speed_up:.2f} рази швидше!")
else:
    print("Кеш не показав кращу швидкість!")