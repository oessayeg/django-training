from elem import Elem, Text
from elements import (
    H1,
    H2,
    P,
    Body,
    Head,
    Html,
    Li,
    Ol,
    Span,
    Table,
    Th,
    Title,
    Tr,
    Ul,
    Div,
    Td,
)


class Page:
    valid_types = {
        "html",
        "head",
        "body",
        "title",
        "meta",
        "img",
        "table",
        "th",
        "tr",
        "td",
        "ul",
        "ol",
        "li",
        "h1",
        "h2",
        "p",
        "div",
        "span",
        "hr",
        "br",
    }

    def __init__(self, elem):
        self.elem = elem

    def _is_valid_tag(self, tag):
        return tag in self.valid_types

    def html_tag_validator(self, content):
        return (
            len(content) == 2
            and isinstance(content[0], Head)
            and isinstance(content[1], Body)
        )

    def head_tag_validator(self, content):
        return len(content) == 1 and isinstance(content[0], Title)

    def body_tag_validator(self, content):
        for element in content:
            if not (
                isinstance(element, H1)
                or isinstance(element, H2)
                or isinstance(element, Div)
                or isinstance(element, Table)
                or isinstance(element, Ul)
                or isinstance(element, Ol)
                or isinstance(element, Span)
                or isinstance(element, Text)
            ):
                return False
        return True

    def text_only_validator(self, content):
        return len(content) == 1 and isinstance(content[0], Text)

    def p_tag_validator(self, content):
        return all(isinstance(element, Text) for element in content)

    def span_tag_validator(self, content):
        return all(
            (isinstance(element, Text) or isinstance(element, P)) for element in content
        )

    def ol_ul_tag_validator(self, content):
        return len(content) > 0 and all(isinstance(element, Li) for element in content)

    def table_tag_validator(self, content):
        return len(content) > 0 and all(isinstance(element, Tr) for element in content)

    def tr_tag_validator(self, content):
        if len(content) == 0:
            return False

        has_th = False
        has_td = False

        for element in content:
            if isinstance(element, Th):
                has_th = True
            elif isinstance(element, Td):
                has_td = True
            else:
                return False

        if not (has_th or has_td):
            return False

        if has_th and has_td:
            return False

        return True

    def __str__(self):
        if isinstance(self.elem, Html):
            return f"<!DOCTYPE html>\n{self.elem.__str__()}"
        return self.elem.__str__()

    def validate_content(self, content, parent_tag):
        if not self._is_valid_tag(parent_tag):
            return False

        is_valid_structure = True
        if parent_tag == "html":
            is_valid_structure = self.html_tag_validator(content)
        elif parent_tag == "head":
            is_valid_structure = self.head_tag_validator(content)
        elif parent_tag == "body" or parent_tag == "div":
            is_valid_structure = self.body_tag_validator(content)
        elif parent_tag in ["title", "h1", "h2", "li", "th", "td"]:
            is_valid_structure = self.text_only_validator(content)
        elif parent_tag == "p":
            is_valid_structure = self.p_tag_validator(content)
        elif parent_tag == "span":
            is_valid_structure = self.span_tag_validator(content)
        elif parent_tag == "ol" or parent_tag == "ul":
            is_valid_structure = self.ol_ul_tag_validator(content)
        elif parent_tag == "table":
            is_valid_structure = self.table_tag_validator(content)
        elif parent_tag == "tr":
            is_valid_structure = self.tr_tag_validator(content)

        if not is_valid_structure:
            return False

        for element in content:
            if isinstance(element, Elem):
                is_valid = self.validate_content(element.content, element.tag)
                if not is_valid:
                    return False
            elif not isinstance(element, Text):
                return False
        return True

    def is_valid(self):
        return self.validate_content(self.elem.content, self.elem.tag)

    def write_to_file(self, filename):
        with open(filename, "w") as f:
            f.write(self.__str__())


