### SCPE Spring 2025

## Euler's Multiples Redux

**Jason Feng**

You are given a list $a_1,a_2,...a_n$ of $n$ unique prime numbers and limit $k$. Compute the number of integers in the inclusive range $[1,k]$ that are multiples of one or more primes from the list.

### Input Specification
The first line of input is two integers $n$ and $k$.
The second line of input is $n$ space-separated integers: the list of integers.

### Constraints
* $1 \le n \le 20$
* $1 \le k \le 10^9$
* $2 \le a_i \le 100, \space a_i \text{ is prime}$


### Output Specification
Output a single integer: the number of integers in the inclusive range $[1,k]$ that are multiples of one or more integers of the list.

<table><tr>
<td><b>Sample Input</b></td>
<td><b>Sample Output</b></td>
</tr>

<tr><td>

```
2 20
3 5
```

</td><td>

```
9
```
</td></tr>

<tr><td>

```
3 50
2 7 11
```

</td><td>

```
31
```
</td></tr>

<tr><td>

```
1 1000
2
```

</td><td>

```
500
```
</td></tr>

</table>

<div style="page-break-after: always;"></div>