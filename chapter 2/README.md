# Chapter 2

In this chapter, we coded a mock-up Taipy Gui application. Each of the directories represents a main step in the building process:

* Part 1: A single page app, with static content.
* Part 2: Multiple page app, we added a unit convertor, to demonstrate Callback.
* Part 3: the final application.

## Extra content

### Change themes with a toggle button

Taipy has two themes: dark and light, which you can choose using the `run()` method (with the dark_mode Boolean parameter). You can also add a toggle button to let users switch themes, anywhere on the root page:

```
tgb.toggle(theme=True)
```