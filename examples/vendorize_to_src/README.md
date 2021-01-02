Example Steps
-------------

First time
- Write your application `example`
- run `so_pip vendorize --question=123 --output=vendor_src`
- Manually copy module code from vendor_src to example/_vendor
- Edit code until it is reusable
- Add `import exampe._vendorize as vendor` and re-use code.

Updating
- Possibly update the code on StackOverflow.
- run `so_pip upgrade --question=123 --output=vendor_src`
- Use your favorite diff tool to merge example/_vendor and the
appropriate folder in vendor_src
