(http://arogozhnikov.github.io/2015/09/29/NumpyTipsAndTricks1.html)
(http://arogozhnikov.github.io/2015/09/30/NumpyTipsAndTricks2.html)

```python
import numpy as np
```

1. Sorting values of one array according to the other.
```python
ages = np.random.randint(low=30, high=60, size=10)
heights = np.random.randint(low=150, high=210, size=10)

sorter = np.argsort(ages)
print(ages[sorter])
print(heights[sorter])
```
Frequently to solve this problem people use 'sorted(zip(ages, heights))', which is much slower (10-20 times slower on large arrays).

<br>
2. Computing inverse of permutation.

```python
permutation = np.random.permutation(10)
inverse_permutation = np.argsort(permutation)
```

Even faster inverse permutation
```python
inverse_permutation = np.empty(len(permutation), dtype=np.int)
inverse_permutation[permutation] = np.arange(len(permutation))
```

<br>
3. Computing order of elements in array.

```python
data = np.random.random(10)
print(data)
print(np.argsort(np.argsort(data)))
```

In fact, there is a more general and faster method with scipy.
```python
from scipy.stats import rankdata
rankdata(data) - 1
```

<br>
4. Weighted covariation matrix.

$cov = \sum_{i} w_{i} X_{i}^{T} X_{i}$

```python
data = np.random.normal(size=[100, 5])
weights = np.random.random(100)

def covariation(data, weights):
    weights = weights / weights.sum()
    return data.T.dot(weights[:, np.newaxis] * data)

np.cov(data.T)
covariation(data, np.ones(len(data)))

covariation(data, weights)
np.einsum('ij, ik, i -> jk', data, data, weights / weights.sum())
```

<br>
5. Pearson coefficient.

```python
np.corrcoef(data.T)

def my_corrcoef(data, weights):
    data = data - np.average(data, axis=0, weights=weights)
    shifted_cov = covariation(data, weights)
    cov_diag = np.diag(shifted_cov)
    return shifted_cov / np.sqrt(cov_diag[:, np.newaxis] * cov_diag[np.newaxis, :])

my_corrcoef(data, np.ones(len(data)))
```

<br>
6. Pairwise distances between vectors.

```python
X = np.random.normal(size=[1000, 100])
distances = ((X[:, np.newaxis, :] - X[np.newaxis, :, :]) ** 2).sum(axis=2) ** 0.5

products = X.dot(X.T)
distances2 = products.diagonal()[:, np.newaxis] + products.diagonal()[np.newaxis, :]  - 2 * products
distances2 **= 0.5
```

<br>
7. np.unique and np.searchsorted

```python
from itertools import combinations
possible_categories = list(map(lambda x: x[0] + x[1], list(combinations('abcdefghijklmn', 2))))
categories = np.random.choice(possible_categories, size=10000)
print(categories)

unique_categories, new_categories = np.unique(categories, return_inverse=True)
print(unique_categories[new_categories])


categories2 = np.random.choice(possible_categories, size=10000)
new_categories2 = np.searchsorted(unique_categories, categories2)
print(categories2)
print(unique_categories[new_categories2])
```

<br>
8. Checking values present in the lookup.

Usually, we use set to have many checks that each element exists in array. But numpy.unique is better option - it works dozens times faster.

```python
np.in1d(['ab', 'ac', 'something new'], unique_categories)
```

<br>
9. Rolling window, strided tricks.

```python
sequence = np.random.normal(size=10000) + np.arange(10000)

def running_average_simple(seq, window=100):
    result = np.zeros(len(seq) - window + 1)
    for i in range(len(result)):
        result[i] = np.mean(seq[i:i + window])
    return result

running_average_simple(sequence)
```

better method is to use as_strided

```python
from numpy.lib.stride_tricks import as_strided
def running_average_strides(seq, window=100):
    stride = seq.strides[0]
    sequence_strides = as_strided(seq, shape=[len(seq) - window + 1, window], strides=[stride, stride])
    return sequence_strides.mean(axis=1)

running_average_strides(sequence)
```

However the right way is using np.cumsum

```python
def running_average_cumsum(seq, window=100):
    s = np.insert(np.cumsum(seq), 0, [0])
    return (s[window :] - s[:-window]) * (1. / window)

running_average_strides(sequence)
```

_Remark_: for computing rolling mean, numpy.cumsum is best, however for other window statistics like min/max/percentile, use strides trick.

<br>
10. as_strided

```python
window = 10
rates = np.random.normal(size=1000)

stride, = rates.strides
X2 = as_strided(rates, [len(rates) - window , window], strides=[stride, stride])
```

another sample:
```python
def compute_window_mean_and_var(image, window_w, window_h):
    w, h = image.shape
    w_new, h_new = w - window_w + 1, h - window_h + 1
    means = np.zeros([w_new, h_new])
    maximums = np.zeros([w_new, h_new])
    variations = np.zeros([w_new, h_new])
    for i in range(w_new):
        for j in range(h_new):
            window = image[i:i+window_w, j:j+window_h]
            means[i, j] = np.mean(window)
            maximums[i, j] = np.max(window)
            variations[i, j] = np.var(window)
    return means, maximums, variations


def compute_window_mean_and_var_strided(image, window_w, window_h):
    w, h = image.shape
    strided_image = np.lib.stride_tricks.as_strided(image,
                                                    shape=[w - window_w + 1, h - window_h + 1, window_w, window_h],
                                                    strides=image.strides + image.strides)
    means = strided_image.mean(axis=(2,3))
    mean_squares = (strided_image ** 2).mean(axis=(2, 3))
    maximums = strided_image.max(axis=(2,3))

    variations = mean_squares - means ** 2
    return means, maximums, variations

image = np.random.random([500, 500])

%time a1, b1, c1 = compute_window_mean_and_var(image, 20, 20)
# CPU times: user 9.83 s, sys: 172 ms, total: 10 s
# Wall time: 9.87 s

%time a2, b2, c2 = compute_window_mean_and_var_strided(image, 20, 20)
# CPU times: user 464 ms, sys: 36 ms, total: 500 ms
# Wall time: 497 ms

np.allclose(a1, a2), np.allclose(b1, b2), np.allclose(c1, c2)
# (True, True, True)
```

<br>
11. Masked arrays

```python
houses_prices = np.random.exponential(size=10000)
max_price = np.percentile(houses_prices, 95)
max_price
n_neighs = 20
position_neighbours = np.random.randint(0, len(houses_prices), size=[100000, n_neighs])

data = houses_prices[position_neighbours]
ignored = houses_prices[position_neighbours] > max_price
masked_prices = np.ma.MaskedArray(data=data, mask=ignored)

np.array(masked_prices.mean(axis=1))
```

<br>
12. numpy.ufunc.at & numpy.ufunc.reduceat

```python
salaries = np.random.random(2000)
programers = np.sort(np.random.randint(0, len(salaries), size=10000))
languages = np.random.randint(0, 50, size=len(programers))

#
lang_average_salaries = np.bincount(languages, salaries[programers]) / np.bincount(languages)

#
programmer_top_salary = np.zeros(programers.max() + 1)
np.maximum.at(programmer_top_salary, programers, lang_average_salaries[languages])
programmer_top_salary
#
lang_sorter = np.argsort(lang_average_salaries)
lang_salaries_ordered = np.argsort(lang_sorter)

programmer_top_language = np.zeros(programers.max() + 1, dtype=int)
np.maximum.at(programmer_top_language, programers, lang_salaries_ordered[languages])

programmer_top_language = lang_sorter[programmer_top_language]

lang_average_salaries[programmer_top_language]
# For programers with no languages, their 'top language' became the worst payed one, while the last method were zero.

# faster way
sorter = np.argsort(programers)
ordered_programers = programers[sorter]
ordered_languages = languages[sorter]

limits_in_programmers = np.insert(np.bincount(programers).cumsum()[:-1], 0, [0])
programmer_top_salary = np.maximum.reduceat(lang_average_salaries[ordered_languages], limits_in_programmers)
```

<br>
13. Multidimensional statistics
Compute number of times each combination met:

```python
first_category = np.random.randint(0, 100, 10000)
second_category = np.random.randint(0, 100, 10000)

counters = np.zeros([first_category.max() + 1, second_category.max() + 1])
np.add.at(counters, [first_category, second_category], 1)

# occurences of second category
counters.sum(axis=0)[second_category]

# maximal occurences of second category with same value of first category
counters.max(axis=0)[second_category]
```

<br>
14. Counter

```python
new_categories = np.random.randint(0, 100, 10000)
np.bincount(new_categories)
np.bincount(new_categories)[new_categories]

predictions = np.random.normal(size=len(new_categories))
means_over_category = np.bincount(new_categories, weights=predictions) / np.bincount(new_categories)
means_over_category[new_categories]
```

<br>
15. One-hot Embedding

```python
one_hot = np.eye(new_categories.max() + 1)[new_categories]
np.allclose(np.argmax(one_hot, axis=1), new_categories)
```
