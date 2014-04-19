from entity.room import Room

class WolfDen(Room):
    def verifyCanBeRetrieved(self,
                             retrievingParty=None):
        slot = self.inventory.slots['inside']
        wolf = slot['Wolf']
        return wolf.stateMachine.currentState.verifyCanBeRetrieved()
        