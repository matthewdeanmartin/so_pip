As others have pointed out, you should use [zipfile](http://docs.python.org/library/zipfile.html). The documentation tells you what functions are available, but doesn't really explain how you can use them to zip an entire directory. I think it's easiest to explain with some example code:

    #!/usr/bin/env python
    import os
    import zipfile

    def zipdir(path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

    if __name__ == '__main__':
        zipf = zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir('tmp/', zipf)
        zipf.close()

Adapted from: http://www.devshed.com/c/a/Python/Python-UnZipped/
