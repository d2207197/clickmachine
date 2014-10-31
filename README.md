clickmachine
===========

A module for building series mouse moving, clicking actions.

```python
from clickmachine import Click, Clicks, Actions, Sleep, Repeat, Move

# Click(x, y)
Click(300, 400).act()

# Cilck(x, y, times, interval)
Clicks(100, 200, times = 10, interval = 0.1).act()

# Move(x, y)
Move(500, 450).act()

# Sleep(seconds)
Sleep(3).act()

# Actions(actions, interval)
Actions([
    Click(300, 400),
    Sleep(3),
    Clicks(100, 50, 20),
    Click(20, 100)
], interval = 0.5).act()

# Repeat(action, times, interval) # if times is None, won't stop
Repeat(Click(20, 50), 10, 0.5) #  == Clicks(20, 50, 10, 0.5)


# complex actions

move_sleep_clicks = Actions([
    Move(100, 200),
    Sleep(2),
    Clicks(300, 350, 30),
])

move_sleep_clicks_20times = Repeat(move_sleep_clicks, 20)

complex_actions = Repeat(Actions([
    Click(30, 150),
    move_sleep_clicks_20times,
    Sleep(20)
]), interval = 3)

complex_actions.act()

```


## Install

```console
$ pip install https://github.com/d2207197/clickmachine/archive/master.zip
```


## Examples

`examples/clicker_heros.py`: A robot for [Clicker Heros](clickerheroes.com)



## Tools

### simple_click

A simple click tool for ClickerHeroes - just perform clicks!

```
python simple_click.py x y [options]
```




