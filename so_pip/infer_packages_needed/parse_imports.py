"""
Astroid to parse imports found in source code

This is safer than importing & using inspection or library loader code.
"""

if __name__ == "__main__":
    import astroid

    thing = astroid.extract_node("""import foobar""")
    print(thing)
