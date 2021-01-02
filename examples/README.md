Workflows
----------
Here are two worked examples.

Our hypothetical developer wants to [send an email and
finds these answers](https://stackoverflow.com/questions/3362600/how-to-send-email-attachments).

[Vendorize to your source tree](vendorize_to_src)
---------------------
- Vendorize code from StackOverflow to vendor_src/ folder
- Pick an answer
- Copy .py files to /src/example/_vendor/
- Import code from `example._vendor`
- If you have to edit, pick a different answer or edit on StackOverflow and repeat


[Self Managed Packages](self_managed_packages)
---------------------
- Vendorize code from StackOverflow to /vendor_src/
- Package it
    - Don't upload to pypi
    - Consider a private package repository
- Use `pip install some_package.whl --target vendor` to install
- Add /vendor/ folder to your PYTHONPATH

Pypi managed packages
---------------------
I will not provide an example, because this is a bad workflow.
- You may feel like publishing junk to pypi because it is easy. Don't.
- Run `so_pip vendorize` command
- Edit until code is re-usable. No one wants to re-use code that needs editing.
- Package and publish to pypi.
- Repeat everytime that package is edited so you can comply with the "Right to be
forgotten" provisions of CC BY SA.
