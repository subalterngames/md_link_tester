### 1.1.0

- On a 429 error, `MdLinkTester` will wait and retry the connection.
- Fixed: `MdLinkTester` tries to parse internal links that include a `#`.

### 1.0.0

- Fixed: Status code 302 treated as a bad link
- Added: `MdLinkTester.get_text(text)`