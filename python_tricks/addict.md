<https://github.com/mewwts/addict>

addict is a Python module that gives you dictionaries whose values are both gettable and settable using attributes, in addition to standard item-syntax.

```Python
from addict import Dict
```

<br>
1.
Use:

```Python
body = Dict()
body.query.filtered.query.match.description = 'addictive'
body.query.filtered.filter.term.created_by = 'Mats'
```

instead of:

```python
body = {
    'query': {
        'filtered': {
            'query': {
                'match': {'description': 'addictive'}
            },
            'filter': {
                'term': {'created_by': 'Mats'}
            }
        }
    }
}
```

<br>
2. mix the two syntaxes:

```Python
addicted = Dict()
addicted.a.b.c.d.e = 2
addicted[2] = [1, 2, 3]
# {2: [1, 2, 3], 'a': {'b': {'c': {'d': {'e': 2}}}}}

addicted.a.b['c'].d.e
# 2
```

<br>
3. Counting

```Python
data = [
    {'born': 1980, 'gender': 'M', 'eyes': 'green'},
    {'born': 1980, 'gender': 'F', 'eyes': 'green'},
    {'born': 1980, 'gender': 'M', 'eyes': 'blue'},
    {'born': 1980, 'gender': 'M', 'eyes': 'green'},
    {'born': 1980, 'gender': 'M', 'eyes': 'green'},
    {'born': 1980, 'gender': 'F', 'eyes': 'blue'},
    {'born': 1981, 'gender': 'M', 'eyes': 'blue'},
    {'born': 1981, 'gender': 'F', 'eyes': 'green'},
    {'born': 1981, 'gender': 'M', 'eyes': 'blue'},
    {'born': 1981, 'gender': 'F', 'eyes': 'blue'},
    {'born': 1981, 'gender': 'M', 'eyes': 'green'},
    {'born': 1981, 'gender': 'F', 'eyes': 'blue'}
]

counter = Dict()

for row in data:
    born = row['born']
    gender = row['gender']
    eyes = row['eyes']

    counter[born][gender][eyes] += 1
print(counter)
# {1980: {'M': {'blue': 1, 'green': 3}, 'F': {'blue': 1, 'green': 1}},
#  1981: {'M': {'blue': 2, 'green': 1}, 'F': {'blue': 2, 'green': 1}}}
```

<br>
4. update

```Python
D = Dict({'a': {'b': 3}})
D.update({'a': {'c': 4}})
print(D)
# {'a': {'b': 3, 'c': 4}}
```

----
_Notes_:
<br>
5.
```Python
b = [1, 2, 3]
mapping = {'a': b}

d1 = Dict()
d1.a = b
d1.a is b
# True

d2 = Dict(mapping)
d2.a is b
# False
```

<br>
6. to_dict

```Python
regular_dict = my_addict.to_dict()
```

<br>
7. As it is a dict, it will serialize into JSON perfectly.
