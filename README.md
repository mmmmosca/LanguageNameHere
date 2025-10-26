# Timballo

## Variables
```
$variableName = value    # Variable declaration/assignment
$x = 42                  # Number assignment
$text = "Hello"         # String assignment
$input = %              # Read input from user
```

## Sections (Functions)
```
sect sectionName        # Define a section
    # code here
    ;                   # End section with semicolon

@sectionName           # Call/jump to a section
```

## Control Flow
```
if condition then action    # If statement
if $x > 5 then print "big" # Example with comparison
if $i == 10 then exit      # Exit program condition
```

## Operators
### Arithmetic
```
$a = $b + $c    # Addition
$a = $b - $c    # Subtraction
$a = $b * $c    # Multiplication
$a = $b / $c    # Division
$a = $b % $c    # Modulo
```

### Comparison
```
==    # Equal to
!=    # Not equal to
>     # Greater than
<     # Less than
>=    # Greater than or equal to
<=    # Less than or equal to
```

## Input/Output
```
print "text"     # Print string literal
print $var       # Print variable value
$x = %           # Read input from user
```

## Comments
```
-- This is a comment
```

## Program Structure
```
-- Every program must have a main section
sect data
    # Your variables here
    ;

sect main
    # Your code here
    ;

-- Example of a complete program
sect data
    $counter = 0
    ;

sect loop
    print $counter
    $counter = $counter + 1
    if $counter < 5 then @loop
    ;

sect main
    @loop
    ;
```

## Special Commands
```
exit            # Terminate program execution
```

## Key Rules
1. All variables start with `$` and can only be defined inside the data section
2. Every section must end with `;`
3. Every program must have a `main` and `data` section
4. Strings must be in double quotes
5. Comments start with `--`
6. Sections can be called/jumped to using `@`
7. File extension must be `.tim`
