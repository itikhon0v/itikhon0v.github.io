Hello, world!
2025-05-05
intro, blog, python

This is my first post using GitHub Pages! I am using small Python script converting markdown and generating RSS

```python
def hello(name: str = None) -> None:
    if not name:
        name = "world"
    print(f"Hello, {str(name).title()}!")
```