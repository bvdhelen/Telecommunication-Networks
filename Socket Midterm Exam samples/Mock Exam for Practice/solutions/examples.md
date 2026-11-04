# ✅ **Task 1 Examples (Client → Server → Client)**

These examples cover **every possible case**: success, not found, invalid format, stock updates, etc.

---

# 🔵 **Example 1 — VIEW (existing item)**

### Client sends:

```
VIEW|PIZZ|0
```

### Server response:

```
Margherita Pizza:1200:10
```

**Explanation:**

* Item PIZZ exists
* Stock is 10
* Server returns: `name:price:stock`

---

# 🔵 **Example 2 — VIEW (non-existing item)**

### Client sends:

```
VIEW|SOUP|0
```

### Server response:

```
NOT_FOUND
```

**Explanation:**
No item with ID SOUP exists.

---

# 🟢 **Example 3 — ORDER (success)**

Assume PIZZ stock = 10.

### Client sends:

```
ORDER|PIZZ|3
```

### Server response:

```
SUCCESS:3600
```

**Explanation:**

* price = 1200
* quantity = 3
* total = 3600
* stock becomes **7**

---

# 🟡 **Example 4 — ORDER (insufficient stock)**

Assume PIZZ stock = 7 after previous order.

### Client sends:

```
ORDER|PIZZ|8
```

### Server response:

```
NO_STOCK
```

**Explanation:**
User requested 8 but only 7 left.

---

# 🔵 **Example 5 — ORDER (item not found)**

### Client sends:

```
ORDER|XXXX|2
```

### Server response:

```
NOT_FOUND
```

---

# 🔴 **Example 6 — Invalid format (too few fields)**

### Client sends:

```
VIEW|PIZZ
```

### Server response:

```
ERROR
```

---

# 🔴 **Example 7 — Invalid format (too many fields)**

### Client sends:

```
ORDER|PIZZ|3|extra
```

### Server response:

```
ERROR
```

---

# 🔴 **Example 8 — Invalid action**

### Client sends:

```
DELETE|PIZZ|0
```

### Server response:

```
ERROR
```

---

# 🔴 **Example 9 — Quantity must be an integer**

### Client sends:

```
ORDER|PIZZ|two
```

### Server response:

```
ERROR
```

---

# 🟣 **Example 10 — VIEW must always send quantity 0**

### Client sends:

```
VIEW|PIZZ|5
```

### Server response:

```
ERROR
```

---

# 🟢 **Example 11 — Multiple operations in one session**

```
Client: VIEW|BURG|0
Server: Cheeseburger:800:15

Client: ORDER|BURG|2
Server: SUCCESS:1600

Client: VIEW|BURG|0
Server: Cheeseburger:800:13

Client: QUIT
(Client disconnects)
```

---

# 🟩 **Example 12 — Server stock update demonstration**

Starting menu:

```
PIZZ: stock = 10
```

Sequence:

1. Client:

   ```
   ORDER|PIZZ|4
   ```

   Server:

   ```
   SUCCESS:4800
   ```

   New stock = 6

2. Client:

   ```
   VIEW|PIZZ|0
   ```

   Server:

   ```
   Margherita Pizza:1200:6
   ```
