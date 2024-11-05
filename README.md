# Installation
- [Install](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/) MySQL and create local connection instance.
- Clone this repo
```
git clone https://github.com/Felix-Zhenghao/robotDB.git
cd robotDB
```
- Install python package dependencies
```
pip install -r requirements.txt
```
- Checkout robosuite `v1.4.1` to avoid import error
```
cd robosuite
git checkout v1.4.1
```
- Check your installation
```
TODO
```


# Method to store `np.ndarray` into MySQL and read it
The key idea is to use BLOB type in MySQL and store the shape of the array as well.

```python
import pymysql.cursors
import numpy as np

x = np.random.rand(5, 3)

# connect to the local MySQL
connection = pymysql.connect(host = 'localhost',
                             user = 'root',
                             database = None,
                             cursorclass = pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS testdb") # create testdb dataset
        cursor.execute("USE testdb")
    connection.commit()

    with connection.cursor() as cursor:
        # create relation, array has type BLOB
        cursor.execute("CREATE TABLE IF NOT EXISTS NumpyTest (testID INT, array BLOB, shape0 INT, shape1 INT)")
    connection.commit()

    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO NumpyTest (testID, array, shape0, shape1) VALUES (1, %s, {x.shape[0]}, {x.shape[1]})", (x,))
    connection.commit()

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM NumpyTest")
        result = cursor.fetchall()
    connection.commit()


array = result[-1]['array'].decode('utf-8')
array = ' '.join(re.findall(r'\d+\.\d+', array))
print(np.fromstring(array, sep=' ').reshape(result[-1]['shape0'], result[-1]['shape1']))
# [[0.14459953 0.41180245 0.14350818]
#  [0.74690602 0.39687072 0.85921284]
#  [0.09498237 0.0326718  0.14720057]
#  [0.64451626 0.95533431 0.26276553]
#  [0.22059957 0.59640218 0.05554185]]
```

