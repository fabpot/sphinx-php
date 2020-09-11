# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2010-2012 Fabien Potencier
    :license: MIT, see LICENSE for more details.
"""

from docutils.parsers.rst import Directive, directives
from docutils import nodes


class configurationblock(nodes.General, nodes.Element):
    pass


class ConfigurationBlock(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}
    formats = {
        'html': 'HTML',
        'xml': 'XML',
        'php': 'PHP',
        'yaml': 'YAML',
        'jinja': 'Twig',
        'html+jinja': 'Twig',
        'jinja+html': 'Twig',
        'twig': 'Twig',
        'html+twig': 'Twig',
        'twig+html': 'Twig',
        'php+html': 'PHP',
        'html+php': 'PHP',
        'ini': 'INI',
        'markdown': 'Markdown',
        'php-annotations': 'Annotations',
        'php-attributes': 'Attributes',
        'php-standalone': 'Standalone Use',
        'php-symfony': 'Framework Use',
        'rst': 'reStructuredText',
        'varnish2': 'Varnish 2',
        'varnish3': 'Varnish 3',
        'varnish4': 'Varnish 4',
        'blackfire': 'Blackfire',
        'bash': 'Bash',
        'apache': 'Apache',
        'nginx': 'Nginx',
        'terminal': 'Terminal',
        'env': '.env',
    }

    def run(self):
        env = self.state.document.settings.env

        node = nodes.Element()
        node.document = self.state.document
        self.state.nested_parse(self.content, self.content_offset, node)

        entries = []
        for i, child in enumerate(node):
            if isinstance(child, nodes.literal_block):
                # add a title (the language name) before each block
                #targetid = "configuration-block-%d" % env.new_serialno('configuration-block')
                #targetnode = nodes.target('', '', ids=[targetid])
                #targetnode.append(child)

                innernode = nodes.emphasis(self.formats[child['language']],
                                           self.formats[child['language']])

                para = nodes.paragraph()
                para += [innernode, child]

                entry = nodes.list_item('')
                entry.append(para)
                entries.append(entry)

        resultnode = configurationblock()
        resultnode.append(nodes.bullet_list('', *entries))

        return [resultnode]


def visit_configurationblock_html(self, node):
    self.body.append(self.starttag(node, 'div', CLASS='configuration-block'))


def depart_configurationblock_html(self, node):
    self.body.append('</div>\n')


def visit_configurationblock_latex(self, node):
    pass


def depart_configurationblock_latex(self, node):
    pass


def setup(app):
    app.add_node(configurationblock,
                 html=(visit_configurationblock_html,
                       depart_configurationblock_html),
                 latex=(visit_configurationblock_latex,
                        depart_configurationblock_latex))
    app.add_directive('configuration-block', ConfigurationBlock)

    return {'parallel_read_safe': True}
