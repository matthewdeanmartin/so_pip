Well, you could always write a simple script that searches the file for `import` statements. This one finds all imported modules and files, including those imported in functions or classes:

    def find_imports(toCheck):
        &quot;&quot;&quot;
        Given a filename, returns a list of modules imported by the program.
        Only modules that can be imported from the current directory
        will be included. This program does not run the code, so import statements
        in if/else or try/except blocks will always be included.
        &quot;&quot;&quot;
        import imp
        importedItems = []
        with open(toCheck, &#39;r&#39;) as pyFile:
            for line in pyFile:
                # ignore comments
                line = line.strip().partition(&quot;#&quot;)[0].partition(&quot;as&quot;)[0].split(&#39; &#39;)
                if line[0] == &quot;import&quot;:
                    for imported in line[1:]:
                        # remove commas (this doesn&#39;t check for commas if
                        # they&#39;re supposed to be there!
                        imported = imported.strip(&quot;, &quot;)
                        try:
                            # check to see if the module can be imported
                            # (doesn&#39;t actually import - just finds it if it exists)
                            imp.find_module(imported)
                            # add to the list of items we imported
                            importedItems.append(imported)
                        except ImportError:
                            # ignore items that can&#39;t be imported
                            # (unless that isn&#39;t what you want?)
                            pass
                    
        return importedItems

    toCheck = raw_input(&quot;Which file should be checked: &quot;)
    print find_imports(toCheck)

This doesn&#39;t do anything for `from module import something` style imports, though that could easily be added, depending on how you want to deal with those. It also doesn&#39;t do any syntax checking, so if you have some funny business like `import sys gtk, os` it will think you&#39;ve imported all three modules even though the line is an error. It also doesn&#39;t deal with `try`/`except` type statements with regards to import - if it could be imported, this function will list it. It also doesn&#39;t deal well with multiple imports per line if you use the `as` keyword. The real issue here is that I&#39;d have to write a full parser to really do this correctly. The given code works in many cases, as long as you understand there are definite corner cases.

One issue is that relative imports will fail if this script isn&#39;t in the same directory as the given file. You may want to add the directory of the given script to `sys.path`.