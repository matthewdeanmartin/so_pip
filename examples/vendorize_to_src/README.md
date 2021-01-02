Example Steps
-------------

First time
- Write your application `example`
- run `so_pip vendorize email --question=3362600 --output=vendor_src`
- Manually copy module code from vendor_src to example/_vendor
- Edit code until it is reusable
- Add `import example._vendor.email_a_tuition_classification.main as emailer` and re-use code.

If an answer is already perfect, then use revision pinning and automatically
copy the answer to your _vendor folder.

Updating
- Possibly update the code on StackOverflow.
- run `so_pip upgrade --question=3362600 --output=vendor_src`
- Use your favorite diff tool to merge example/_vendor and the
appropriate folder in vendor_src
