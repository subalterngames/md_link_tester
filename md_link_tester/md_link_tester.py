from time import sleep
from typing import List, Dict, Union
import os
from pathlib import Path
import re
from requests import head, ConnectionError, ConnectTimeout


class MdLinkTester:
    """
    Recursively find all .md files in a directory and test all of their links.
    """

    """:class_var
    The search string for URLs on a markdown page.
    """
    SEARCH_STRING: str = r"\[(.*?)\]\((.*?)\)"
    """:class_var
    Status codes that indicate a valid link.
    """
    GOOD_STATUS_CODES: List[int] = [200, 301, 302]

    @staticmethod
    def test_directory(path: Union[str, Path], ignore_files: List[str] = None) -> Dict[str, List[str]]:
        """
        Test all links in each .md file in a directory.

        :param path: The root directory.
        :param ignore_files: A list of file names (incuding the file extension) that will be ignored. Can be None.

        :return: A dictionary. Key = A file path. Value = A list of broken links in that file.
        """

        if isinstance(path, Path):
            path = str(path.resolve())
        if ignore_files is None:
            ignore_files = []
        files_with_bad_links: Dict[str, List[str]] = dict()
        for root, dirs, files in os.walk(path):
            for file in files:
                # Ignore files that aren't .md (markdown).
                if not file.endswith(".md"):
                    continue
                if file in ignore_files:
                    continue
                path = os.path.join(root, file)
                bad_links = MdLinkTester.test_file(path=path)
                if len(bad_links) > 0:
                    files_with_bad_links[path] = bad_links
        return files_with_bad_links

    @staticmethod
    def test_file(path: Union[str, Path]) -> List[str]:
        """
        Test all links in a single file.

        :param path: The path to the file.

        :return: A list of broken links.
        """

        if isinstance(path, str):
            path = Path(path)
        text = path.read_text(encoding="utf-8")
        # Switch to this path's directory.
        cwd = os.getcwd()
        d = str(path.parent.resolve())
        os.chdir(d)
        bad_links = MdLinkTester.test_text(text=text)
        os.chdir(cwd)
        return bad_links

    @staticmethod
    def test_text(text: str) -> List[str]:
        """
        Test all links in a body of text.

        :param text: The text.

        :return: A list of broken links.
        """

        # Get each link in the document.
        links = re.findall(MdLinkTester.SEARCH_STRING, text, flags=re.MULTILINE)
        # Get all of the links from the tuple. Ignore email addresses.
        links: List[str] = [link[1] for link in links if "@" not in link[1]]
        # Record all bad links.
        bad_links: List[str] = list()
        for link in links:
            # Test a URL.
            if link.startswith("http"):
                try:
                    resp = head(link)
                    if resp.status_code == 429:
                        if "Retry-After" in resp.headers:
                            sleep(float(resp.headers["Retry-After"]))
                        else:
                            sleep(60)
                        resp = head(link, verify=link.startswith("https"))
                    if resp.status_code not in MdLinkTester.GOOD_STATUS_CODES:
                        bad_links.append(link)
                except ConnectTimeout:
                    bad_links.append(link)
                except ConnectionError:
                    bad_links.append(link)
            else:
                try:
                    if link.startswith("#"):
                        continue
                    elif "#" in link:
                        link_no_header = re.search(r"((.*)\.md)", link).group(1)
                    else:
                        link_no_header = link
                    if not Path(link_no_header).exists():
                        bad_links.append(link)
                except AttributeError:
                    bad_links.append(link)
        return bad_links
