from utils import Camera


if __name__ == "__main__":
    camera = Camera.VideoFeed()
    camera.start()