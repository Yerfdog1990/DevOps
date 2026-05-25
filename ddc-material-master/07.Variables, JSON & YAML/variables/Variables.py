print("Hello World")

# String variable
# In Python, a string is a sequence of characters.
print("============ String variable ============")
name = "John"
print(name)

# Integer variable
# In Python, an integer is a whole number, positive or negative, without decimals, of unlimited length.
print("============ Integer variable ============")
age = 25
print(age)

# Float variable
# In Python, a float is a number, positive or negative, containing one or more decimals.
print("============ Float variable ============")
height = 5.9
print(height)

# Boolean variable
# In Python, a boolean is a value of either True or False.
print("============ Boolean variable ============")
is_active = True
print(is_active)

# 1.Sequence Types (Ordered Collections)
# List (list)
# An ordered, mutable (changeable) collection that allows duplicate members. Note: In Python, standard arrays are typically implemented as lists.

print("============ List (Array) ============")
devopsToolsList = ["Jenkins", "Docker", "Kubernetes", "Terraform", "Ansible"]

# Common Methods & Operations
devopsToolsList.append("GitLab")          # Adds to the end
devopsToolsList.insert(1, "Prometheus")   # Inserts at index 1
devopsToolsList.remove("Docker")          # Removes specific item
popped_item = devopsToolsList.pop()       # Removes and returns last item
devopsToolsList.sort()                    # Sorts the list alphabetically

print(devopsToolsList)
print(type(devopsToolsList))              # <class 'list'>
print(len(devopsToolsList))                # Get length
print(devopsToolsList[0])                 # Access via index (Jenkins)
print(devopsToolsList[-1])                # Access via negative index (Ansible)
print(devopsToolsList[1:3])               # Access via slice (Docker, Kubernetes)
print(devopsToolsList[1:4][2])
print(devopsToolsList[:3])                # Access via slice (Jenkins, Docker, Kubernetes)
print(devopsToolsList[2:])                # Access via slice (Kubernetes, Terraform, Ansible)
print(devopsToolsList[::-1])              # Access via reverse slice (Ansible, Terraform, Kubernetes, Docker, Jenkins)
print(devopsToolsList.count("Ansible"))    # Access via count (1)
print(devopsToolsList.index("Ansible"))    # Access via index (1)

# Tuple (tuple)
# An ordered, immutable (unchangeable) collection that allows duplicate members. Used for data that shouldn't change.

print("============ Tuple ============")
devopsToolsTuple = ("Jenkins", "Docker", "Kubernetes", "Jenkins")

# Common Methods & Operations
print(devopsToolsTuple.count("Jenkins"))  # Returns 2 (counts occurrences)
print(devopsToolsTuple.index("Docker"))   # Returns 1 (finds index)
print(devopsToolsTuple[2])                # Access via index (Kubernetes)
print(type(devopsToolsTuple))             # <class 'tuple'>

# 2.Set Types (Unordered Collections)
# Set (set)
# An unordered, mutable collection with no duplicate elements. Great for membership testing and eliminating duplicates.

print("============ Set ============")
devopsToolsSet = {"Jenkins", "Docker", "Kubernetes", "Docker"} # "Docker" duplicate will be ignored

# Common Methods & Operations
devopsToolsSet.add("Terraform")           # Adds an element
devopsToolsSet.remove("Jenkins")          # Removes an element (raises error if missing)
devopsToolsSet.discard("Puppet")          # Removes if present, won't error if missing

# Set Math Operations
anotherSet = {"Docker", "AWS"}
print(devopsToolsSet.intersection(anotherSet)) # Returns common items
print(devopsToolsSet.union(anotherSet))        # Combines both sets

print(devopsToolsSet)                     # Order will be random
print(type(devopsToolsSet))               # <class 'set'>

# Frozen Set (frozenset)
# An immutable version of a set. Once created, elements cannot be added or removed.

immutableSet = frozenset(["Jenkins", "Docker", "Kubernetes"])
print(type(immutableSet))                 # <class 'frozenset'>

# 3. Mapping Type
# Dictionary (dict)
# An ordered (as of Python 3.7) collection of key-value pairs. Keys must be unique and immutable.

print("============ Dictionary ============")
toolCategory = {
    "CI/CD": "Jenkins",
    "Container": "Docker",
    "Orchestration": "Kubernetes"
}

# Common Methods & Operations
toolCategory["IaC"] = "Terraform"         # Adding/Updating a key-value pair
print(toolCategory.get("Container"))      # Returns "Docker" safely
print(toolCategory.keys())                # Returns dict_keys list
print(toolCategory.values())              # Returns dict_values list
print(toolCategory.items())               # Returns list of (key, value) tuples
print(toolCategory.pop("CI/CD"))          # Removes and returns the value for "CI/CD"
print(toolCategory)                       # Shows remaining items
print(toolCategory["Orchestration"])      # Returns "Kubernetes"
print(toolCategory["Orchestration"][2])   # Returns "b"
print(toolCategory.clear())               # Removes all items
print(toolCategory)                       # Shows empty dictionary

print(type(toolCategory))                 # <class 'dict'>