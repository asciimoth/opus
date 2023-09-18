import src.opus as opus
import src.opus.main as main


def test_version():
    assert opus.__version__ == "0.1.0"


def test_helloworld():
    assert main.helloworld() == "Hello World"
