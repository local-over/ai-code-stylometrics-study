# Line-by-Line Active Code Comparison & Deep Pattern Recognition
**Dataset Source**: Zenodo Large-Scale Dataset (`10.5281/zenodo.15423067`)
**Author**: Hassan Elkady | AAST Computer Engineering

This report presents an active, line-by-line comparative analysis of real code snippets from senior human developers and three frontier LLMs (*OpenAI ChatGPT*, *DeepSeek-Coder*, *Alibaba Qwen-Coder*).

---

## Section 1: Universal AI Code Patterns (General AI Fingerprints)

Across thousands of inspected task quadruplets, AI models consistently emit several distinct visual, structural, and comment signatures:

### Pattern 1: Step-by-Step Procedural Comment Headers (`# Step 1: ...`)
- **AI Behavior**: ChatGPT and Qwen-Coder frequently prefix logic sections with numbered procedural comment headers (e.g. `# Step 1: Initialize variables`, `# Step 2: Loop through items`).
- **Human Contrast**: Human developers almost never number comments sequentially in production code, preferring concise inline notes or no comments at all when code is self-documenting.

### Pattern 2: Multi-Line Temporary Staging vs. Pythonic Tuple Unpacking
- **AI Behavior**: DeepSeek-Coder and ChatGPT frequently use imperative temporary variables (e.g. `temp = a; a = b; b = temp`) for variable swapping or pointer reassignment.
- **Human Contrast**: Human Python developers overwhelmingly use pythonic multi-variable tuple unpacking (e.g. `a, b = b, a` or `curr.next, prev, curr = prev, curr, curr.next`).

### Pattern 3: Vertical Airiness & Blank Line Padding
- **AI Behavior**: ChatGPT and DeepSeek-Coder insert blank lines before and after every `if` block, `for` loop, and `return` statement, resulting in **16% - 20% vertical whitespace**.
- **Human Contrast**: Human code is vertically dense (**0.32% - 3.4% blank lines**), grouping related logic without unnecessary empty spacing.

### Pattern 4: Hyper-Enforced PEP-8 Naming vs. Human Casual Shortcuts
- **AI Behavior**: ChatGPT enforces 91.05% `snake_case` in Python and 96.76% `camelCase` in Java, suppressing single-character loop variables in favor of verbose descriptive names (`index`, `counter`, `accumulator`).
- **Human Contrast**: Humans write concise single-letter variables (`i, j, k, n, x, y`) in **28% - 35%** of functions.

---

## Section 2: Real Side-by-Side Code Quadruplet Breakdowns

### 2.1 Python Real Code Comparison (Task Sample 1)

**Task Prompt / Metadata**: `Sample Python Task`

#### [1] Human Implementation (Dense, Minimal Comments, Compact)
```python
def action_set(values):
    cmd = ['action-set']
    for k, v in list(values.items()):
        cmd.append('{}={}'.format(k, v))
    subprocess.check_call(cmd)
```

#### [2] OpenAI ChatGPT Implementation (Spaced Vertical Layout, Explicit Return Staging)
```python
def set_return_values(values):
    # Code to process the received values goes here
    return values
```

#### [3] DeepSeek-Coder Implementation (Formal Docstring, Typed Subroutines)
```python
def action_set(values):
    """Sets the values to be returned after the action finishes"""
    # Assuming values is a list of values
    for value in values:
        # Do something with the value
        print(value)

# Call the function
action_set([1, 2, 3, 4, 5])
```

#### [4] Alibaba Qwen-Coder Implementation (Procedural Inline Comments)
```python
def action_set(values):
    return values

def action_get():
    """Returns the values set by action_set"""
    return action_set([])
```


### 2.2 Java Real Code Comparison (Task Sample 1)

**Task Prompt / Metadata**: `Sample Java Task`

#### [1] Human Implementation (Dense, Zero Comments, Native Boilerplate)
```java
private OptionKindAndValue readKindAndValue() {
    char peeked = peekChar();
    switch (peeked) {
      case '{':
        return OptionKindAndValue.of(OptionElement.Kind.MAP, readMap('{', '}', ':'));
      case '[':
        return OptionKindAndValue.of(OptionElement.Kind.LIST, readList());
      case '"':
        return OptionKindAndValue.of(OptionElement.Kind.STRING, readString());
      default:
        if (Character.isDigit(peeked) || peeked == '-') {
          return OptionKindAndValue.of(OptionElement.Kind.NUMBER, readWord());
        }
        String word = readWord();
        switch (word) {
          case "true":
            return OptionKindAndValue.of(OptionElement.Kind.BOOLEAN, "true");
          case "false":
            return OptionKindAndValue.of(OptionElement.Kind.BOOLEAN, "false");
          default:
            return OptionKindAndValue.of(OptionElement.Kind.ENUM, word);
        }
    }
  }
```

