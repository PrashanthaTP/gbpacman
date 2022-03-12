from bs4 import BeautifulSoup
from re import (search as re_search,
                IGNORECASE as re_IGNORECASE)
"""
why some filters are in 'decorator' style
-  to support internal state management?
   - kind of bloat though? do you think you can convince me
     by saying some big words like 'state' 'management'and stuff
   - atleast make all the function consistent
   - okay okay will do, remember its a work in progress
   
"""

# **TODO**:
# Make all filter function consistent


def match_class(reference):
    def filter(candidate):
        if reference.has_attr('class') and candidate.has_attr('class'):
            return reference['class'] == candidate['class']
        else:
            return not reference.has_attr('class')

    return filter


def match_name(reference):

    def filter(candidate):
        return reference.name == candidate.name

    return filter


def match_name_and_text(reference):
    def filter(candidate):
        return reference.name == candidate.name and\
            candidate.text.lower() in reference.text.lower()
    return filter


def create_filter(template_html, target_html, attrs=None, **kwargs_for_find):
    if attrs is None:
        attrs = {}
    template_soup = BeautifulSoup(template_html, features="html.parser")
    target_soup = BeautifulSoup(target_html, features="html.parser")
    base_filter = match_name(template_soup)
    match = template_soup.find(base_filter, attrs=attrs, **kwargs_for_find)

    if match is None:
        raise Exception("Match is empty")

    def tags_filter(tag):
        is_base_matched = base_filter(tag)
        is_parent_matched = tag.parent.name == match.parent.name
        is_parent_class_matched = match_class(match.parent)(tag)
        is_next_element_matched = tag.find_next_element(
        ).name == match.find_next_element().name
        is_prev_element_matched = tag.find_prev_element(
        ).name == match.find_prev_element().name
        return is_base_matched \
            and is_parent_matched \
            and is_next_element_matched \
            and is_prev_element_matched

    return tags_filter, {"attrs": attrs, **kwargs_for_find}


def create_filter_v1(template_html, target_text):
    soup = BeautifulSoup(template_html, features="html.parser")
    matched_tags = soup.find_all(
        lambda tag: tag.text.lower() == target_text.lower(), limit=1)
    return matched_tags


def filter_for_div_sibling(tag):
    """
    for package found:
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

if package not found
<div class="card mb-3">
  <div class="card-header">
    <h4 class="card-title">Search results for "tmux1"</h4>
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

      </tbody>
    </table>
  </div>
</div>
    """
    match = re_search(r".*search\s*results.*",
                      tag.text,
                      flags=re_IGNORECASE)
    if tag.name == "div" and match is not None:
        print(" found ".center(30, "*"))
        print(tag.name)
        print("parent", tag.parent.name, tag.parent.text)
        print("sibling", tag.next_sibling.name,)
    return tag.name == "td" and tag.text.lower() == "A terminal multiplexer".lower()


def filter_tag(tag):
    """
    for package found:
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

if package not found
<div class="card mb-3">
  <div class="card-header">
    <h4 class="card-title">Search results for "tmux1"</h4>
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

      </tbody>
    </table>
  </div>
</div>
    """
    match = re_search(r".*search\s*results.*",
                      tag.text,
                      flags=re_IGNORECASE)
    if tag.name == "div" and match is not None:
        print(" found ".center(30, "*"))
        print(tag.name)
        print("parent", tag.parent.name, tag.parent.text)
        print("sibling", tag.next_sibling.name,)
    return tag.name == "td" and tag.text.lower() == "A terminal multiplexer".lower()


def get_content_of_div_sibling(soup):
    soup.findall()


def is_search_table(tag):
    content_matches = re_search(r".*search\s*results.*",
                                tag.text,
                                flags=re_IGNORECASE)
    num_of_direct_children = len(tag.find_all(recursive=False))
    return tag.name == "div" \
        and content_matches is not None \
        and num_of_direct_children == 2


def get_package_table(soup):

    return soup.find(is_search_table)


def is_base_package_link(tag):
    prev_sibling = tag.find_previous_sibling()
    if prev_sibling is None:
        return False
    prev_heading = re_search(r".*Binary Packages\s?:?\s?.*",
                             prev_sibling.get_text(),
                             re_IGNORECASE)
    return tag.name == "dd"  \
        and prev_sibling.name == "dt"\
        and prev_heading is not None


def is_download_link(tag):
    parent = tag.parent
    if parent is None:
        return False
    prev_sibling = parent.find_previous_sibling()
    if prev_sibling is None:
        return False
    prev_heading = re_search(r".*File\s?:?\s?.*",
                             prev_sibling.get_text())
    return tag.name == "a"  \
        and parent.name == "dd"\
        and prev_sibling.name == "dt"\
        and prev_heading is not None
