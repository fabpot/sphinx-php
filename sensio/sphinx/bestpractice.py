from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from docutils import nodes
from sphinx import addnodes
from sphinx.locale import _


class bestpractice(nodes.Admonition, nodes.Element): pass


class BestPractice(BaseAdmonition):

    node_class = bestpractice


def visit_bestpractice_node(self, node):
    self.visit_admonition(node, 'best-practice')


def depart_bestpractice_node(self, node):
    self.depart_admonition(node)


def setup(app):
    app.add_node(bestpractice,
                 html=(visit_bestpractice_node, depart_bestpractice_node))
    app.add_directive('best-practice', BestPractice)

    return {'parallel_read_safe': True}
