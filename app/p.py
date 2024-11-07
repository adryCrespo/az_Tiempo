# z = [("a",1),("b",2),("c",3)]
# x = [i[0] for i in z]
# y = [i[1] for i in z]
# print(x)
# print(y)

# print(*z)

from database_ops import DatabaseManager

ciudad = 'madrid'
dm = DatabaseManager()
result = dm.query_ciudad_db(ciudad)
print(result)
# xs, ys = zip(*result)
# print(xs)