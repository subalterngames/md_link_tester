from md_link_tester import MdLinkTester

bad_links = MdLinkTester.test_directory(path="doc", ignore_files=["another_page.md"])
for f in bad_links:
    print(f)
    for link in bad_links[f]:
        print("\t", link)
