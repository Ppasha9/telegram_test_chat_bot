from transitions import Machine


class BotState:
    states = ["waiting_for_product_select", "waiting_for_size_select", "waiting_for_payment_select"]

    def __init__(self):
        self._machine = Machine(model=self, states=BotState.states, initial="waiting_for_product_select")

        self._machine.add_transition(
            trigger="product_selected",
            source="waiting_for_product_select",
            dest="waiting_for_size_select",
            after="_set_product_name")

        self._machine.add_transition(
            trigger="size_selected",
            source="waiting_for_size_select",
            dest="waiting_for_payment_select",
            after="_set_product_size")

        self._machine.add_transition(
            trigger="payment_selected",
            source="waiting_for_payment_select",
            dest="waiting_for_product_select",
            after="_set_payment_method")

    def _clear_state(self):
        self._state = dict()

    def _set_product_name(self, product_name):
        self._clear_state()
        self._state["product"] = product_name

    def _set_product_size(self, product_size):
        self._state["product_size"] = product_size

    def _set_payment_method(self, payment_method):
        self._state["payment_method"] = payment_method

    def get_product_name(self):
        return self._state["product"]

    def get_product_size(self):
        return self._state["product_size"]

    def get_payment_method(self):
        return self._state["payment_method"]

    def is_waiting_for_product_name(self):
        return self.state == "waiting_for_product_select"

    def is_waiting_for_product_size(self):
        return self.state == "waiting_for_size_select"

    def is_waiting_for_payment_method(self):
        return self.state == "waiting_for_payment_select"
