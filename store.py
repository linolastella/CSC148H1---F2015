"""Assignment 1 - Grocery Store Models (Task 1)

This file should contain all of the classes necessary to model the entities
in a grocery store.
"""
import json


class GroceryStore:
    """A grocery store.

    A grocery store contains customers and checkout lines.

    === Attributes ===
    @type lines: list[CheckoutLine]
        A list of checkout lines in this grocery store.
    @type costumers: set[Costumer]
        A collection of costumers in the grocery store.
    """

    # === Private Attributes ===
    # @type _lines_capacity: int
    #    The maximum number of costumers allowed to join a checkout line.

    def __init__(self, filename):
        """Initialize a GroceryStore from a configuration file <filename>.

        @type filename: str
            The name of the file containing the configuration for the
            grocery store.
        @rtype: None
        """
        with open(filename, 'r') as file:
            config = json.load(file)
        lines_list = []
        lines_cap = config['line_capacity']
        for i in range(config['cashier_count']):
            lines_list.append(Cashier())
        for i in range(config['express_count']):
            lines_list.append(Express())
        for i in range(config['self_serve_count']):
            lines_list.append(SelfServe())
        self.lines = lines_list
        self.costumers = set()
        self._lines_capacity = lines_cap

    def _is_allowed(self, line, cos):
        """This is a helper function used *only* in the <assign_to_line> method.

        Return True if and only if the costumer <cos> is allowed to join the
        checkout line <line>.

        @type self: GroceryStore
        @type cos: Costumer
        @type line: CheckoutLine
        @rtype: Bool
        """
        if type(line) is Express:
            return cos.items < 8
        return True

    def _helper_on_lines(self, lines):
        """This is a helper function used *only* in the <assign_to_line> method.

        It takes a list of checkout lines that the costumer is theoretically
        allowed to join and returns the one he/she will actually join according
        to the algorithm.

        @type self: GroceryStore
        @type lines: list [CheckoutLine]
        @rtype: CheckoutLine
        """
        k = 0
        for i in range(len(lines)):
            if len(lines[i].costumers_list) < len(lines[k].costumers_list):
                k = i
        return lines[k]

    def assign_to_line(self, costumer):
        """Return the line that the costumer should join.


        Algorithm:   When a new customer joins, he or she always joins the open
        line with the fewest number of customers that he or she is allowed to
        join, choosing the one with the lowest index (as represented by the
        grocery store) if there is a tie.


        @type self: GroceryStore
        @type costumer: Costumer
        @rtype: CheckoutLine
        """
        if len(self.lines) == 1:
            return self.lines[0]
        else:
            checkout_lines = []
            for line in self.lines:
                if self._is_allowed(line, costumer) and \
                        len(line.costumers_list) < self._lines_capacity:
                    checkout_lines.append(line)
        return self._helper_on_lines(checkout_lines)

    def close(self, line):
        """Close the checkout line <line> in the grocery store.

        @type self: GroceryStore
        @type line: CheckoutLine
        @rtype: None
        """
        self.lines.remove(line)


class Costumer:
    """A costumer in the grocery store.

    === Attributes ===
    @type id: str
        The unique string identifier of the costumer.
    @type items: int
        The number of items that costumer wants to purchase
    @type joined_store: int
        The *first* timestamp of a JoinLine event assigned to this costumer.
        If the costumer joins two different lines (i. e. the first one he joined
        closes), the first timestamp is the one considered.
    @type total_time_waited: int
        The total time a costumer spent in the grocery store.
    """
    def __init__(self, name, items):
        """Initialize a Costumer.

        @type self: Costumer
        @type name: str
        @type items: int
        @rtype: None

        >>> c = Costumer('Joseph', 10)
        >>> c.id
        'Joseph'
        >>> c.items
        10
        """
        self.id = name
        self.items = items
        self.joined_store = None
        self.total_time_waited = None


class CheckoutLine:
    """A checkout line in the grocery store.

    === Attributes ===
    @type costumers_list: list[Costumer]
        A list of costumers queueing in the checkout line.
    """
    def __init__(self):
        """Initialize a CheckoutLine.

        @type self: CheckoutLine
        @rtype: None
        """
        self.costumers_list = []

    def time_to_checkout(self, items):
        """Return the time it takes to checkout <items> items.

        This amount of times varies depending on the type of checkout line.

        @type self: CheckoutLine
        @type items: int
        @rtype: int
        """
        raise NotImplementedError


class Cashier(CheckoutLine):
    """A type of checkout line.

    """
    def __init__(self):
        """Initialize this subclass.

        @type self: Cashier
        @rtype: None
        """
        super(Cashier, self).__init__()

    def time_to_checkout(self, items):
        """This method overrides the one in the superclass.

        @type self: Cashier
        @type items: int
        @rtype: int

        >>> c = Cashier()
        >>> c.time_to_checkout(39)
        46
        """
        return items + 7


class Express(CheckoutLine):
    """A type of checkout line.

    """
    def __init__(self):
        """Initialize this subclass.

        @type self: Express
        @rtype: None
        """
        super(Express, self).__init__()

    def time_to_checkout(self, items):
        """This method overrides the one in the superclass.

        @type self: Express
        @type items: int
        @rtype: int

        >>> e = Express()
        >>> e.time_to_checkout(1)
        5
        """
        return items + 4


class SelfServe(CheckoutLine):
    """A type of checkout line.

    """
    def __init__(self):
        """Initialize this subclass.

        @type self: SelfServe
        @rtype: None
        """
        super(SelfServe, self).__init__()

    def time_to_checkout(self, items):
        """This method overrides the one in the superclass.

        @type self: SelfServe
        @type items: int
        @rtype: int

        >>> s = SelfServe()
        >>> s.time_to_checkout(11)
        23
        """
        return (2 * items) + 1
