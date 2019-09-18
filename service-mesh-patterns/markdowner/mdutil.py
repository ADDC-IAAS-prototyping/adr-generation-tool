
class MDUtil():

    def add_lvl_1_header(self, headerName):
        return "# {}\n".format(headerName)

    def add_lvl_2_header(self, headerName):
        return "## {}\n".format(headerName)

    def add_lvl_3_header(self, headerName):
        return "### {}\n".format(headerName)

    def add_lvl_4_header(self, headerName):
        return "#### {}\n".format(headerName)

    def add_lvl_5_header(self, headerName):
        return "##### {}\n".format(headerName)

    def add_lvl_6_header(self, headerName):
        return "###### {}\n".format(headerName)

    def add_paragraph(self, paragraphContent):
        return "{}\n".format(paragraphContent)

    def add_spacing(self):
        return "\n"