# md_link_tester

Test all of the links in a markdown (.md) file or directory of markdown files.

Links can be http URLs:

```
[md_link_tester](https://github.com/alters-mit/md_link_tester)
```

Links can be internal markdown links:

```
[md_link_tester](README.md)
```

Requires Python 3.6+

## Install

1. `git clone https://github.com/alters-mit/md_link_tester`
2. `cd md_link_tester`
3. `pip3 install -e .`

## Usage

See `doc/test.md` in this repo.

To test the links of a single file:

```python
from md_link_tester import MdLinkTester

bad_links = MdLinkTester.test_file(path="doc/test.md")
print(bad_links)
```

To test the links of each file in a directory and all of its subdirectories:

```python
from md_link_tester import MdLinkTester

files_with_bad_links = MdLinkTester.test_directory(path="doc", ignore_files=["another_page.md"])
for f in files_with_bad_links:
    print(f)
    for link in files_with_bad_links[f]:
        print("\t", link)
```