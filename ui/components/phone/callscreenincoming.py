from ui.components.phone.callscreen import CallScreen


class CallScreenIncoming(CallScreen):

    def __init__(self, name, hfp, pbap):
        super().__init__(name, hfp)
        hfp.bind(attention=self.on_call_change)
        self.pbap = pbap
        self.ids.decline.bind(on_press=self.on_decline)
        self.ids.accept.bind(on_press=self.on_accept)

    def on_call_change(self, instance, value):
        if value[0] is not None:
            try:
                self.ids.number.text = self.pbap.phonebook_search(value[0].line_id)
            except KeyError:
                self.ids.number.text = value[0].line_id
                print(value[0].line_id)

    def on_decline(self, isinstance):
        self.parent.active_call.hangup()

    def on_accept(self, instance):
        self.parent.active_call.accept()
