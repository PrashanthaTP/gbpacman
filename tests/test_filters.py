import unittest
from plogger import get_logger
from gbpacman.lib import filters, calls, parser
url = "https://packages.msys2.org/"

logger = get_logger(__name__)


class TestFilters(unittest.TestCase):
    def test_create_filter_(self):
        template = """
        <body>
            <div>
                parent
                <h1>aytala</h1>
                <h2>sibling</h2>
            </div>
            <div>
                target
            </div>
        </body>
        """

        res = filters.create_filter_v1(template, target_text="aytala")[0]
        print(res)
        self.assertEqual(res.name, "h1")
        self.assertEqual(res.parent.name, "div")
        self.assertEqual(
            res.parent.find_next_sibling().get_text(strip=True), "target")

    def test_create_filter(self):
        template = """
        <div class="card mb-3">
          <div class="card-header">
            <h4 class="card-title">Search results for "tmux"</h4>
            <h6 class="card-subtitle mb-2 text-muted">Base packages matching the search query</h6>
          </div>
          <div class="card-body overflow-auto">
            <table class="table table-hover table-sm">
              <thead>
                <tr>
                  <th>Base Package</th>
                  <th>Version</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>

                <tr>
                  <td><a href="https://packages.msys2.org/base/tmux">tmux</a></td>
                  <td>3.2.a-1</td>
                  <td>A terminal multiplexer</td>
                 </tr>

              </tbody>
            </table>
          </div>
        </div>

        """
        target = """
              <tbody>

                <tr>
                  <td><a href="https://packages.msys2.org/base/tmux">tmux</a></td>
                  <td>3.2.a-1</td>
                  <td>A terminal multiplexer</td>
                 </tr>
              </tbody>
              """
        filter, kwargs_for_find = filters.create_filter(
            template, target, name="tbody")
        response = calls.ping_url(url)
        exerpt = parser.extract(response, filter, **kwargs_for_find)
        print(exerpt)


if __name__ == "__main__":
    unittest.main(verbosity=3)
