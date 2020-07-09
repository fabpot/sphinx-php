"""
    :copyright: (c) 2010-2015 Fabien Potencier
    :license: MIT, see LICENSE for more details.
"""

from sphinx.directives.code import CodeBlock
from docutils.parsers.rst import directives
from docutils import nodes
try:
    from html import escape
except ImportError:
    # old python 2
    from cgi import escape

"""
A wrapper around the built-in CodeBlock class to always
enable line numbers.
and add support for zerocopy
"""
class NumberedCodeBlock(CodeBlock):
    option_spec = {
        'linenos': directives.flag,
        'zerocopy': directives.flag,
        'dedent': int,
        'lineno-start': int,
        'emphasize-lines': directives.unchanged_required,
        'caption': directives.unchanged_required,
        'class': directives.class_option,
        'name': directives.unchanged,
    }

    def run(self):
        self.options['linenos'] = True
        literal = super(NumberedCodeBlock, self).run()[0];

        if 'zerocopy' in self.options:
            resultnode = codeblock()
            resultnode['code'] = u'\n'.join(self.content)
            resultnode['zerocopy'] = 'zerocopy'
            resultnode.append(literal)

            return [resultnode]
        else:
            return [literal]

class codeblock(nodes.General, nodes.Element):
    pass


def visit_codeblock_html(self, node):
    if 'zerocopy' in node:
        self.body.append(
            self.starttag(node, 'div', CLASS='zeroclipboard-pre input-group'))


def depart_codeblock_html(self, node):
    if 'zerocopy' in node:
        self.body.append('''
    <span class="input-group-btn zeroclipboard-group-btn">
        <button data-clipboard-text="%s" class="zeroclipboard btn" type="button">
           <svg viewBox="0 0 20 20" version="1.1" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" xml:space="preserve">
           <path d="M17,14.7c0,0.6-0.4,1-1,1H8.9c-0.6,0-1-0.4-1-1c0-0.6,0.4-1,1-1H16C16.6,13.7,17,14.2,17,14.7z M16,10.2H8.9
               c-0.6,0-1,0.4-1,1c0,0.6,0.4,1,1,1H16c0.6,0,1-0.4,1-1C17,10.6,16.6,10.2,16,10.2z M16,6.6H8.9c-0.6,0-1,0.4-1,1s0.4,1,1,1H16
               c0.6,0,1-0.4,1-1S16.6,6.6,16,6.6z M20.6,5.7v10.2c0,2.2-1.8,4.1-4.1,4.1H8.4C7,20,5.7,19.3,5,18.2c-0.2,0.1-0.4,0.2-0.6,0.2
               c-2.2,0-4.1-1.8-4.1-4.1V4.1C0.4,1.8,2.2,0,4.4,0h8.2c0.6,0,1,0.4,1,1c0,0.2-0.1,0.4-0.2,0.6h3.1C18.8,1.6,20.6,3.4,20.6,5.7z
                M6.6,2H4.4C3.3,2,2.4,3,2.4,4.1v10.2c0,1.1,0.9,2,2,2.1c0-0.2,0-0.3,0-0.5V5.7C4.3,4.1,5.3,2.7,6.6,2z M18.6,5.7
               c0-1.1-0.9-2.1-2.1-2.1H8.4c-1.1,0-2.1,0.9-2.1,2.1v10.2C6.3,17,7.2,18,8.4,18h8.2c1.1,0,2.1-0.9,2.1-2.1V5.7z"/>
           </svg>
        </button>
    </span>
</div>
        ''' % escape(node['code']))


def visit_codeblock_latex(self, node):
    pass


def depart_codeblock_latex(self, node):
    pass


def setup(app):
    app.add_node(codeblock,
                 html=(visit_codeblock_html, depart_codeblock_html),
                 latex=(visit_codeblock_latex, depart_codeblock_latex))
    app.add_directive('code-block', NumberedCodeBlock, override = True)
    app.add_directive('sourcecode', NumberedCodeBlock, override = True)

    return {'parallel_read_safe': True}
