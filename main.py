import Client
import Graphics

class ClientGraphicsInterface:
    def __init__(self):
        self.client = Client.Client()
        self.updater = Graphics.GraphicsUpdater(self.client)
        self.client.set_observer(self.updater)
        self.client.gameLoop()

if __name__ == '__main__':
    c = ClientGraphicsInterface()
