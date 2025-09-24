#!/usr/bin/python3

class Text(str):
    """
    A Text class to represent a text you could use with your HTML elements.

    Because directly using str class was too mainstream.
    """

    def __str__(self):
        """
        Do you really need a comment to understand this method?..
        """
        return (
            super()
            .__str__()
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("\n", "\n<br />\n")
        )


class Elem:
    """
    Elem will permit us to represent our HTML elements.
    """

    class ValidationError(Exception):
        def __init__(self):
            super().__init__("incorrect behaviour.")

    def __init__(self, tag="div", attr={}, content=None, tag_type="double"):
        """
        __init__() method.

        Obviously.
        """
        # if content is not None and len(content) == 0:
        #     raise Elem.ValidationError
        if content is not None and not self.check_type(content):
            raise Elem.ValidationError
        self.tag = tag
        self.attr = attr
        self.content = content
        self.tag_type = tag_type

    def __str__(self, depth=1):
        """
        The __str__() method will permit us to make a plain HTML representation
        of our elements.
        Make sure it renders everything (tag, attributes, embedded
        elements...).
        """
        result = ""
        if self.tag_type == "double":
            result += (
                f"<{self.tag}{self.__make_attr()}>"
                f"{self.__make_content(depth)}"
                f"</{self.tag}>"
            )
        elif self.tag_type == "simple":
            f"<{self.tag}{self.__make_attr()}/>"
        return result

    def __make_attr(self):
        """
        Here is a function to render our elements attributes.
        """
        result = ""
        for pair in sorted(self.attr.items()):
            result += " " + str(pair[0]) + '="' + str(pair[1]) + '"'
        return result

    def __make_text_content(
        self,
        textInstance,
        element_position,
        previous_element=None,
        is_last_element=False,
    ):
        if len(textInstance) == 0:
            return ""

        text_content = ""
        if element_position == 0 or isinstance(previous_element, Text):
            text_content += "\n"
        text_content += f"  {textInstance.__str__()}"
        if is_last_element:
            text_content += "\n"
        return text_content

    def __make_elem_content(self, elemInstance, depth, elementPosition):
        result = ""

        if elementPosition == 0:
            result = "\n"
        return result + (
            f"{"  " * depth}{elemInstance.__str__(depth)}\n"
        )

    def __make_content(self, depth=1):
        """
        Here is a method to render the content, including embedded elements.
        """

        if self.content is None or len(self.content.__str__()) == 0:
            return ""

        result = ""
        if isinstance(self.content, list):
            pass
            for elementPosition, elem in enumerate(self.content):
                if isinstance(elem, Text):
                    previous_element = (
                        self.content[elementPosition - 1]
                        if elementPosition - 1 >= 0
                        else None
                    )
                    result += self.__make_text_content(
                        elem,
                        elementPosition,
                        previous_element,
                        elementPosition == len(self.content) - 1,
                    )
                else:
                    result += self.__make_elem_content(elem, depth, elementPosition)
        elif isinstance(self.content, Text):
            result += f"\n{" " * depth}{self.content.__str__()}{" "}\n"
        else:
            result += f"\n{"  " * depth}{self.content.__str__(depth + 1)}\n{"  " * (depth - 1)}"
        return result

    def add_content(self, content):
        if not Elem.check_type(content):
            raise Elem.ValidationError
        if type(content) == list:
            self.content += [elem for elem in content if elem != Text("")]
        elif content != Text(""):
            self.content.append(content)

    @staticmethod
    def check_type(content):
        """
        Is this object a HTML-compatible Text instance or a Elem, or even a
        list of both?
        """
        return (
            isinstance(content, Elem)
            or type(content) == Text
            or (
                type(content) == list
                and all(
                    [type(elem) == Text or isinstance(elem, Elem) for elem in content]
                )
            )
        )


if __name__ == "__main__":
    test = Elem(tag="html", content=Elem(tag="body", content=Elem(tag="p", content=[Elem("h1"), Elem("h2")])))
    print(test)
    # html_content = Elem(
    #     tag="html",
    #     content=[
    #         Elem("head", content=[Elem("title")]),
    #         Elem(
    #             "body",
    #             content=[
    #                 Elem("h1"),
    #                 Elem(
    #                     "img",
    #                     attr={"src": "http://i.imgur.com/pfp3T.jpg"},
    #                     tag_type="double",
    #                 ),
    #             ],
    #         ),
    #     ],
    # )

    # print(html_content)
