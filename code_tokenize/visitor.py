

class ASTVisitor:

    # Decreased version of visit (no edges are supported) -----------------------

    def visit(self, node):
        # Default handler: Override to capture all nodes
        pass

    def _visit(self, node):
        visitor_fn = getattr(self, "visit_%s" % node.type, self.visit)
        return visitor_fn(node) is not False

    # Navigation ----------------------------------------------------------------

    def walk(self, root_node):
        cursor   = root_node.walk()
        has_next = True

        while has_next:
            current_node = cursor.node
            # Step 1: Try to go to next child if we continue the subtree
            if self._visit(current_node):
                has_next = cursor.goto_first_child()
            else:
                has_next = False

            # Step 2: Stop if parent or sibling is out of subtree
            if not has_next and node_equal(current_node, root_node):
                break

            # Step 3: Try to go to next sibling
            if not has_next:
                has_next = cursor.goto_next_sibling()

            previous_node = current_node

            # Step 4: Go up until sibling exists
            while not has_next and cursor.goto_parent():
                if node_equal(cursor.node, root_node): break
                has_next = cursor.goto_next_sibling()
                has_next = has_next and not node_equal(previous_node, cursor.node)

    def __call__(self, root_node):
        return self.walk(root_node)


# Helper --------------------------------

def node_equal(n1, n2):
    if n1 == n2: return True
    try:
        return (n1.type == n2.type 
                    and n1.start_point == n2.start_point
                    and n1.end_point   == n2.end_point)
    except AttributeError:
        return n1 == n2


# Compositions ----------------------------------------------------------------

class VisitorComposition(ASTVisitor):

    def __init__(self, *visitors):
        super().__init__()
        self.visitors = visitors

    def _visit(self, node):
        for base_visitor in self.visitors:
            if base_visitor._visit(node) is False: return False
        return True
