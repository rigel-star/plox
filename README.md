# plox
Plox programming language

## Examples:

### Variable declaration
```
var name = [value];
```

### Function declaration
```
fun name(param1, param2, ...)
{
    // body
}
```

or

```
var func_name = fun (a, b, ...) {
    // body
};
```

## If ... else
```
if(condition)
{
    // body
}
else
{
    // body
}
```

### Loop(While)
```
while(condition)
{
    // body
}
```

## Anonymous function
```
fun caller(func, arg)
{
    func(arg);
}

caller(fun (arg) {
    print(arg)
}, "Ramesh");
```

## Arithmetic Operations
```
+ - * /
```

## Bit operations
```
& ^ | << >> ~
```

## Run:

`python3 plox.py [plox script]`