if __name__ == "__main__":
    print("=" * 50)
    print("TESTING SPECIFIC FAILING CASES FOR EACH TAG")
    print("=" * 50)

    print("\n1. Testing HTML tag - should fail (missing head)")
    invalid_html_no_head = Page(Html([Body([H1(Text("Test"))])]))
    print(f"   Valid: {invalid_html_no_head.is_valid()}")

    print("\n2. Testing HTML tag - should fail (missing body)")
    invalid_html_no_body = Page(Html([Head(Title(Text("Test")))]))
    print(f"   Valid: {invalid_html_no_body.is_valid()}")

    print("\n3. Testing HTML tag - should fail (wrong order)")
    invalid_html_wrong_order = Page(
        Html([Body([H1(Text("Test"))]), Head(Title(Text("Test")))])
    )
    print(f"   Valid: {invalid_html_wrong_order.is_valid()}")

    print("\n4. Testing HEAD tag - should fail (no title)")
    invalid_head_no_title = Page(Html([Head([]), Body([H1(Text("Test"))])]))
    print(f"   Valid: {invalid_head_no_title.is_valid()}")

    print("\n5. Testing HEAD tag - should fail (multiple titles)")
    invalid_head_multiple_titles = Page(
        Html(
            [
                Head([Title(Text("Title1")), Title(Text("Title2"))]),
                Body([H1(Text("Test"))]),
            ]
        )
    )
    print(f"   Valid: {invalid_head_multiple_titles.is_valid()}")

    print("\n6. Testing BODY tag - should fail (invalid child P)")
    invalid_body_with_p = Page(
        Html(
            [
                Head(Title(Text("Test"))),
                Body([P(Text("This P shouldn't be directly in body"))]),
            ]
        )
    )
    print(f"   Valid: {invalid_body_with_p.is_valid()}")

    print("\n7. Testing BODY tag - should fail (invalid child Title)")
    invalid_body_with_title = Page(
        Html([Head(Title(Text("Test"))), Body([Title(Text("Invalid title in body"))])])
    )
    print(f"   Valid: {invalid_body_with_title.is_valid()}")

    print("\n8. Testing TITLE tag - should fail (non-text content)")
    invalid_title_with_elem = Page(
        Html(
            [
                Head(Title([Text("Valid"), H1(Text("Invalid H1 in title"))])),
                Body([H1(Text("Test"))]),
            ]
        )
    )
    print(f"   Valid: {invalid_title_with_elem.is_valid()}")

    print("\n9. Testing H1 tag - should fail (multiple text elements)")
    invalid_h1_multiple_text = Page(
        Html([Head(Title(Text("Test"))), Body([H1([Text("First"), Text("Second")])])])
    )
    print(f"   Valid: {invalid_h1_multiple_text.is_valid()}")

    print("\n10. Testing LI tag - should fail (non-text content)")
    invalid_li_with_div = Page(
        Html([Head(Title(Text("Test"))), Body([Ul([Li(Div(Text("Div inside Li")))])])])
    )
    print(f"   Valid: {invalid_li_with_div.is_valid()}")

    print("\n11. Testing P tag - should fail (contains H1)")
    invalid_p_with_h1 = Page(
        Html(
            [
                Head(Title(Text("Test"))),
                Body([Div([P([Text("Valid text"), H1(Text("Invalid H1"))])])]),
            ]
        )
    )
    print(f"   Valid: {invalid_p_with_h1.is_valid()}")

    print("\n12. Testing SPAN tag - should fail (contains H1)")
    invalid_span_with_h1 = Page(
        Html(
            [
                Head(Title(Text("Test"))),
                Body([Span([Text("Valid"), H1(Text("Invalid H1 in span"))])]),
            ]
        )
    )
    print(f"   Valid: {invalid_span_with_h1.is_valid()}")

    print("\n13. Testing UL tag - should fail (contains H1)")
    invalid_ul_with_h1 = Page(
        Html(
            [
                Head(Title(Text("Test"))),
                Body([Ul([Li(Text("Valid")), H1(Text("Invalid H1 in UL"))])]),
            ]
        )
    )
    print(f"   Valid: {invalid_ul_with_h1.is_valid()}")

    print("\n14. Testing OL tag - should fail (empty list)")
    invalid_ol_empty = Page(Html([Head(Title(Text("Test"))), Body([Ol([])])]))
    print(f"   Valid: {invalid_ol_empty.is_valid()}")

    print("\n15. Testing TABLE tag - should fail (contains H1)")
    invalid_table_with_h1 = Page(
        Html(
            [
                Head(Title(Text("Test"))),
                Body([Table([H1(Text("Invalid H1 in table"))])]),
            ]
        )
    )
    print(f"   Valid: {invalid_table_with_h1.is_valid()}")

    print("\n16. Testing TR tag - should fail (mixed TH and TD)")
    invalid_tr_mixed = Page(
        Html(
            [
                Head(Title(Text("Test"))),
                Body([Table(Tr([Th(Text("Header")), Td(Text("Data"))]))]),
            ]
        )
    )
    print(f"   Valid: {invalid_tr_mixed.is_valid()}")

    print("\n17. Testing TR tag - should fail (contains H1)")
    invalid_tr_with_h1 = Page(
        Html(
            [
                Head(Title(Text("Test"))),
                Body([Table(Tr([H1(Text("Invalid H1 in TR"))]))]),
            ]
        )
    )
    print(f"   Valid: {invalid_tr_with_h1.is_valid()}")

    print("\n18. Testing TR tag - should fail (empty TR)")
    invalid_tr_empty = Page(Html([Head(Title(Text("Test"))), Body([Table(Tr([]))])]))
    print(f"   Valid: {invalid_tr_empty.is_valid()}")

    print("\n" + "=" * 50)
    print("COMPREHENSIVE TEST - ALL TAGS WORKING CORRECTLY")
    print("=" * 50)

    comprehensive_valid_page = Page(
        Html(
            [
                Head(Title(Text("Othmane Title Test"))),
                Body(
                    [
                        H1(Text("This is H1")),
                        H2(Text("This is H2")),
                        Div(
                            [
                                Text("Text inside Div"),
                                Span(
                                    [
                                        Text("Text inside Span"),
                                        P(
                                            [
                                                Text("Text inside P"),
                                                Text("Text inside P"),
                                            ]
                                        ),
                                    ]
                                ),
                                Ul(
                                    [
                                        Li(Text("First list item")),
                                        Li(Text("Second list item")),
                                        Li(Text("Third list item")),
                                    ]
                                ),
                                Ol(
                                    [
                                        Li(Text("First numbered item")),
                                        Li(Text("Second numbered item")),
                                    ]
                                ),
                            ]
                        ),
                        Div(
                            [
                                H2(Text("Table Section")),
                                Table(
                                    Tr(
                                        [
                                            Th(Text("Header 1")),
                                            Th(Text("Header 2")),
                                            Th(Text("Header 3")),
                                        ]
                                    )
                                ),
                            ]
                        ),
                        Div(
                            [
                                Table(
                                    Tr(
                                        [
                                            Td(Text("Data 1")),
                                            Td(Text("Data 2")),
                                            Td(Text("Data 3")),
                                        ]
                                    )
                                )
                            ]
                        ),
                        Div(
                            [
                                H2(Text("Nested Content")),
                                Div(
                                    [
                                        Span(
                                            [
                                                Text("Nested span with "),
                                                P([Text("nested paragraph")]),
                                            ]
                                        ),
                                        Ul(
                                            [
                                                Li(Text("Nested list item 1")),
                                                Li(Text("Nested list item 2")),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        )
    )

    print("\n19. Comprehensive test with all tag types:")
    print(f"    Valid: {comprehensive_valid_page.is_valid()}")

    if comprehensive_valid_page.is_valid():
        print(comprehensive_valid_page)
        comprehensive_valid_page.write_to_file("test.html")
        print("\nComplete HTML written to 'test.html'")
    else:
        print("\nCOMPREHENSIVE TEST FAILED - Check validation logic!")
