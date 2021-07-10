import dramatiq
import pytest
from feed.models import Feed


@pytest.fixture
def broker():
    broker = dramatiq.get_broker()
    broker.emit_after("process_boot")
    broker.flush_all()
    return broker


@pytest.fixture
def worker(broker):
    worker = dramatiq.worker.Worker(broker, worker_timeout=100)
    worker.start()
    yield worker
    worker.stop()


@pytest.fixture()
def empty_feed():
    feed = Feed.objects.create(
        link="http://www.nu.nl/rss/Algemeen", title="nu.nl")
    return feed
