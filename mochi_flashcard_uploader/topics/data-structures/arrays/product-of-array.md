## Card 1

What is the "Product of Array Except Self" problem and why is it significant?

---

- Given array nums[], return array output[] where output[i] = product of all elements except nums[i]
- Significant because it tests multiple concepts:
  1. Array manipulation
  2. Space optimization
  3. Prefix/Suffix patterns
  4. Handling edge cases (zeros)
- Must solve without using division
- Real-world analogy: Like calculating total group productivity if each person took a day off

## Card 2

Write a basic solution using two arrays (left and right products):

---

```python
def productExceptSelf(nums: list[int]) -> list[int]:
    n = len(nums)
    left_products = [1] * n  # Products of all elements to the left
    right_products = [1] * n  # Products of all elements to the right

    # Build left products
    for i in range(1, n):
        left_products[i] = left_products[i-1] * nums[i-1]

    # Build right products
    for i in range(n-2, -1, -1):
        right_products[i] = right_products[i+1] * nums[i+1]

    # Combine left and right products
    return [left_products[i] * right_products[i] for i in range(n)]
```

## Card 3

How do you optimize the space complexity to O(1) (excluding output array)?

---

```python
def productExceptSelf(nums: list[int]) -> list[int]:
    n = len(nums)
    output = [1] * n

    # Left pass
    left_product = 1
    for i in range(n):
        output[i] = left_product
        left_product *= nums[i]

    # Right pass
    right_product = 1
    for i in range(n-1, -1, -1):
        output[i] *= right_product
        right_product *= nums[i]

    return output
```

Key insights:

- Use output array to store left products
- Use single variable for right products
- Combine in second pass

## Card 4

Trace this algorithm for input [1,2,3,4]. Show each step:

---

Initial array: [1,2,3,4]

Left pass:

1. output = [1] → [1,1,1,1]
2. After i=0: [1,1,1,1], left_product = 1\*1 = 1
3. After i=1: [1,1,1,1], left_product = 1\*2 = 2
4. After i=2: [1,2,2,2], left_product = 2\*3 = 6
5. After i=3: [1,2,6,6], left_product = 6\*4 = 24

Right pass:

1. right_product starts as 1
2. After i=3: [1,2,6,6], right_product = 1\*4 = 4
3. After i=2: [1,2,6,24], right_product = 4\*3 = 12
4. After i=1: [1,2,24,24], right_product = 12\*2 = 24
5. After i=0: [24,12,8,6]

Final result: [24,12,8,6]

## Card 5

How do you handle arrays containing zeros?

---

Three cases to consider:

1. No zeros in array:

   - Standard approach works

2. One zero in array:
   - All positions except zero's position will be 0
   - Zero's position gets product of all other numbers

```python
def productExceptSelfWithZero(nums: list[int]) -> list[int]:
    zero_count = nums.count(0)
    if zero_count > 1:
        return [0] * len(nums)

    total_product = 1
    zero_index = -1

    for i, num in enumerate(nums):
        if num == 0:
            zero_index = i
            continue
        total_product *= num

    result = [0] * len(nums)
    if zero_index != -1:
        result[zero_index] = total_product
    return result
```

3. More than one zero:
   - All positions will be 0

## Card 6

What are common follow-up questions for this problem?

---

1. What if division is allowed?

   ```python
   def productExceptSelfWithDivision(nums: list[int]) -> list[int]:
       total_product = 1
       zero_count = 0

       for num in nums:
           if num == 0:
               zero_count += 1
               continue
           total_product *= num

       result = []
       for num in nums:
           if zero_count > 1:
               result.append(0)
           elif zero_count == 1:
               result.append(total_product if num == 0 else 0)
           else:
               result.append(total_product // num)
       return result
   ```

2. What if numbers can be negative?

   - Solution remains same, handles negatives automatically

3. How to handle integer overflow?
   - Use mod operation if required
   - Consider using log and exp for very large numbers

## Card 7

Debug this implementation. What's wrong?

```python
def productExceptSelf(nums):
    n = len(nums)
    output = [1] * n
    left = right = 1

    for i in range(n):
        output[i] *= left
        left *= nums[i]
        output[i] *= right
        right *= nums[n-1-i]

    return output
```

---

Two bugs:

1. Multiplying by both left and right in same iteration
2. Using wrong indices for right product

Correct implementation:

```python
def productExceptSelf(nums):
    n = len(nums)
    output = [1] * n

    left = 1
    for i in range(n):
        output[i] = left
        left *= nums[i]

    right = 1
    for i in range(n-1, -1, -1):
        output[i] *= right
        right *= nums[i]

    return output
```
