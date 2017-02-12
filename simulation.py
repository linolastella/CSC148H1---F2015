"""Assignment 1 - Grocery Store Simulation (Task 3)

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""

from container import PriorityQueue
from store import GroceryStore
from event import JoinLine, FinishCheckingOut, create_event_list


class GroceryStoreSimulation:
    """A Grocery Store simulation.

    This is the class which is responsible for setting up and running a
    simulation.
    """
    # === Private Attributes ===
    # @type _events: PriorityQueue[Event]
    #     A sequence of events arranged in priority determined by the event
    #     sorting order.
    # @type _store: GroceryStore
    #     The grocery store associated with the simulation.

    def __init__(self, store_file):
        """Initialize a GroceryStoreSimulation from a file.

        @type store_file: str
            A file containing the configuration of the grocery store.
        @rtype: None
        """
        self._events = PriorityQueue()
        self._store = GroceryStore(store_file)

    def run(self, event_file):
        """Run the simulation on the events stored in <event_file>.

        Return a dictionary containing statistics of the simulation,
        according to the specifications in the assignment handout.

        @type self: GroceryStoreSimulation
        @type event_file: str
            A filename referring to a raw list of events.
            Precondition: the event file is a valid list of events.
        @rtype: dict[str, object]
        """
        stats = {
            'num_customers': 0,
            'total_time': 0,
            'max_wait': -1
        }

        initial_events = create_event_list(event_file)
        max_times = []

        for event in initial_events:
            self._events.add(event)
            if type(event) is JoinLine:
                self._store.costumers.add(event.cos)
            else:
                event.line = self._store.lines[event.line]
                # To avoid creating another public attribute for the class
                # CloseLine, I intentionally stored the index of the line that
                # will close in a " wrong " attribute (in event.line) from the
                # create_event_list function, and here I fix it.

        while not self._events.is_empty():
            next_event = self._events.remove()
            new_events = next_event.do(self._store)
            if type(next_event) is FinishCheckingOut:
                max_times.append(next_event.cos.total_time_waited)
            for event in new_events:
                self._events.add(event)
            stats['total_time'] = next_event.timestamp

        stats['num_customers'] = len(self._store.costumers)
        stats['max_wait'] = max(max_times)
        return stats


if __name__ == '__main__':
    sim = GroceryStoreSimulation('config.json')
    final_stats = sim.run('events.txt')
    print(final_stats)
