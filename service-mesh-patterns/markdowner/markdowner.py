import datetime
from mdutil import MDUtil

class Markdowner():

    date = datetime.datetime.now().strftime("%x")
    path = "doc/architecture/decisions/"

    def __init__(self, fileName):
        self.path += fileName + '.md'

    def grab_config_set(self):
        config_dict = {}
        with open(self.path, "r") as md:
            line = md.readline()
            while line:
                if line == MDUtil().add_lvl_2_header('Config Set'):
                    paragraph = md.readline()
                    while paragraph == '\n':
                        paragraph = md.readline()
                    config = filter(None, paragraph.replace('}', '').replace('{', '').replace(', ', '\n').split('\n'))
                    for dic in config:
                        dic_list = dic.split(': ')
                        config_dict[dic_list[0].replace('\'', '')] = dic_list[1].replace('u\'', '\'').replace('\'', '')
                    return config_dict
                line = md.readline()
        return None

    def generate_ADR(self, header, contentStatus, contentContext, contentDecision, contentConsequences, contentDSL):
        with open(self.path, "w") as md:
            util = MDUtil()
            ################################################
            md.write(util.add_lvl_1_header(header))
            ################################################
            md.write(util.add_spacing())
            ################################################
            md.write(util.add_paragraph('Date: {}'.format(self.date)))
            ################################################
            md.write(util.add_spacing())
            ################################################
            md.write(util.add_lvl_2_header('Status'))
            md.write(util.add_paragraph(contentStatus))
            ################################################
            md.write(util.add_spacing())
            ################################################
            md.write(util.add_lvl_2_header('Context'))
            md.write(util.add_paragraph(contentContext))
            ################################################
            md.write(util.add_spacing())
            ################################################
            md.write(util.add_lvl_2_header('Decision'))
            md.write(util.add_paragraph(contentDecision))
            ################################################
            md.write(util.add_spacing())
            ################################################
            md.write(util.add_lvl_2_header('Consequences'))
            md.write(util.add_paragraph(contentConsequences))
            ################################################
            md.write(util.add_spacing())
            ################################################
            md.write(util.add_lvl_2_header('Config Set'))
            md.write(util.add_paragraph(contentDSL))
            ################################################
            md.write(util.add_spacing())
            ################################################

if __name__ == '__main__':
    md = Markdowner('file_name')
    md.path = '../' + md.path
    md.generate_ADR('1. Record test',
     'none', 'some context stuff', 
     'some decision stuff', 
     'some consequences', 
     'content of the DSL')