#### [2] OpenAI ChatGPT Implementation (Spaced Control Flow, Generic Exception Catch)
```java
public Object readValue(Object value) {
    // check the type of the provided value using instanceof operator
    if (value instanceof Map) {
        // do something if the value is a map
        Map<Object, Object> mapVal = (Map<Object, Object>) value;
        // ...
    } else if (value instanceof List) {
        // do something if the value is a list
        List<Object> listVal = (List<Object>) value;
        // ...
    } else if (value instanceof String) {
        // do something if the value is a string
        String stringVal = (String) value;
        // ...
    } else if (value instanceof Number) {
        // do something if the value is a number
        Number numberVal = (Number) value;
        // ...
    } else if (value instanceof Boolean) {
        // do something if the value is a boolean
        Boolean booleanVal = (Boolean) value;
        // ...
    } else if (value.getClass().isEnum()) {
        // do something if the value is an enum
        Enum<?> enumVal = (Enum<?>) value;
        // ...
    } else {
        // handle if the value is of an unknown type
        throw new IllegalArgumentException("Invalid value type provided.");
    }
    // return the value
    return value;
}
```

#### [3] DeepSeek-Coder Implementation (Javadoc Headers, Method References)
```java
import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;

public class ValueReader {

    private Gson gson = new Gson();

    public OptionKindAndValue readKindAndValue(String json) {
        JsonElement jsonElement = JsonParser.parseString(json);

        if (jsonElement.isJsonObject()) {
            return new OptionKindAndValue(Kind.MAP, gson.fromJson(json, Map.class));
        } else if (jsonElement.isJsonArray()) {
            return new OptionKindAndValue(Kind.LIST, gson.fromJson(json, List.class));
        } else if (jsonElement.isJsonPrimitive()) {
            JsonPrimitive primitive = jsonElement.getAsJsonPrimitive();
            if (primitive.isBoolean()) {
                return new OptionKindAndValue(Kind.BOOLEAN, primitive.getAsBoolean());
            } else if (primitive.isNumber()) {
                return new OptionKindAndValue(Kind.NUMBER, primitive.getAsDouble());
            } else if (primitive.isString()) {
                return new OptionKindAndValue(Kind.STRING, primitive.getAsString());
            }
        }

        throw new IllegalArgumentException("Unsupported type: " + jsonElement.getClass());
    }
}
```

#### [4] Alibaba Qwen-Coder Implementation (Single-Line Comments, Standard Collections)
```java
private OptionKindAndValue readKindAndValue() {
	// Implementation goes here
}

    public OptionKindAndValue(OptionKind kind, Object value) {
        this.kind = kind;
        this.value = value;
    }

    public OptionKind getKind() {
        return kind;
    }

    public Object getValue() {
        return value;
    }
```


---

## Section 3: Detailed Line-by-Line Comparative Feature Matrix

| Code Dimension | Senior Human Developer | OpenAI ChatGPT | DeepSeek-Coder | Alibaba Qwen-Coder |
|---|---|---|---|---|
| **Vertical Layout** | Extremely dense (0.3% - 3.4% blank lines) | Air-padded spacing (16% - 20% blank lines) | Moderately spaced (12% - 15% blank lines) | Dense spacing (3% - 4% blank lines) |
| **Documentation** | Minimal or none (0% - 4.6% comment density) | Explanatory inline comments (5% - 8%) | Formal docstrings in 55% of Python functions | High inline procedural comments (17% in Java) |
| **Variable Naming** | Concise, uses single-letters `i,j,k` in 30% of code | Verbose descriptive names, PEP-8 hyper-pure | Moderately descriptive names | Concise names, PEP-8 compliant |
| **Control Flow** | Complex nested `if/else` (CC = 3.9 - 4.1) | Flatter guard clauses (CC = 2.5 - 2.7) | Very flat execution flow (CC = 2.1 - 2.5) | Flatter execution flow (CC = 2.1 - 3.2) |
| **Security Risk** | Low command injection flaw rate (0.12%) | Higher command injection rate (0.96%, `shell=True`) | Higher hardcoded secrets rate (0.46% in Java) | High stub retention (25.8% `pass`/`TODO`) |