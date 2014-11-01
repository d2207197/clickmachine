clickmachine
===========

A module for building series mouse moving, clicking actions.

```python
from clickmachine import Click, Clicks, Actions, Sleep, Repeat, Move

# Actions would execute after call the act() method

# Click(x, y)
Click(300, 400).act()

# Cilck multiple times. Using the repeat() method
click_20times = Click(100, 200).repeat(20)
click_20times.act()

# Move(x, y)
move_to_500_450 = Move(500, 450)
click_500_450 = move_to_500_450.to_click()
move_to_500_450.act()
click_500_450.act()

# Sleep(seconds)
Sleep(3).act()

# Actions(action1, action2, action3, ...)
Actions(
    Click(300, 400),
    Sleep(3),
    Click(100, 50, 20).repeat(20),
    Click(20, 100)
).act()

# Repeat(action, times, interval) # if times is None, won't stop
Repeat(Click(20, 50), 20, 0.5)
Click(20, 50).repeat(times = 20, interval = 0.5) 


# complex actions

move_sleep_clicks = Actions(
    Move(100, 200),
    Sleep(2),
    Clicks(300, 350, 30),
)

move_sleep_clicks_20times = move_sleep_clicks.repeat(20)

complex_actions = Actions(
    Click(30, 150),
    move_sleep_clicks_20times,
    Sleep(20),
    ).interval(3).repeat()

complex_actions.act()

```

----

## Install

```console
$ pip install https://github.com/d2207197/clickmachine/archive/master.zip
```

----

## Examples

`examples/clicker_heros.py`: A robot for [Clicker Heros](http://www.clickerheroes.com)


----
## Tools

#### simple_click.py

A tool just performing clicks!

```console
$ simple_click x y [options]
```




